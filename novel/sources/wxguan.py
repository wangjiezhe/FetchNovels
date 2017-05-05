#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.wxguan.com/wenzhang/{}/{}/'


class WxguanTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend((
            re.compile(pat) for pat in (
                r'请记住本书首发域名：www.wxguan.com。',
                r'文学馆手机版阅读网址：m.wxguan.com',
                r'无弹窗推荐地址：\S*',
                r'http://www.wxguan.com/wenzhang/\S*html',
            )
        ))


class Wxguan(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         intro_sel='.intro',
                         tid=tid)
        self.encoding = config.GB
        self.tool = WxguanTool

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('.listmain')('dt:eq(1)').next_all('dd').filter(
            lambda i, e: PyQuery(e)('a').attr('href')
        ).map(
            lambda i, e: (i,
                          urljoin(utils.get_base_url(self.url),
                                  PyQuery(e)('a').attr('href')),
                          PyQuery(e).text())
        )
        return clist
