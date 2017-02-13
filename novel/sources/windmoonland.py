#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery

from novel import serial, utils

BASE_URL = 'https://windmoonland.com/stories/{}'


class WindmoonlandPage(serial.Page):

    def get_content(self):
        content = self.doc.html()
        pat = re.compile(r'.*?<hr/>(.*?)<hr/>.*', re.S)
        content = re.match(pat, content).group(1)
        content = self.refine(content)
        return content


class Windmoonland(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         tid=tid)
        self.page = WindmoonlandPage

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'description'
        ).attr('content')
        author, name = re.match('^(.*):(.*)$', st).groups()
        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('td a').map(
            lambda i, e: (i,
                          urljoin(utils.get_base_url(self.url),
                                  PyQuery(e).attr('href')),
                          PyQuery(e).text())
        )
        return clist
