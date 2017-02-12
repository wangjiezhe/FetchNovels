#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.69shu.com/{}/'
INTRO_URL = 'http://www.69shu.com/modules/article/jianjie.php?id={}'


class Shu69(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.yd_text2',
                         utils.base_to_url(INTRO_URL, tid), '.jianjie',
                         tid=tid)
        self.encoding = config.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)
        author = self.doc('.mu_beizhu:eq(0)')('a:eq(1)').text()
        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('.mu_contain:eq(1)')('.mulu_list:last').prev_all('.mulu_list')('li').filter(
            lambda i, e: PyQuery(e)('a').attr('href')
        ).map(
            lambda i, e: (i,
                          urljoin(utils.get_base_url(self.url),
                                  PyQuery(e)('a').attr('href')),
                          PyQuery(e).text())
        )
        return clist
