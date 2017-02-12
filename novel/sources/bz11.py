#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import urljoin

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.11bz.org/{}_{}/'


class Bz11(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content:eq(1)',
                         intro_sel='#intro',
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

    @property
    def chapter_list(self):
        clist = self.doc('#list')('dt:eq(1)').next_all('dd').filter(
            lambda i, e: PyQuery(e)('a').attr('href')
        ).map(
            lambda i, e: (i,
                          urljoin(utils.get_base_url(self.url),
                                  PyQuery(e)('a').attr('href')),
                          PyQuery(e).text())
        )
        return clist
