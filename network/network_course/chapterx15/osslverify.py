# -*- coding:utf-8 -*-
__author__ = 'walkskyer'
"""

success domain: www.python.org github.org
error domain:www.baidu.com
"""
import socket, sys
from OpenSSL import SSL

cafile, host = ('cert/digiCert.chain', 'www.python.org')

if len(sys.argv) > 1:
    host = sys.argv[1]

def printX509(x509):
    """Display an x.509 certificate"""
    fields = {
        'contry_name': 'Country',
        'SP': 'State/Province',
        'L': 'Locality',
        'O': 'Organization Unit',
        'OU': 'Organizational Unit',
        'CN': 'Common Name',
        'email': 'E-Mail'
    }
    for field, desc in fields.items():
        try:
            print "%30s: %s" % (desc, getattr(x509, field))
        except:
            pass

# Whether or not the certificate name has bean verified
cnverified = 0

def verify(connection, certificate, errnum, depth, ok):
    """Verify a given certificate"""
    global cnverified

    subject = certificate.get_subject()
    issuer = certificate.get_issuer()

    print "Certificate from:"
    printX509(subject)

    if not ok:
        # OpenSSL could not verify the digital signature
        print "Could not verify certificate"
        return 0

    # Digital signature verified. Now make sure it's for the server
    # we connected to.
    if subject.CN == None or subject.CN.lower() !=  host.lower():
        print "Connected to %s, but got cert for %s "% \
              (host, subject.CN)
    else:
        cnverified = 1

    if depth == 0 and not cnverified:
        print "Could not verify server name; failing."
        return 0

    print "-" * 70
    return 1

if __name__ == "__main__":
    # Create SSL context object
    ctx = SSL.Context(SSL.SSLv23_METHOD)
    ctx.load_verify_locations(cafile)

    # Set up the verification. Notice we pass the verify function to
    # ctx.set_verify
    ctx.set_verify(SSL.VERIFY_PEER | SSL.VERIFY_FAIL_IF_NO_PEER_CERT, verify)


    print "Create socket ..."
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print "done."

    # Create SSL connection object
    ssl = SSL.Connection(ctx, s)

    print "Establishing SSL..."
    ssl.connect((host, 443))
    print "done."

    print "Requsting document...",
    ssl.sendall("GET / HTTP/1.0\r\nHost:www.python.org\r\n\r\n")
    print "done."

    while 1:
        try:
            buf = ssl.recv(4096)
        except SSL.ZeroReturnError:
            break
        sys.stdout.write(buf)

    ssl.close()