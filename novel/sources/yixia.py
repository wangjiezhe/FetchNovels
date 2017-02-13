#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.yixia.net/book/{}/{}/'


class Yixia(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='.int div',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        author, name = re.match('(.*?)作品免费阅读,(.*?)全文免费阅读,.*', st).groups()
        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('#list a').map(
            lambda i, e: (i,
                          urljoin(self.url,
                                  PyQuery(e).attr('href')),
                          PyQuery(e).text())
        )
        return clist
