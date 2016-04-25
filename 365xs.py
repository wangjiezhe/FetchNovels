#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from urllib.parse import urljoin
from pyquery import PyQuery as pq

from novel.serial import Novel, GOAGENT, HEADERS
from novel.utils import base_to_url

BASE_URL = 'http://www.365xs.org/books/%s/%s/'
INTRO_URL = 'http://www.365xs.org/book/%s/index.html'
ENCODING = 'GB18030'


class Xs365(Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '#content',
                         HEADERS, proxies, ENCODING)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: pq(e).attr('name') == 'author').attr('content')
        return re.match(r'(.*)版权属于作者(.*)', st).groups()

    @property
    def chapter_list(self):
        clist = self.doc('.chapterlist')('li').map(
            lambda i, e: (i,
                          urljoin(self.url, pq(e)('a').attr('href')),
                          pq(e).text())
        ).filter(
            lambda i, e: e[1] is not None
        )
        return clist


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Xs365(tid, GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
