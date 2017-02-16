#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, config, utils

BASE_URL = 'http://www.biqugex.com/book_{}/'


class BiqugexTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.append(
            re.compile(r'一秒记住【笔.*?趣.*?阁 www.biqugex.com】，精彩小说无弹窗免费阅读！', re.I)
        )


class Biqugex(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         chap_type=serial.ChapterType.last,
                         chap_sel='dd',
                         tid=tid)
        self.encoding = config.GB
        self.tool = BiqugexTool

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
