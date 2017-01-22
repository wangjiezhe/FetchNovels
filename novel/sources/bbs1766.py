#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.1766bbs.com/{}/{}/'


class Bbs1766(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#htmlContent',
                         intro_sel='.bookinfo_intro',
                         chap_type=serial.ChapterType.last,
                         chap_sel='.book_list li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        author = re.match(r'.*,(.*?)$', st).group(1)
        return name, author
