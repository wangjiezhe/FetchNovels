#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.yqhhy.cc/{}/{}/index.html'
INTRO_URL = 'http://www.yqhhy.cc/bookinfo/{}/{}.htm'


class YqhhyTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.append(re.compile(r'更多，尽在言情后花园。请记住本站： www.yqhhy.cc'))


class Yqhhy(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '#desCon1',
                         chap_type=serial.ChapterType.last,
                         chap_sel='#readtext td',
                         tid=tid)
        self.encoding = config.GB
        self.tool = YqhhyTool

    def get_title_and_author(self):
        name = self.doc('h1').text()

        st = self.doc('#info').text()
        author = re.match(r'作者：(.*)', st).group(1)

        return name, author
