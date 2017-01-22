#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.shushuwu.cc/novel/{}/'
INTRO_URL = 'http://www.shushuwu.cc/book/{}/'


class Shushuwu(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.yd_text2',
                         utils.base_to_url(INTRO_URL, tid), '.bookintro',
                         chap_type=serial.ChapterType.last,
                         chap_sel='dd',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('title').text()
        pat = re.compile(r'(.*?)_.*_(.*?)_.*?')
        return re.match(pat, st).groups()
