#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.feizw.com/Html/{}/Index.html'
INTRO_URL = 'http://www.feizw.com/Book/{}/Index.aspx'


class FeizwTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend(
            (re.compile(pat, re.I) for pat in
             (r'www.feizw.com 飞速中文网',
              r'最快更新无错小说阅读，请访问www.feizw.com',
              r'手机请访问：http://m.feizw.com'))
        )


class Feizw(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         chap_type=serial.ChapterType.last,
                         chap_sel='.chapterlist li',
                         tid=tid)
        self.encoding = config.GB
        self.tool = FeizwTool

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords').attr('content')
        name = re.match(r'(.*?),.*', st).group(1)

        st = self.doc('span:not([class])').text()
        author = re.match(r'文 / (\S*)', st).group(1)

        return name, author
