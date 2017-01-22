#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.zhaishu8.com/xiaoshuo/{}/{}/'
INTRO_URL = 'http://www.zhaishu8.com/book/{}/index.aspx'


class Zhaishu8Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend((
            re.compile(r'<h2>.*?</h2>'),
            re.compile(r'完结穿越小说推荐：')
        ))


class Zhaishu8(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#texts',
                         utils.base_to_url(INTRO_URL, tid), '#b_info',
                         chap_type=serial.ChapterType.last,
                         chap_sel='#BookText li',
                         tid=tid)
        self.encoding = config.GB
        self.tool = Zhaishu8Tool

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*?),(.*?),', st).groups()
