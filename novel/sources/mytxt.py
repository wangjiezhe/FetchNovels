#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.mytxt.cc/read/{}/'


class Mytxt(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.detail_con_m62topxs',
                         chap_type=serial.ChapterType.last,
                         chap_sel='.story_list_m62topxs li',
                         intro_sel='#intro_m62topxs',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'og:novel:author'
        ).attr('content')

        return name, author
