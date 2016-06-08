#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.lwxs.com/shu/{}/{}/'
INTRO_URL = 'http://www.lwxs.com/info-{}.html'


class Lwxs(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.zhangjieTXT',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         const.HEADERS, proxies, const.GB,
                         chap_sel='dd',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords'
        ).attr('content')
        return re.match(r'(.*)最新章节\((.*?)\),.*', st).groups()


def main():
    utils.in_main(Lwxs, const.GOAGENT)


if __name__ == '__main__':
    main()
