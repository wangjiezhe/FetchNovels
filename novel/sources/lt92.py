#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.lt92.com/files/article/html/{}/{}/index.html'
INTRO_URL = 'http://www.lt92.com/modules/article/articleinfo.php?id={}'


class Lt92(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#htmlContent',
                         utils.base_to_url(INTRO_URL, tid), 'h3',
                         chap_type=serial.ChapterType.last,
                         chap_sel='#htmlList li',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords').attr('content')
        name = re.match(r'(.*?),.*', st).group(1)

        author = self.doc('h1 span a').text()

        return name, author
