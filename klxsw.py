#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from urllib.parse import urljoin

from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.klxsw.com/files/article/html/%s/%s/'
ENCODING = 'GB18030'


class Klxsw(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), None,
                         None, '#r1c',
                         serial.HEADERS, proxies, ENCODING)

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author

    def get_intro(self):
        intro = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:description'
        ).attr('content')
        return intro

    @property
    def chapter_list(self):
        clist = self.doc('div').filter(
            lambda i, e: Pq(e).attr('align') == 'left'
        ).filter(
            lambda i, e: Pq(e)('a').attr('href')
        ).map(
            lambda i, e: (i,
                          urljoin(self.url, Pq(e)('a').attr('href').strip()),
                          Pq(e).text())
        )
        return clist


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Klxsw(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
