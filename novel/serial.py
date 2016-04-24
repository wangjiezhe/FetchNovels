#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from time import sleep
from pyquery import PyQuery as pq

from .decorators import retry
from .utils import Tool
from .error import *

GOAGENT = {'http': '127.0.0.1:8087'}
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36'}


class Novel(object):

    def __init__(self, url, intro_url,
                 intro_sel, cont_sel,
                 headers=None, proxies=None, encoding=None):
        self.url = url
        self.intro_url = intro_url
        self.intro_sel = intro_sel
        self.cont_sel = cont_sel
        self.headers = headers or {}
        self.proxies = proxies or {}
        self.encoding = encoding
        self.tool = Tool()

        self.doc = pq(self.url, headers=self.headers, proxies=self.proxies,
                      encoding=self.encoding)
        self.title, self.author = self.get_title_and_author()

    def get_title_and_author(self):
        raise MethodNotSetError(sys._getframe().f_code.co_name)

    @property
    def chapter_list(self):
        raise PropertyNotSetError(sys._getframe().f_code.co_name)

    def get_intro(self):
        try:
            intro_page = IntroPage(self.intro_url, self.intro_sel,
                                   self.headers, self.proxies, self.encoding)
            intro = intro_page.get_content()
            return intro
        except HTTPError:
            print("Wait 5s to retry...")
            sleep(5)
            return self.get_intro()

    @property
    def download_dir(self):
        return os.path.join(os.getcwd(), "《%s》%s" % (self.title, self.author))

    def dump_split(self):
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir)
        print('《%s》%s' % (self.title, self.author))
        for i, url, title in self.chapter_list:
            self.dump_chapter(url, title, i + 1)

    @retry(HTTPError)
    def dump_chapter(self, url, title, num):
        page = Page(url, title, self.cont_sel,
                    self.headers, self.proxies, self.encoding)
        page.dump(folder=self.download_dir, num=num)

    def dump(self):
        name = '《%s》%s.txt' % (self.title, self.author)
        print(name)
        path = os.path.join(os.getcwd(), name)
        with open(path, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n')
            fp.write(self.author)
            fp.write('\n\n\n')
            fp.write(self.get_intro())
            for _, url, title in self.chapter_list:
                content = self.get_chapter(url, title)
                fp.write('\n\n\n\n')
                print(title)
                fp.write(title)
                fp.write('\n\n\n')
                fp.write(content)
                fp.write('\n')

    @retry(HTTPError)
    def get_chapter(self, url, title):
        page = Page(url, title, self.cont_sel,
                    self.headers, self.proxies, self.encoding)
        return page.get_content()


class Page(object):

    def __init__(self, url, title, selector,
                 headers=None, proxies=None, encoding=None):
        self.url = url
        self.title = title
        self.selector = selector
        self.headers = headers or {}
        self.proxies = proxies or {}
        self.encoding = encoding
        self.tool = Tool()

        self.doc = pq(self.url, headers=self.headers, proxies=self.proxies,
                      encoding=self.encoding)

    def get_content(self):
        content = self.doc(self.selector).html()
        content = self.tool.replace(content)
        return content

    def dump(self, path=None, folder=None, num=None):
        if path is None:
            if num is not None:
                pre = '「%d」' % num
            else:
                pre = ''
            name = '%s%s.txt' % (pre, self.title)
            if folder is None:
                path = os.path.join(os.getcwd(), name)
            else:
                path = os.path.join(folder, name)
        print(self.title)
        with open(path, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n')
            fp.write(self.get_content())


class IntroPage(object):

    def __init__(self, url, selector,
                 headers=None, proxies=None, encoding=None):
        self.url = url
        self.headers = headers or {}
        self.proxies = proxies or {}
        self.encoding = encoding
        self.selector = selector
        self.tool = Tool()

        self.doc = pq(self.url, headers=self.headers, proxies=self.proxies,
                      encoding=self.encoding)

    def get_content(self):
        intro = self.doc(self.selector).html()
        intro = self.tool.replace(intro)
        return intro
