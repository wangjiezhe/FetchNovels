#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urljoin

from pyquery import PyQuery
from selenium import webdriver

from novel import serial, utils, config

BASE_URL = 'http://www.piaotian.net/html/{}/{}/'
INTRO_URL = 'http://www.piaotian.net/bookinfo/{}/{}.html'


class PiaotianPage(serial.Page):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encoding = config.GB

    def get_content(self):
        content = self.doc.html()
        pat = re.compile(r'.*<!-- 标题上AD结束 -->(.*)<!-- 翻页上AD开始 -->.*',
                         re.S)
        try:
            content = re.match(pat, content).group(1)
        except AttributeError:
            if 'http' in self.proxies:
                service_args = [
                    '--proxy=' + self.proxies['http'],
                    '--proxy-type=http'
                ]
            else:
                service_args = None
            driver = webdriver.PhantomJS(service_args=service_args)
            driver.get(self.url)
            driver.execute_script('''
                var element = document.querySelector(".toplink");
                if (element)
                    element.parentNode.removeChild(element);
            ''')
            content = driver.find_element_by_id('content').text
            driver.close()
            return content
        content = self.refine(content)
        return content


class PiaotianIntroPageTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.append(
            re.compile(r'.*</span>')
        )


class PiaotianIntroPage(serial.IntroPage):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tool = PiaotianIntroPageTool
        self.encoding = config.GB

    def get_content(self):
        intro = self.doc('div').filter(
            lambda i, e: 'float:left' in (PyQuery(e).attr('style') or '')
        ).html()
        intro = self.refine(intro)
        return intro


class PiaotianTool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend((
            re.compile(r'飘天文学'),
            re.compile(r'www\.piaotian\.com', re.I),
            re.compile(r'&lt;tr&gt;&lt;td&gt;'),
            re.compile(r'&lt;div id="content"&gt;\xa0\xa0\xa0\xa0'),
            re.compile(r'&amp;nbsp'),
            re.compile(r'手机用户请访问http://m\.piaotian\.net'),
        ))


class Piaotian(serial.SerialNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         intro_url=utils.base_to_url(INTRO_URL, tid),
                         tid=tid)
        self.encoding = config.GB
        self.tool = PiaotianTool
        self.page = PiaotianPage
        self.intro_page = PiaotianIntroPage

    def get_title_and_author(self):
        st = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'keywords'
        ).attr('content')
        name = re.match(r'(.*?),.*', st).group(1)
        author = self.doc('meta').filter(
            lambda i, e: PyQuery(e).attr('name') == 'author'
        ).attr('content')
        return name, author

    @property
    def chapter_list(self):
        clist = self.doc('li').filter(
            lambda i, e: (PyQuery(e)('a').attr('href') and
                          re.match(r'\d+\.html', PyQuery(e)('a').attr('href')))
        ).map(
            lambda i, e: (i,
                          urljoin(self.url, PyQuery(e)('a').attr('href')),
                          PyQuery(e).text())
        )
        return clist
