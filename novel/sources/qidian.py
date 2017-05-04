#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import serial, utils

BASE_URL = 'https://book.qidian.com/info/{}#Catalog'


class Qidian(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.read-content',
                         intro_sel='.intro',
                         chap_type=serial.ChapterType.noscheme,
                         chap_sel='.volume-wrap li',
                         tid=tid)

    def get_title_and_author(self):
        name = self.doc('h1 em').text()
        author = self.doc('.writer').text()
        return name, author
