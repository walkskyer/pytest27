# -*- coding:utf-8 -*-
__author__ = 'walkskyer'
"""
udp test
获取时间
cmd:udp02.py
"""
import socket, sys, time, struct

if __name__ == "__main__":
    hostname = 'time.nist.gov'
    port = 37

    host = socket.gethostbyname(hostname)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto('', (host, port))

    print "Looking for replies; press Ctrl-C to stop."
    buf = s.recvfrom(2048)[0]
    if len(buf) != 4:
        print "Wrong-size reply %d: %s" % (len(buf), buf)
        sys.exit(1)

    print buf
    secs = struct.unpack("!I", buf)[0]
    secs -= 2208988800
    print time.ctime(int(secs))