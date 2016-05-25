#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
将输入的阿拉伯数字转化为汉字
"""

import sys
import re
from itertools import repeat

ZERO = '零'
NEGATIVE = '负'
DIGITS = ['', '一', '二', '三', '四', '五', '六', '七', '八', '九']
UNITS = ['', '十', '百', '千']
GROUPS = ['', '万', '亿']


def num_to_group(num, nl=None, n=4):
    """
    将数字从右向左，每n位分为一组
    """
    assert(num >= 0)
    if nl is None:
        nl = []
    if num == 0:
        nl.reverse()
        return nl
    else:
        nl.append(num % (10 ** n))
        return num_to_group(num // (10 ** n), nl, n)


def translate(num):
    """
    将一万以内的阿拉伯数字转换为汉字
    """
    assert(num < 10000)
    res = ''
    if num == 0:
        return res
    s = str(num)
    for i in range(-1, -len(s) - 1, -1):
        j = int(s[i])
        if j == 0:
            res = ZERO + res
        else:
            res = DIGITS[int(s[i])] + UNITS[-i - 1] + res
    res = res.rstrip(ZERO)
    res = re.sub('零{2,}', ZERO, res)
    if len(s) < 4:
        res = ZERO + res
    return res


def int_to_cn(num):
    """
    将阿拉伯数字转换为汉字
    """
    assert(type(num) == int)
    res = ''
    if_minus = ''
    if num == 0:
        return ZERO
    elif num < 0:
        if_minus = NEGATIVE
        num = -num
    # if num >= 10 ** 16:
    #     print("只适用于正负一亿亿以下的整数！")
    #     return -1
    words = [translate(k) for k in num_to_group(num)]
    for i in range(-1, -len(words) - 1, -1):
        if -i == 1:
            suf = ''
        else:
            suf = ''.join(repeat(GROUPS[2], (-i) % 2))  # 亿
        if len(words[i]) > 0:
            suf = GROUPS[(-i - 1) % 2] + suf  # 万
        res = words[i] + suf + res
    res = res.lstrip(ZERO)
    res = re.sub('^一十', '十', res)
    res = if_minus + res
    return res


def main():
    arg = sys.argv[1]
    res = int_to_cn(int(arg))
    print(res)


if __name__ == '__main__':
    main()
