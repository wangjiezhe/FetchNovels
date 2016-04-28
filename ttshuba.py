#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.ttshuba.com/shu/%s/%s/'
INTRO_URL = 'http://www.ttshuba.com/info-%s.html'
ENCODING = 'GB18030'


class Ttshuba(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '.zhangjieTXT',
                         serial.HEADERS, proxies, ENCODING,
                         chap_sel='dd',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*)最新章节,(.*?),.*', st).groups()


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Ttshuba(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
