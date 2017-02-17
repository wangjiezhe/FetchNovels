#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, config, utils

BASE_URL = 'http://www.benbenwx.com/{}_{}/'


class BenbenwxTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend((
            re.compile(r'\( \.\)'),
            re.compile(r'rds\(\);'),
            re.compile(r'^\( \)', re.M),
        ))


class Benbenwx(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='#intro',
                         chap_type=serial.ChapterType.path,
                         chap_sel='#list li',
                         tid=tid)
        self.encoding = config.GB
        self.tool = BenbenwxTool

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author
