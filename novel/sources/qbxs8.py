#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.qbxs8.net/partlist/{}/{}/index.shtml'
INTRO_URL = 'http://www.qbxs8.net/book.asp?id={}'


class Qbxs8Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend(
            re.compile(pat) for pat in (
                '全本小说吧：www..net 千万别记错哦！手机访问m.qbxs8.net',
                '全本小说吧www.qbxs8.com',
                '看完记得：方便下次看，或者。',
            )
        )


class Qbxs8(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.text',
                         utils.base_to_url(INTRO_URL, tid), '.info .it:first',
                         chap_type=serial.ChapterType.last,
                         chap_sel='.list li',
                         tid=tid)
        self.encoding = config.GB
        self.tool = Qbxs8Tool

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author
