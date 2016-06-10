#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.zhaishu8.com/xiaoshuo/{}/{}/'
INTRO_URL = 'http://www.zhaishu8.com/book/{}/index.aspx'


class Zhaishu8Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend((
            re.compile(r'<h2>.*?</h2>'),
            re.compile(r'完结穿越小说推荐：')
        ))


class Zhaishu8(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#texts',
                         utils.base_to_url(INTRO_URL, tid), '#b_info',
                         chap_sel='#BookText li',
                         chap_type=serial.ChapterType.last)
        self.encoding = const.GB
        self.tool = Zhaishu8Tool

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*?),(.*?),', st).groups()


def main():
    utils.in_main(Zhaishu8, const.GOAGENT)


if __name__ == '__main__':
    main()
