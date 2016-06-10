#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery as Pq

from novel import serial, utils, const

BASE_URL = 'http://www.piaotian.net/html/{}/{}/'
INTRO_URL = 'http://www.piaotian.net/bookinfo/{}/{}.html'


class PiaotianPage(serial.Page):

    def get_content(self):
        content = self.doc.html()
        pat = re.compile(r'.*<!-- 标题上AD结束 -->(.*)<!-- 翻页上AD开始 -->.*',
                         re.S)
        content = re.match(pat, content).group(1)
        content = self.tool().refine(content)
        return content


class PiaotianIntroPageTool(serial.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.append(
            re.compile(r'.*</span>')
        )


class PiaotianIntroPage(serial.IntroPage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tool = PiaotianIntroPageTool

    def get_content(self):
        intro = self.doc('div').filter(
            lambda i, e: 'float:left' in (Pq(e).attr('style') or '')
        ).html()
        intro = self.tool().refine(intro)
        return intro


class PiaotianTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend((
            re.compile(r'飘天文学'),
            re.compile(r'www\.piaotian\.com', re.I),
            re.compile(r'&lt;tr&gt;&lt;td&gt;'),
            re.compile(r'&lt;div id="content"&gt;\xa0\xa0\xa0\xa0'),
            re.compile(r'&amp;nbsp')
        ))


class Piaotian(serial.Novel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid), None,
                         utils.base_to_url(INTRO_URL, tid), None)
        self.encoding = const.GB
        self.tool = PiaotianTool
        self.page = PiaotianPage
        self.intro_page = PiaotianIntroPage

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
    utils.in_main(Piaotian, const.GOAGENT)


if __name__ == '__main__':
    main()
