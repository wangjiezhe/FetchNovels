#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import urljoin

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.klxsw.com/files/article/html/{}/{}/'
ENCODING = 'GB18030'


class Klxsw(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#r1c',
                         headers=const.HEADERS, proxies=proxies,
                         encoding=ENCODING)

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

    @property
    def chapter_list(self):
        clist = self.doc('div').filter(
            lambda i, e: Pq(e).attr('align') == 'left'
        ).filter(
            lambda i, e: Pq(e)('a').attr('href')
        ).map(
            lambda i, e: (i,
                          urljoin(self.url, Pq(e)('a').attr('href').strip()),
                          Pq(e).text())
        )
        return clist


def main():
    utils.in_main(Klxsw, const.GOAGENT)


if __name__ == '__main__':
    main()
