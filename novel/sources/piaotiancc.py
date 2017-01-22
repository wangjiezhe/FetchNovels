#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://tw.piaotian.cc/read/{}/index.html'
INTRO_URL = 'http://tw.piaotian.cc/book/{}.html'


class Piaotiancc(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.novel_content',
                         utils.base_to_url(INTRO_URL, tid), '#description1',
                         chap_type=serial.ChapterType.path,
                         chap_sel='.novel li',
                         tid=tid)
        self.encoding = config.BIG

    def get_title_and_author(self):
        title = self.doc('h1').text()
        author = self.doc('.novel_info')('a').filter(
            lambda i, e: PyQuery(e).attr('target') == '_blank'
        ).text()
        return title, author
