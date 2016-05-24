#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.lwxsw.org/books/%s/%s/'
INTRO_URL = 'http://www.lwxsw.org/book/%s/index.html'
ENCODING = 'GB18030'


class Lwxsw(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '#content',
                         const.HEADERS, proxies, ENCODING,
                         chap_sel='.bookinfo_td td',
                         chap_type=serial.ChapterType.last)

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
