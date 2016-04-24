#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


class Tool(object):

    def __init__(self):
        self._remove_addr = re.compile(r'<a.*?>.*?</a>')
        self._remove_div = re.compile(r'<div.*?>.*?</div>')
        self._replace_br = re.compile(r'<br\s*/\s*>|</\s*br>')
        self._replace_xa = re.compile(r'\xa0')
        self._remove_r = re.compile(r'&#13;|\r')
        self._remove_ot = re.compile(r'<.*?>')

    def replace(self, text):
        text = re.sub(self._remove_addr, '', text)
        text = re.sub(self._remove_div, '', text)
        text = re.sub(self._replace_br, '\n', text)
        text = re.sub(self._replace_xa, ' ', text)
        text = re.sub(self._remove_r, '', text)
        text = re.sub(self._remove_ot, '', text)
        return text.strip()


def fix_order(i):
    if i % 3 == 0:
        return i + 2
    elif i % 3 == 2:
        return i - 2
    else:
        return i


def base_to_url(base_url, tid):
    return base_url % (tid[:-3] if tid[:-3] != '' else 0, tid)
