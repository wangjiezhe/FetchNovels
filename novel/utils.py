#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urlparse, urlunparse


class Tool(object):

    def __init__(self):
        self._remove_a = re.compile(r'<a.*?>.*?</a>', re.I)
        self._remove_div = re.compile(r'<div.*?>.*?</div>',
                                      re.I | re.S)
        self._remove_span = re.compile(r'<span.*?>.*?</span>', re.I)
        self._remove_script = re.compile(r'<script.*?>.*?</script>',
                                         re.I | re.S)
        self._replace_br = re.compile(r'<br\s*/\s*>|</\s*br>', re.I)
        self._replace_p = re.compile(r'</?p>', re.I)
        self._replace_xa0 = re.compile(r'\xa0')
        self._replace_u3000 = re.compile(r'\u3000')
        self._remove_ufeff = re.compile(r'\ufeff')
        self._remove_r = re.compile(r'&#13;|\r')
        self.replace_extras = []
        self.remove_extras = []
        self._remove_ot = re.compile(r'<.*?>')

    def replace(self, text):
        text = re.sub(self._remove_a, '', text)
        text = re.sub(self._remove_div, '', text)
        text = re.sub(self._remove_script, '', text)
        text = re.sub(self._replace_br, '\n', text)
        text = re.sub(self._replace_p, '\n', text)
        text = re.sub(self._replace_xa0, ' ', text)
        text = re.sub(self._replace_u3000, '  ', text)
        text = re.sub(self._remove_ufeff, '', text)
        text = re.sub(self._remove_r, '', text)
        for s, d in self.replace_extras:
            text = re.sub(s, d, text)
        for pat in self.remove_extras:
            text = re.sub(pat, '', text)
        text = re.sub(self._remove_ot, '', text)
        return text

    def refine(self, text):
        text = self.replace(text)

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
