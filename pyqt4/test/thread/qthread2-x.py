# -*- coding: utf-8 -*-
# filename:qthread2.py
# datetime:2014-03-12 22:30
__author__ = 'walkskyer'
"""

"""
import sys
from PyQt4 import QtGui, QtCore
import time
import random
import subprocess

class MyThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str) # trigger传输的内容是字符串

    def __init__(self, parent=None):
        super(MyThread, self).__init__(parent)

    def run(self):
        time.sleep(random.random()*5)  # random sleep to imitate working
        self.ping_host("www.baidu.com")

    # 把下面代码中的print改为trigger.emit
    def ping_host(self, host):
        subprocess.call(['arp', '-d'], shell=True, stdout=open('NUL', 'w'), stderr=subprocess.STDOUT)
        # print('Pinging  ' + host + u', Please waiting...')
        self.trigger.emit('Pinging  ' + host + u', Please waiting...\n')
        p = subprocess.Popen('ping -n 4 -w 1 %s' % host, stdin = subprocess.PIPE,
                                 stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        self.trigger.emit(p.stdout.read().decode('gbk'))



class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.text_area = QtGui.QTextBrowser()
        self.thread_button = QtGui.QPushButton('Start threads')
        self.thread_button.clicked.connect(self.start_threads)

        central_widget = QtGui.QWidget()
        central_layout = QtGui.QHBoxLayout()
        central_layout.addWidget(self.text_area)
        central_layout.addWidget(self.thread_button)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

    def start_threads(self):
        self.threads = []              # this will keep a reference to threads
        thread = MyThread(self)    # create a thread
        thread.trigger.connect(self.update_text)  # connect to it's signal
        thread.start()             # start the thread
        self.threads.append(thread) # keep a reference

    def update_text(self, message):
        self.text_area.insertPlainText(message) # use insertPlainText to prevent the extra newline character

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    mainwindow = Main()
    mainwindow.show()

    sys.exit(app.exec_())
