#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery

from novel import serial, utils, config

BASE_URL = 'http://www.wodexiaoshuo123.com/{}/chapter.html'
INTRO_URL = 'http://www.wodexiaoshuo123.com/{}/'


class WdxsTool(utils.Tool):

    def __init__(self):
        super().__init__(remove_div=False, remove_font=False)

        self.remove_extras.extend(
            (re.compile(pat) for pat in
             (r'本文是龙马\nVIP文 特意购买希望大家喜欢,看龙马vip小说来91耽美网',
              r'本文是龙马\nVIP文 特意购买希望大家喜欢',
              '看特色销售就来我的小说网-',
              ))
        )

        self.remove_extras.extend(
            (re.compile(pat, re.I) for pat in
             (r'看.*?小.*?说.*?就.*?来.*?w.*?o.*?d.*?e.*?x.*?i.*?a.*?o.*?s.*?h.*?u.*?o.*?c.*?o.*?m',
              r'w.*?w.*?w.*?w.*?o.*?d.*?e.*?x.*?i.*?a.*?o.*?s.*?h.*?u.*?o.*?(c.*?o.*?m|n.*?e.*?t)',
              r'w.*?w.*?w.*?0.*?1.*?b.*?z.*?(c.*?o.*?m|n.*?e.*?t|w.*?a.*?n.*?g)',
              r'(w.*?w.*?w|m).*?9.*?1.*?d.*?a.*?n.*?m.*?e.*?i.*?(c.*?o.*?m|n.*?e.*?t)',
              r'w.*?o.*?d.*?e.*?x.*?i.*?a.*?o.*?s.*?h.*?u.*?o.*?c.*?o.*?m',
              r'9.*?1.*?d.*?a.*?n.*?m.*?e.*?i.*?(c.*?o.*?m|n.*?e.*?t)',
              r'w.*?w.*?w.*?\.',
              ))
        )
        self.remove_extras.extend(
            (re.compile(pat) for pat in
             (r'\t',
              r'&amp;nbsp;'))
        )


class Wdxs(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.box_box',
                         utils.base_to_url(INTRO_URL, tid), '.j_box .words',
                         chap_type=serial.ChapterType.path,
                         chap_sel='.box_box li',
                         tid=tid)
        self.encoding = config.GB
        self.tool = WdxsTool

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)
        author = self.doc('a').filter(
            lambda i, e: re.match(r'^/author/\?\d+\.html$',
                                  PyQuery(e)('a').attr('href') or '')
        ).attr('title')
        return name, author
