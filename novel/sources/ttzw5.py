#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.ttzw5.com/book/{}/{}/'


class Ttzw5(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#contents',
                         chap_type=serial.ChapterType.last,
                         chap_sel='li.zp_li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)

        st = self.doc('h3').text()
        author = re.match(r'作者：(.*?)/.*', st).group(1)

        return name, author
