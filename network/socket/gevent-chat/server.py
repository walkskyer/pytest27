# -*- coding:utf-8 -*-
__author__ = 'walkskyer'
"""
gevent 玩具3 聊天服务器 服务器端
"""
import gevent
from gevent import monkey
monkey.patch_all()
from collections import deque
import socket


class SockClient():
    def __init__(self,name):
        self.conn = None
        self.addr = None
        self.name = name
        self.msg_queue = deque()

    def msg_append(self, msg):
        if not msg:
            return None
        self.msg_queue.append(msg)

    def msg_pop(self):
        if len(self.msg_queue)>0:
            return self.msg_queue.popleft()
        return None

    def msg_len(self):
        return len(self.msg_queue)

    def set_conn_info(self, conn, addr):
        self.conn = conn
        self.addr = addr

    def recv(self, length=1024, flags=0):
        """
        接收指定长度消息
        :param length:
        :param flags:
        :return:
        """
        try:
            return self.conn.recv(length, flags)
        except socket.error, e:
            print "client-recv(%s):%s"% (self.name,e)
            return None

    def recv_all(self):
        """
        接收全部消息
        :return:
        """
        data = ''
        while True:
            str_tmp = self.recv()
            if not str_tmp:
                break
            data += str_tmp
        return data

    def send(self,string='', flags=0):
        """
        发送一条消息
        :param string:
        :param flags:
        :return:
        """
        if not string and self.conn:
            self.conn.send(string, flags)

    def send_all(self):
        """
        发送队列中的全部消息
        :return:
        """
        while self.msg_len()>0:
            self.send(self.msg_pop())


def send_msg(name, client):
    while True:
        print '%s:%s' % (name, 'I want send')
        if client.msg_len() > 0:
            print '%s:%s' % (name, client.msg_pop())
        else:
            gevent.sleep(5)


def recv_msg(client, client_que):
    while True:
        print '%s:%s' % (client.name, 'I want receive msg')
        msg = client.recv_all()
        if msg:
            print '%s:%s' % (client.name, msg)
            for cli in client_que:
                if cli['client'].name != client.name:
                    cli['client'].msg_append("%s:%s" % (client.name, msg))
        else:
            gevent.sleep(5)


client_que = deque()


def handle(name, cli_info):
    client = SockClient(name)
    client.conn, client.addr = cli_info
    client.conn.setblocking(0)
    print '%s:%s' % (name, client.addr)
    data = {
        'name':name,
        'send' : gevent.Greenlet(send_msg, name, client),
        'recv' : gevent.Greenlet(recv_msg, client, client_que),
        'client' : client
    }
    client_que.append(data)
    data['send'].start()
    data['recv'].start()


def server_forever():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 18888))
    server.listen(20)
    count=1
    print 'I\'m started,Waiting for you...'
    while True:
        cli_info = server.accept()
        name = 'custom_%s' % count
        handle(name, cli_info)
        print 'task join'
        count += 1
if __name__ == "__main__":
    print "server starting"
    server_forever()
