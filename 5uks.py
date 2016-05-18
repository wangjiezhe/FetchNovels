#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from pyquery import PyQuery as Pq

from novel import serial

BASE_URL = 'http://www.5uks.com/book/%s/'


class Uks5Page(serial.Page):

    def get_content(self):
        content = self.doc(self.selector).eq(1).html()
        content = self.tool().refine(content)
        return content


class Uks5(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(BASE_URL % tid, None,
                         None, '.box_box',
                         serial.HEADERS, proxies,
                         chap_sel='.list_box li',
                         chap_type=serial.ChapterType.path,
                         page=Uks5Page)

    def get_title_and_author(self):
        name = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:book_name'
        ).attr('content')

        author = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('property') == 'og:novel:author'
        ).attr('content')

        return name, author


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Uks5(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()
