#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import serial, utils, config

BASE_URL = 'http://www.ziyouge.com/zy/{}/{}/index.html'


class Ziyouge(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#htmlContent',
                         chap_type=serial.ChapterType.last,
                         chap_sel='.chapter-list li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('h1').text()
        author = self.doc('.title span a').text()
        return name, author
