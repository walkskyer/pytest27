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


if __name__ == '__main__':
    t = time.clock()
    x = 1
    y = 100000000000000
    sqr_x = int(math.sqrt(x))
    sqr_y = int(math.sqrt(y))
    aa = [{x: x * x} for x in xrange(sqr_x, sqr_y) if is_palindrome(x) and is_palindrome(x * x)]
    print aa
    print time.clock() - t
