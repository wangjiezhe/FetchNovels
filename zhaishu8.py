#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.zhaishu8.com/xiaoshuo/%s/%s/'
INTRO_URL = 'http://www.zhaishu8.com/book/%s/index.aspx'
ENCODING = 'GB18030'


class Zhaishu8Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend(
            [re.compile(r'<h2>.*?</h2>'),
             re.compile(r'完结穿越小说推荐：')]
        )


class Zhaishu8(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '#b_info', '#texts',
                         serial.HEADERS, proxies, ENCODING,
                         tool=Zhaishu8Tool,
                         chap_sel='#BookText li',
                         chap_type=serial.ChapterType.last)

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
        yq = Zhaishu8(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
