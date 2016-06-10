#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.ranwen.org/files/article/{}/{}/'


class Ranwen(serial.Novel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         chap_sel='dd',
                         chap_type=serial.ChapterType.whole)
        self.encoding = const.GB

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author


def main():
    utils.in_main(Ranwen, const.GOAGENT)


if __name__ == '__main__':
    main()
