#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

from .. import serial, utils, config

BASE_URL = 'http://www.xianwang123.com/{}/{}/'


class Xianwang123(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#ccontent',
                         None, 'div .gray',
                         chap_sel='.acss td',
                         chap_type=serial.ChapterType.last,
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author
