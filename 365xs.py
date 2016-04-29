#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.365xs.org/books/%s/%s/'
INTRO_URL = 'http://www.365xs.org/book/%s/index.html'
ENCODING = 'GB18030'


class Xs365(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '#content',
                         serial.HEADERS, proxies, ENCODING,
                         chap_sel='.chapterlist li',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'author').attr('content')
        return re.match(r'(.*)版权属于作者(.*)', st).groups()


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Xs365(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
