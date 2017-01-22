#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.baishulou.net/read/{}/{}/'
INTRO_URL = 'http://www.baishulou.net/books_{}.html'


class Baishulou(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '.bintro',
                         chap_type=serial.ChapterType.last,
                         chap_sel='td.dccss',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        author = re.match(r'.*,(.*?),.*?', st).group(1)
        return name, author
