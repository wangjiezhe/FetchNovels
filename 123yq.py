#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re

from pyquery import PyQuery as pq

from novel.serial import Novel, GOAGENT, HEADERS
from novel.utils import fix_order, base_to_url

BASE_URL = 'http://www.123yq.org/read/%s/%s/'
INTRO_URL = 'http://www.123yq.org/xiaoshuo_%s.html'
ENCODING = 'GB18030'


class Yq123(Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '#TXT',
                         HEADERS, proxies, ENCODING)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: pq(e).attr['name'] == 'keywords').attr['content']
        return re.match(r'(.*?),(.*?),', st).groups()

    @property
    def chapter_list(self):
        clist = self.doc('dd').map(
            lambda i, e: (fix_order(i),
                          pq(e)('a').attr['href'],
                          pq(e).text())
        ).filter(
            lambda i, e: e[1] is not None
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
        yq = Yq123(tid, GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
