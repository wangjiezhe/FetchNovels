#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import serial, utils, config

BASE_URL = 'http://www.akxs6.com/{}/{}/'
INTRO_URL = 'http://www.akxs6.com/book/{}.html'


class Akxs6(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '#bookintro',
                         chap_type=serial.ChapterType.path,
                         chap_sel='#readerlist li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('h1').text()
        author = self.doc('#smallcons span a').text()
        return name, author
