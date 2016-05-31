#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import serial, utils, const

BASE_URL = 'http://2bgif.com/chapters/{}'


class Bgif2(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#content',
                         None, '#description',
                         const.HEADERS, proxies,
                         chap_sel='tbody td',
                         chap_type=serial.ChapterType.path)

    def get_title_and_author(self):
        title = self.doc('.active').text()
        author = self.doc('#author_resume').text()
        return title, author


def main():
    utils.in_main(Bgif2)


if __name__ == '__main__':
    main()
