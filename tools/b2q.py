#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def strQ2B(ustring):
    """把字符串全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
            rstring += uchar
        rstring += chr(inside_code)
    return rstring


def strB2Q(ustring):
    """把字符串半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
            rstring += uchar
        if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code = 0x3000
        else:
            inside_code += 0xfee0
        rstring += chr(inside_code)
    return rstring


def main():
    arg = sys.argv[1]
    res = strB2Q(arg)
    print(res)


if __name__ == '__main__':
    main()
