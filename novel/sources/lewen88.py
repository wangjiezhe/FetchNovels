#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.lewen88.com/{}/{}/'


class Lewen88Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.append(re.compile(r'\(www.lewen88.com\)'))


class Lewen88(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.content-body',
                         tid=tid)
        self.encoding = config.GB
        self.tool = Lewen88Tool

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
        clist = self.doc('.list-charts:first li').filter(
            lambda i, e: PyQuery(e)('a').attr('href')
        ).map(
            lambda i, e: (i,
                          urljoin(utils.get_base_url(self.url),
                                  PyQuery(e)('a').attr('href')),
                          self.refine(PyQuery(e).text()))
        )
        return clist
