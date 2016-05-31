#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import serial, utils, const

BASE_URL = 'http://www.haxtxt.com/files/article/html/{}/{}/'
ENCODING = 'GB18030'


class Haxtxt(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#BookText',
                         None, '.intro',
                         const.HEADERS, proxies, ENCODING,
                         chap_sel='.chapterlist dd',
                         chap_type=serial.ChapterType.last)

    def get_title_and_author(self):
        title = self.doc('.btitle h1').text().strip('《》')
        author = self.doc('.btitle em a').text()
        return title, author


def main():
    utils.in_main(Haxtxt, const.GOAGENT)


if __name__ == '__main__':
    main()
