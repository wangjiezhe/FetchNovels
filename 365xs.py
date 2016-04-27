#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from urllib.parse import urljoin
from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.365xs.org/books/%s/%s/'
INTRO_URL = 'http://www.365xs.org/book/%s/index.html'
ENCODING = 'GB18030'


class Xs365(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '#content',
                         serial.HEADERS, proxies, ENCODING)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'author').attr('content')
        return re.match(r'(.*)版权属于作者(.*)', st).groups()

    @property
    def chapter_list(self):
        clist = self.doc('.chapterlist')('li').filter(
            lambda i, e: Pq(e)('a').attr('href') is not None
        ).map(
            lambda i, e: (i,
                          urljoin(self.url, Pq(e)('a').attr('href')),
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
        yq = Xs365(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
