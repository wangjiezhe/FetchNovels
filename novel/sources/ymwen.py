#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.ymwen.com/{}/{}/'
INTRO_URL = 'http://www.ymwen.com/book/{}.html'


class Ymwen(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         chap_type=serial.ChapterType.path,
                         chap_sel='.liebiao li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('.infot span').text()
        author = re.match(r'作者：(.*)', st).group(1)
        return name, author
