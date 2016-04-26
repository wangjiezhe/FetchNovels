#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from urllib.parse import urljoin
from pyquery import PyQuery as pq

from novel import serial, utils

BASE_URL = 'http://www.piaotian.net/html/%s/%s/'
INTRO_URL = 'http://www.piaotian.net/bookinfo/%s/%s.html'
ENCODING = 'GB18030'


class PiaotianPage(serial.Page):

    def get_content(self):
        content = self.doc.html()
        pat = re.compile(r'.*<!-- 标题上AD结束 -->(.*)<!-- 翻页上AD开始 -->.*',
                         re.S)
        content = re.match(pat, content).group(1)
        content = self.tool.replace(content)
        return content


class PiaotianTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self._remove_ex = re.compile(r'GetFont\(\);')

    def replace(self, text):
        text = super().replace(text)
        text = re.sub(self._remove_ex, '', text)
        return text


class Piaotian(serial.Novel):

    def __init__(self, tid, proxies=None):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         utils.base_to_url(INTRO_URL, tid),
                         None, None,
                         serial.HEADERS, proxies, ENCODING,
                         page=PiaotianPage, tool=PiaotianTool)

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: pq(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)
        author = self.doc('meta').filter(
            lambda i, e: pq(e).attr('name') == 'author'
        ).attr('content')
        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('li').filter(
            lambda i, e: re.match(r'\d+\.html', pq(e)('a').attr('href'))
        ).map(
            lambda i, e: (i,
                          urljoin(self.url, pq(e)('a').attr('href')),
                          pq(e).text())
        ).filter(
            lambda i, e: e[1] is not None
        )
        return clist


def main():
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        yq = Piaotian(tid, serial.GOAGENT)
        yq.dump()


if __name__ == '__main__':
    main()