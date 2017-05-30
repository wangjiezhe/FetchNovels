#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.tangzhekan3.com/{}/{}/'


class Tangzhekan3Tool(utils.Tool):

    def __init__(self):
        super().__init__(remove_div=False, remove_font=False)


class Tangzhekan3(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.box_box',
                         intro_sel='.j_box .words p',
                         chap_type=serial.ChapterType.last,
                         chap_sel='.list_box li',
                         tid=tid)
        self.encoding = config.GB
        self.tool = Tangzhekan3Tool

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'description'
        ).attr('content')
        pat = re.compile(r'(.*)的新书(.*)最新章节.*')
        author, name = re.match(pat, st).groups()

        return name, author
