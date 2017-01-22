#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.shushu8.com/{}/'


class Shushu8(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='.bookintro',
                         chap_type=serial.ChapterType.last,
                         chap_sel='li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('title').text()
        pat = re.compile(r'(.+)全文阅读_(.+)作品.*')
        return re.match(pat, st).groups()
