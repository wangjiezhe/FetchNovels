#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.365xs.org/books/{}/{}/'
INTRO_URL = 'http://www.365xs.org/book/{}/index.html'
ENCODING = 'GB18030'


class Xs365(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         utils.base_to_url(INTRO_URL, tid),
                         '.intro', '#content',
                         const.HEADERS, proxies, ENCODING,
                         chap_sel='.chapterlist li',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'author').attr('content')
        return re.match(r'(.*)版权属于作者(.*)', st).groups()


def main():
    utils.in_main(Xs365, const.GOAGENT)


if __name__ == '__main__':
    main()
