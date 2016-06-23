#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import urljoin

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.klxsw.com/files/article/html/{}/{}/'


class Klxsw(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#r1c',
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

    def get_intro(self):
        intro = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:description'
        ).attr('content')
        return intro

    @property
    def chapter_list(self):
        clist = self.doc('div').filter(
            lambda i, e: PyQuery(e).attr('align') == 'left'
        ).filter(
            lambda i, e: PyQuery(e)('a').attr('href')
        ).map(
            lambda i, e: (i,
                          urljoin(self.url,
                                  PyQuery(e)('a').attr('href').strip()),
                          PyQuery(e).text())
        )
        return clist
