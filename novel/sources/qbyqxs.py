#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils

BASE_URL = 'http://www.qbyqxs.com/book/{}.aspx'


class Qbyqxs(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='#bookintroinner',
                         chap_type=serial.ChapterType.path,
                         chap_sel='#readlist li',
                         tid=tid)

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('.ti p').text()
        author = re.match(r'作者：(.*)', st).group(1)
        return name, author
