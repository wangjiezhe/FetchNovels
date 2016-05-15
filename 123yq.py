#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.123yq.org/read/%s/%s/'
INTRO_URL = 'http://www.123yq.org/xiaoshuo_%s.html'
ENCODING = 'GB18030'


class Yq123Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.replace_extras.append(
            (re.compile(r'123言情'), '晋江')
        )


class Yq123(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '#TXT',
                         serial.HEADERS, proxies, ENCODING,
                         chap_sel='dd',
                         chap_type=serial.ChapterType.last_rev,
                         tool=Yq123Tool)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*?),(.*?),', st).groups()


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
