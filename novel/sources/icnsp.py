#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import serial, utils

BASE_URL = 'http://www.icnsp.com/plugin.php?id=ysysyan_novel:novel&do=chapter&tid={}'


class Icnsp(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#msgdiv',
                         intro_sel='.noveldes',
                         chap_type=serial.ChapterType.path,
                         chap_sel='.c_chapter td',
                         tid=tid)

    def get_title_and_author(self):
        title = self.doc('.h2_subject').text()
        author = self.doc('.author')('a').text()
        return title, author
