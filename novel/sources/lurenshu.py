#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.lurenshu.net/{}.shtml'


class Lurenshu(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='.excerpt',
                         chap_type=serial.ChapterType.whole,
                         chap_sel='li.min-width',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('title').text()
        return re.match(r'(.*?)\|(.*?)的小说', st).groups()
