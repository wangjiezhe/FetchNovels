#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.lwxsw.org/books/%s/%s/'
INTRO_URL = 'http://www.lwxsw.org/book/%s/index.html'
ENCODING = 'GB18030'


class Lwxsw(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '#content',
                         serial.HEADERS, proxies, ENCODING,
                         chap_sel='.bookinfo_td td',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'og:novel:author'
        ).attr('content')

        return name, author


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Lwxsw(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
