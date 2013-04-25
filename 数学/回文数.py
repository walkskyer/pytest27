# coding=gbk
__author__ = 'weijie'
'''
"������"��һ�����֡��磺98789, �������������98789,����Ҳ��98789,��������һ��������������־��ǻ�������
�ű���Դ:http://www.oschina.net/code/snippet_554209_20748
��ruby̫���ˡ�:www.oschina.net/translate/ruby-is-too-slow-for-programming-competitions
'''
import math
import time


def is_palindrome(num):
    '''�ж��Ƿ�Ϊ������'''
    str_num = str(num)
    if (str_num[0] == str_num[-1]):
        i_len = len(str_num) / 2
        for i in xrange(i_len):
            if (str_num[i] != str_num[-(i + 1)]):
                return False
        return True
def is_palindrome2(num):
    '''һ���µ��ж��Ƿ�Ϊ�������ķ���'''
    s = str(num)
    return s == s[::-1]

if __name__ == '__main__':
    start=1
    end = 10000000
    print 'first:'
    t = time.clock()
    aa = [{x: x * x} for x in xrange(start,end) if is_palindrome(x) and is_palindrome(x * x)]
    print aa
    print time.clock() - t

    print 'secend'
    t=time.clock()
    bb=[{x:x*x} for x in xrange(start,end) if is_palindrome2(x) and is_palindrome2(x*x)]
    print bb
    print 'time:',time.clock()-t