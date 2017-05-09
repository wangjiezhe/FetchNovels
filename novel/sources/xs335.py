#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.335xs.com/{}/{}/'
INTRO_URL = 'http://www.335xs.com/book/{}.html'


class Xs335Tool(utils.Tool):

    def __init__(self):
        super().__init__()

        self.remove_extras.append(re.compile(r'小强文学网-http://www.335xs.com'))


class Xs335(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         chap_type=serial.ChapterType.path,
                         chap_sel='.liebiao li',
                         tid=tid)
        self.encoding = config.GB
        self.tool = Xs335Tool

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('.infot span').text()
        author = re.match(r'作者：(.*)', st).group(1)
        return name, author
