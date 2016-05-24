#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.123yq.org/read/%s/%s/'
INTRO_URL = 'http://www.123yq.org/xiaoshuo_%s.html'
ENCODING = 'GB18030'


class Yq123Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.replace_extras.append(
            (re.compile(r'123言情'), '晋江')
        )


class Yq123(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid), INTRO_URL % tid,
                         '.intro', '#TXT',
                         const.HEADERS, proxies, ENCODING,
                         chap_sel='dd',
                         chap_type=serial.ChapterType.last_rev,
                         tool=Yq123Tool)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*?),(.*?),', st).groups()


def main():
    serial.in_main(Yq123, const.GOAGENT)


if __name__ == '__main__':
    main()
