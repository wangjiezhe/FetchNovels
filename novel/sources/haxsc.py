#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from pyquery import PyQuery
from novel import serial, utils, config

BASE_URL = 'http://www.haxsc.com/files/article/html/{}/{}/index.html'
INTRO_URL = 'http://www.haxsc.com/files/article/info/{}/{}.htm'


class Haxsc(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#BookText',
                         utils.base_to_url(INTRO_URL, tid), '.book-intro',
                         chap_type=serial.ChapterType.last,
                         chap_sel='.chapterlist dd',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        author, name = re.match(r'(.*?)，(.*?)全文.*', st).groups()
        return name, author
