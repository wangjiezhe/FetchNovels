#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.33yq.com/read/{}/{}/'


class Yq33Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.replace_extras.append(
            (re.compile(r'123言情'), '晋江')
        )


class Yq33(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#TXT',
                         intro_sel='.introtxt',
                         tid=tid)
        self.encoding = config.GB
        self.tool = Yq33Tool

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*?),(.*?),', st).groups()

    @property
    def chapter_list(self):
        clist = self.doc('dd').map(
            lambda i, e: (utils.fix_order(i),
                          PyQuery(e)('a').attr('href'),
                          PyQuery(e).text())
        ).filter(
            lambda i, e: e[1]
        )
        clist.sort()
        return clist
