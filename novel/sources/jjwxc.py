#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.jjwxc.net/onebook.php?novelid={}'


class Jjwxc(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.noveltext',
                         intro_sel='#novelintro',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'Keywords'
        ).attr('content')
        author, name = re.match(r'(.*?),(.*?),', st).groups()
        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('tr').filter(
            lambda i, e: (PyQuery(e).attr('itemprop') and
                          'chapter' in PyQuery(e).attr('itemprop'))
        )('div').filter(
            lambda i, e: PyQuery(e).attr('style') == 'float:left'
        ).map(
            lambda i, e: (i,
                          PyQuery(e)('a').attr('href'),
                          PyQuery(e).text())
        )
        return clist
