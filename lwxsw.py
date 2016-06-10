#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.lwxsw.org/books/{}/{}/'
INTRO_URL = 'http://www.lwxsw.org/book/{}/index.html'


class Lwxsw(serial.Novel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         utils.base_to_url(INTRO_URL, tid), '.intro',
                         chap_sel='.bookinfo_td td',
                         chap_type=serial.ChapterType.last)
        self.encoding = const.GB

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'og:novel:author'
        ).attr('content')

        return name, author


def main():
    utils.in_main(Lwxsw, const.GOAGENT)


if __name__ == '__main__':
    main()
