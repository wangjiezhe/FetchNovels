#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urlparse, urlunparse


class Tool(object):

    def __init__(self):
        self._remove_addr = re.compile(r'<a.*?>.*?</a>')
        self._remove_div = re.compile(r'<div.*?>.*?</div>')
        self._remove_script = re.compile(r'<script>.*?</script>')
        self._replace_br = re.compile(r'<br\s*/\s*>|</\s*br>')
        self._replace_xa = re.compile(r'\xa0')
        self._replace_u3000 = re.compile(r'\u3000')
        self._remove_r = re.compile(r'&#13;|\r')
        self._remove_ot = re.compile(r'<.*?>')
        self._remove_ex = re.compile(r'GetFont\(\);')

    def replace(self, text):
        text = re.sub(self._remove_addr, '', text)
        text = re.sub(self._remove_div, '', text)
        text = re.sub(self._remove_script, '', text)
        text = re.sub(self._replace_br, '\n', text)
        text = re.sub(self._replace_xa, ' ', text)
        text = re.sub(self._replace_u3000, '  ', text)
        text = re.sub(self._remove_r, '', text)
        text = re.sub(self._remove_ot, '', text)
        text = re.sub(self._remove_ex, '', text)

        text = re.sub(r'\n\s+\n', '\n\n', text)

        return text.strip()


def fix_order(i):
    if i % 3 == 0:
        return i + 2
    elif i % 3 == 2:
        return i - 2
    else:
        return i


def base_to_url(base_url, tid):
    tid = str(tid)
    return base_url % (tid[:-3] if tid[:-3] != '' else 0, tid)


def get_base_url(url):
    result = urlparse(url)
    base_url = urlunparse((result.scheme, result.netloc, '', '', '', ''))
    return base_url
