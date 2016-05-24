#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.wodexiaoshuo.com/%s/chapter.html'
INTRO_URL = 'http://www.wodexiaoshuo.com/%s/'
ENCODING = 'GB18030'


class WdxsTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend(
            [re.compile(pat, re.I) for pat in
             [r'www\.(wodexiaoshuo|01bz)\.(com|net|wang)',
              r'wodexiaoshuo\.com',
              r'www\.']]
        )
        self.remove_extras.extend(
            [re.compile(pat) for pat in
             [r'\t',
              r'&amp;nbsp;']]
        )


class Wdxs(serial.Novel):

    def __init__(self, tid, proxies=None):
        self.tid = str(tid)
        super().__init__(BASE_URL % tid, INTRO_URL % tid,
                         '.j_box .words', '.box_box',
                         const.HEADERS, proxies, ENCODING,
                         tool=WdxsTool,
                         chap_sel='.box_box li',
                         chap_type=serial.ChapterType.path)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)
        author = self.doc('a').filter(
            lambda i, e: re.match(r'^/author/\?\d+\.html$',
                                  Pq(e)('a').attr('href') or '')
        ).attr('title')
        return name, author


def main():
    serial.in_main(Wdxs, const.GOAGENT)


if __name__ == '__main__':
    main()
