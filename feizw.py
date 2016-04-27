#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from urllib.parse import urljoin
from pyquery import PyQuery as Pq

from novel import serial, utils

BASE_URL = 'http://www.feizw.com/Html/%s/Index.html'
INTRO_URL = 'http://www.feizw.com/Book/%s/Index.aspx'


class FeizwTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend(
            [re.compile(pat) for pat in
             [r'[Ww]ww.feizw.co[Mm] 飞速中文网',
              r'最快更新无错小说阅读，请访问www.feizw.com',
              r'手机请访问：http://m.feizw.com']]
        )


class Feizw(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(BASE_URL % tid, INTRO_URL % tid,
                         '.intro', '#content',
                         serial.HEADERS, proxies,
                         tool=FeizwTool)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords').attr('content')
        name = re.match(r'(.*?),.*', st).group(1)

        st = self.doc('span:not([class])').text()
        author = re.match(r'文 / (\S*)', st).group(1)

        return name, author

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
        yq = Feizw(tid)
        yq.dump()


if __name__ == '__main__':
    main()
