#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.cmshy.com/spring/{}.html'


class Cmshy(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         chap_type=serial.ChapterType.whole,
                         chap_sel='.index li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('.title').text()
        st = self.doc('.info').text()
        author = re.match(r'作者：(.*)', st).group(1)
        return name, author
