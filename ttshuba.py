#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.ttshuba.com/shu/{}/{}/'
INTRO_URL = 'http://www.ttshuba.com/info-{}.html'


class Ttshuba(serial.Novel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '.zhangjieTXT',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         chap_sel='dd',
                         chap_type=serial.ChapterType.last)
        self.encoding = const.GB

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords'
        ).attr('content')
        return re.match(r'(.*)最新章节,(.*?),.*', st).groups()


def main():
    utils.in_main(Ttshuba, const.GOAGENT)


if __name__ == '__main__':
    main()
