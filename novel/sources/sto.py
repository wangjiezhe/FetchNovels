#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils

BASE_URL = 'http://www.sto.cc/{}-1/'
PAGE_URL = 'http://www.sto.cc/{}-{}/'


class StoTool(utils.Tool):

    def __init__(self):
        super().__init__()

        word_list = (
            's思s兔s網s文s檔s下s載s與s在s線s閱s讀s',
            's本s作s品s由s思s兔s網s提s供s下s載s與s在s線s閱s讀s',
            's本s作s品s由s思s兔s在s線s閱s讀s網s友s整s理s上s傳s',
            's思s兔s在s線s閱s讀s',
            's思s兔s文s檔s共s享s與s在s線s閱s讀s',
        )
        symbol_list = (
            '\^_\^', ':-\)', '\^o\^', '-_-!',
            '││', '//', '\$\$',
        )
        symbols = '|'.join(symbol_list).join(('(.|', ')'))
        pats = (symbols.join(w.split('s')) for w in word_list)

        symbol_extras = ('',)

        self.remove_extras.extend(
            (re.compile(pat) for pat in pats)
        )
        self.remove_extras.extend(
            (re.compile(pat) for pat in symbol_extras)
        )


class Sto(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#BookContent',
                         tid=tid)
        self.tool = StoTool

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        return re.match(r'(.*?),(.*?),.*', st).groups()

    @property
    def chapter_list(self):
        st = re.search(
            r'ANP_goToPage\("Page_select",(\d+),(\d+),1\);', self.doc.html())
        if st.group(1) == self.tid:
            page_num = int(st.group(2))
        else:
            raise Exception('Something strange may happened.')
        return [(i + 1, PAGE_URL.format(self.tid, i + 1), '第{:d}頁'.format(i + 1))
                for i in range(page_num)]

    def get_intro(self):
        intro = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'description'
        ).attr('content')
        return intro
