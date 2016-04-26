#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
from urllib.parse import urljoin
from pyquery import PyQuery as Pq

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
        content = self.tool().replace(content)
        return content


class PiaotianTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self._remove_exs = (
            re.compile(r'&lt;tr&gt;&lt;td&gt;'),
            re.compile(r'&lt;div id="content"&gt;\xa0\xa0\xa0\xa0'))

    def replace(self, text):
        for pat in self._remove_exs:
            text = re.sub(pat, '', text)
        text = super().replace(text)
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
            lambda i, e: Pq(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)
        author = self.doc('meta').filter(
            lambda i, e: Pq(e).attr('name') == 'author'
        ).attr('content')
        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('li').filter(
            lambda i, e: (Pq(e)('a').attr('href') and
                          re.match(r'\d+\.html', Pq(e)('a').attr('href')))
        ).map(
            lambda i, e: (i,
                          urljoin(self.url, Pq(e)('a').attr('href')),
                          Pq(e).text())
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
