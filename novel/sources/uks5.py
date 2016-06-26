#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

from .. import serial, utils

BASE_URL = 'http://www.5uks.com/book/{}/'


class Uks5Page(serial.Page):

    def get_content(self):
        content = self.doc(self.selector).eq(1).html()
        content = self.refine(content)
        return content


class Uks5(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.box_box',
                         chap_sel='.list_box li',
                         chap_type=serial.ChapterType.path,
                         tid=tid)
        self.page = Uks5Page

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author
