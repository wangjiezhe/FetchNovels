#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.yibanzhu.com/html/{}/'


class Yibanzhu(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content:eq(1)',
                         intro_sel='#intro',
                         chap_type=serial.ChapterType.path,
                         chap_sel='#list dd',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('#info p:first').text()
        author = re.match(r'作.*?者：(.*)', st).group(1)
        return name, author
