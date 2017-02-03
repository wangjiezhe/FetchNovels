#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.amxs520.com/reader/{}/'
INTRO_URL = 'http://www.amxs520.com/book/{}.html'


class Amxs520(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.content span',
                         utils.base_to_url(INTRO_URL, tid), '.bookintro',
                         chap_type=serial.ChapterType.last,
                         chap_sel='.list_Content li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('.author1').text()
        author = re.match(r'作者：(.*)', st).group(1)
        return name, author
