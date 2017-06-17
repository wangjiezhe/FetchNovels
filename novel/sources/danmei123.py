#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.123danmei.com/read/{}/'


class Danmei123Tool(utils.Tool):

    def __init__(self):
        super().__init__()

        self.remove_extras.extend(
            (re.compile(pat) for pat in
             (r'本文是龙马\nVIP文 特意购买希望大家喜欢,看龙马vip小说来91耽美网',
              r'本文是龙马\nVIP文 特意购买希望大家喜欢',
              r'如果你喜欢本站一定要记住网址哦~',
              ))
        )


class Danmei123(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='#aboutbook',
                         chap_type=serial.ChapterType.path,
                         chap_sel='dd',
                         tid=tid)
        self.encoding = config.GB
        self.tool = Danmei123Tool

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author
