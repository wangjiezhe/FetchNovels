#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.365xs.org/books/{}/{}/'
INTRO_URL = 'http://www.365xs.org/book/{}/index.html'


class Xs365(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         chap_type=serial.ChapterType.last,
                         chap_sel='.chapterlist li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'author').attr('content')
        return re.match(r'(.*)版权属于作者(.*)', st).groups()
