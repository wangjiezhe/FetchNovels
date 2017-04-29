#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import serial, utils, config

BASE_URL = 'http://www.wodexiaoshuo.cc/{}/{}/'
INTRO_URL = 'http://www.wodexiaoshuo.cc/book/{}.html'


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
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         chap_type=serial.ChapterType.path,
                         chap_sel='.liebiao li',
                         tid=tid)
        self.encoding = config.GB
        self.tool = WdxsTool

    def get_title_and_author(self):
        name = self.doc('h1').text()
        st = self.doc('.infot span').text()
        author = re.match(r'作者：(.*)', st).group(1)
        return name, author
