#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.69shu.com/{}/'
INTRO_URL = 'http://www.69shu.com/modules/article/jianjie.php?id={}'


class Shu69(serial.Novel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.yd_text2',
                         utils.base_to_url(INTRO_URL, tid), '.jianjie')
        self.encoding = const.GB

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
    utils.in_main(Shu69, const.HEADERS)


if __name__ == '__main__':
    main()
