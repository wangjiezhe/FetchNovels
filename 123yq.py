#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.123yq.org/read/%s/%s/'
INTRO_URL = 'http://www.123yq.org/xiaoshuo_%s.html'
ENCODING = 'GB18030'


class Yq123(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '#TXT',
                         serial.HEADERS, proxies, ENCODING)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*?),(.*?),', st).groups()

    @property
    def chapter_list(self):
        clist = self.doc('dd').filter(
            lambda i, e: Pq(e)('a').attr('href') is not None
        ).map(
            lambda i, e: (utils.fix_order(i),
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
        yq = Yq123(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
