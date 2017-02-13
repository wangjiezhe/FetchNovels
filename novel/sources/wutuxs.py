#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.wutuxs.com/html/{}/{}/'


class Wutuxs(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#contents',
                         intro_sel='.js',
                         chap_type=serial.ChapterType.path,
                         chap_sel='td',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('.btitle i:first').text()
        author = re.match(r'作者：(.*)', st).group(1)
        return name, author
