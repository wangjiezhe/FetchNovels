#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from .. import serial, utils, config

BASE_URL = 'http://www.danmei123.com/{}/'


class Danmei123(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.box_box',
                         None, '.j_box .words p',
                         chap_sel='.list_box li',
                         chap_type=serial.ChapterType.path,
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'description'
        ).attr('content')
        pat = re.compile(r'(.*)的新书(.*)最新章节.*')
        author, name = re.match(pat, st).groups()

        return name, author
