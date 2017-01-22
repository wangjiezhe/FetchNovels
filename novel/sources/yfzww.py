#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils

BASE_URL = 'http://www.yfzww.com/Book/{}'


class YfzwwTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.append(
            re.compile(r'【一凡中文网.*', re.S)
        )


class Yfzww(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         chap_type=serial.ChapterType.path,
                         chap_sel='#chapters li',
                         tid=tid)
        self.tool = YfzwwTool

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
