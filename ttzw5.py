#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.ttzw5.com/book/%s/%s/'
ENCODING = 'GB18030'


class Ttzw(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), None,
                         None, '#contents',
                         serial.HEADERS, proxies, ENCODING,
                         chap_sel='li.zp_li',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)

        st = self.doc('h3').text()
        author = re.match(r'作者：(.*?)/.*', st).group(1)

        return name, author


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Ttzw(tid)
        yq.dump()


if __name__ == '__main__':
    main()
