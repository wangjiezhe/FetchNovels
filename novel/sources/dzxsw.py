#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils

BASE_URL = 'http://www.dzxsw.la/book/{}/index.html'
INTRO_URL = 'http://www.dzxsw.la/book/{}/'


class Dzxsw(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '#cintro',
                         chap_type=serial.ChapterType.path,
                         chap_sel='.chapterList ul:eq(1) li',
                         tid=tid)

    def get_title_and_author(self):
        name = self.doc('.title').text()
        pat = re.compile(r'作者：(.+)', re.U)
        st = self.doc('.item').filter(
            lambda i, e: re.match(pat, PyQuery(e).text())
        )
        author = re.match(pat, st.text()).group(1)
        return name, author
