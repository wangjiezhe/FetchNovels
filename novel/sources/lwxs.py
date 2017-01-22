#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.lwxs.com/shu/{}/{}/'
INTRO_URL = 'http://www.lwxs.com/info-{}.html'


class Lwxs(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.zhangjieTXT',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         chap_type=serial.ChapterType.last,
                         chap_sel='dd',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        return re.match(r'(.*)最新章节\((.*?)\),.*', st).groups()
