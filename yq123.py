#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.123yq.org/read/{}/{}/'


class Yq123Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.replace_extras.append(
            (re.compile(r'123言情'), '晋江')
        )


class Yq123(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), '#TXT',
                         None, '.introtxt',
                         chap_sel='dd',
                         chap_type=serial.ChapterType.last_rev,
                         tid=tid)
        self.encoding = const.GB
        self.tool = Yq123Tool

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'keywords').attr('content')
        return re.match(r'(.*?),(.*?),', st).groups()


def main():
    utils.in_main(Yq123, const.GOAGENT)


if __name__ == '__main__':
    main()
