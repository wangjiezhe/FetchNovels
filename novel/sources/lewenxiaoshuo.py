#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.lewenxiaoshuo.com/books/{}/'


class Lewenxiaoshuo(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='#intro',
                         chap_type=serial.ChapterType.whole,
                         chap_sel='dd',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('title').text()
        return re.match(r'(.*)\((.*?)\),.*', st).groups()
