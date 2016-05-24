#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as Pq

from novel import serial, const

BASE_URL = 'http://www.biquge.la/book/%s/'
ENCODING = 'GB18030'


class Biquge(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(BASE_URL % tid, None,
                         None, '#content',
                         const.HEADERS, proxies, ENCODING,
                         chap_sel='dd',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author

    def get_intro(self):
        intro = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:description'
        ).attr('content')
        return intro


def main():
    utils.in_main(Biquge)


if __name__ == '__main__':
    main()
