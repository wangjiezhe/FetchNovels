#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from pyquery import PyQuery as Pq

from novel import serial, error

BASE_URL = 'http://www.sto.cc/%s-1/'
PAGE_URL = 'http://www.sto.cc/%s-%s/'


class Sto(serial.Novel):

    def __init__(self, tid, proxies=None):
        self.tid = str(tid)
        super().__init__(BASE_URL % self.tid, None,
                         None, '#BookContent',
                         serial.HEADERS, proxies)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords'
        ).attr('content')
        return re.match(r'(.*?),(.*?),.*', st).groups()

    @property
    def chapter_list(self):
        st = re.search(r'ANP_goToPage\("Page_select",(\d+),(\d+),1\);', self.doc.html())
        if st.group(1) == self.tid:
            page_num = int(st.group(2))
        else:
            raise error.Error('Something strange may happened.')
        return [(i+1, PAGE_URL % (self.tid, i+1), '第%d頁' % (i+1)) for i in range(page_num)]


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Sto(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
