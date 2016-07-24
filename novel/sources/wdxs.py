#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from .. import serial, utils, config

BASE_URL = 'http://www.wodexiaoshuo.com/{}/chapter.html'
INTRO_URL = 'http://www.wodexiaoshuo.com/{}/'


class WdxsTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend(
            (re.compile(pat, re.I) for pat in
             (r'www\.(wodexiaoshuo|01bz)\.(com|net|wang)',
              r'wodexiaoshuo\.com',
              r'www\.'))
        )
        self.remove_extras.extend(
            (re.compile(pat) for pat in
             (r'\t',
              r'&amp;nbsp;'))
        )


class Wdxs(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.box_box',
                         utils.base_to_url(INTRO_URL, tid), '.j_box .words',
                         chap_sel='.box_box li',
                         chap_type=serial.ChapterType.path,
                         tid=tid)
        self.encoding = config.GB
        self.tool = WdxsTool

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)
        author = self.doc('a').filter(
            lambda i, e: re.match(r'^/author/\?\d+\.html$',
                                  PyQuery(e)('a').attr('href') or '')
        ).attr('title')
        return name, author
