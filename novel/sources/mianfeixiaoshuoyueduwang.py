#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils

BASE_URL = 'http://www.mianfeixiaoshuoyueduwang.com/book/{}/'


class Mianfeixiaoshuoyueduwang(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='.description',
                         chap_type=serial.ChapterType.path,
                         chap_sel='.list li',
                         tid=tid)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*?),(.*?),.*', st).groups()
