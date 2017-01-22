#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery
from selenium import webdriver

from novel import serial, utils

BASE_URL = 'http://www.aastory.xyz/archive.php?id={}'


class AastoryPage(serial.Page):

    def get_content(self):
        driver = webdriver.PhantomJS()
        driver.get(self.url)
        content = driver.find_element_by_id('chapter_content').text
        driver.close()
        return content


class Aastory(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         chap_type=serial.ChapterType.path,
                         chap_sel='li',
                         tid=tid)
        self.page = AastoryPage

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('.index_info').text()
        author = re.match(r'作者：(.*)', st).group(1)
        return name, author

    def get_intro(self):
        intro = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'Description'
        ).attr('content')
        return intro
