#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import serial, utils

BASE_URL = 'http://www.quanben5.com/n/{}/xiaoshuo.html'


class Quanben5(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='.description',
                         chap_type=serial.ChapterType.path,
                         chap_sel='.list li',
                         tid=tid)

    def get_title_and_author(self):
        name = self.doc('h1').text()
        author = self.doc('.author').text()
        return name, author
