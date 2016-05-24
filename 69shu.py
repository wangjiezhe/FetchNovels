#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.69shu.com/%s/'
INTRO_URL = 'http://www.69shu.com/modules/article/jianjie.php?id=%s'
ENCODING = 'GB18030'


class Shu69(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(BASE_URL % tid, INTRO_URL % tid,
                         '.jianjie', '.yd_text2',
                         const.HEADERS, proxies, ENCODING)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)
        author = self.doc('.mu_beizhu').eq(0)('a').eq(1).text()
        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('.mulu_list').eq(1)('li').filter(
            lambda i, e: Pq(e)('a').attr('href')
        ).map(
            lambda i, e: (i,
                          urljoin(utils.get_base_url(self.url),
                                  Pq(e)('a').attr('href')),
                          Pq(e).text())
        )
        return clist


def main():
    serial.in_main(Shu69, const.HEADERS)


if __name__ == '__main__':
    main()
