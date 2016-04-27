#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.ranwen.org/files/article/%s/%s/'
ENCODING = 'GB18030'


class Ranwen(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), None,
                         None, '#content',
                         serial.HEADERS, proxies, ENCODING)

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('dd').filter(
            lambda i, e: Pq(e)('a').attr('href') is not None
        ).map(
            lambda i, e: (i,
                          Pq(e)('a').attr('href'),
                          Pq(e).text())
        )
        clist.sort(key=lambda s: int(s[0]))
        return clist


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Ranwen(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
