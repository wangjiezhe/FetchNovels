#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from enum import Enum
from urllib.error import HTTPError
from urllib.parse import urljoin

from lxml.etree import XMLSyntaxError
from pyquery import PyQuery as Pq

from .decorators import retry
from .error import PropertyNotSetError, MethodNotSetError, ValueNotSetError
from .utils import Tool, get_base_url, fix_order


class Page(object):

    def __init__(self, url, title, selector,
                 headers=None, proxies=None, encoding=None,
                 tool=Tool):
        self.url = url
        self.title = title
        self.selector = selector
        self.headers = headers or {}
        self.proxies = proxies or {}
        self.encoding = encoding
        self.tool = tool

        self.doc = self.get_doc()

    @retry((HTTPError, XMLSyntaxError))
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_content(self):
        if self.selector is None:
            return ''
        content = self.doc(self.selector).html()
        content = self.tool().refine(content)
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
                 headers=None, proxies=None, encoding=None,
                 tool=Tool):
        self.url = url
        self.headers = headers or {}
        self.proxies = proxies or {}
        self.encoding = encoding
        self.selector = selector
        self.tool = tool

        self.doc = self.get_doc()

    @retry((HTTPError, XMLSyntaxError))
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_content(self):
        if self.selector is None:
            return ''
        intro = self.doc(self.selector).html()
        intro = self.tool().refine(intro)
        return intro


class ChapterType(Enum):
    whole = 1
    path = 2
    last = 3
    last_rev = 4


class Novel(object):

    def __init__(self, url, intro_url,
                 intro_sel, cont_sel,
                 headers=None, proxies=None, encoding=None,
                 page=Page, intro_page=IntroPage, tool=Tool,
                 chap_sel=None, chap_type=None):
        self.url = url
        self.intro_url = intro_url
        self.intro_sel = intro_sel
        self.cont_sel = cont_sel
        self.headers = headers or {}
        self.proxies = proxies or {}
        self.encoding = encoding
        self.page = page
        self.intro_page = intro_page
        self.tool = tool
        self.chap_sel = chap_sel
        self.chap_type = chap_type

        self.doc = self.get_doc()
        self.title, self.author = self.get_title_and_author()

    @retry((HTTPError, XMLSyntaxError))
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_title_and_author(self):
        raise MethodNotSetError('get_title_and_author')

    @property
    def chapter_list(self):
        if self.chap_sel and self.chap_type:
            return self.chapter_list_with_sel(self.chap_sel, self.chap_type)
        raise PropertyNotSetError('chapter_list')

    def chapter_list_with_sel(self, selector, chap_type):
        clist = self.doc(selector).filter(
            lambda i, e: Pq(e)('a').attr('href')
        )
        if chap_type == ChapterType.whole:
            clist = clist.map(
                lambda i, e: (i,
                              Pq(e)('a').attr('href'),
                              Pq(e).text())
            )
        elif chap_type == ChapterType.path:
            clist = clist.map(
                lambda i, e: (i,
                              urljoin(get_base_url(self.url),
                                      Pq(e)('a').attr('href')),
                              Pq(e).text())
            )
        elif chap_type == ChapterType.last:
            clist = clist.map(
                lambda i, e: (i,
                              urljoin(self.url, Pq(e)('a').attr('href')),
                              Pq(e).text())
            )
        elif chap_type == ChapterType.last_rev:
            clist = clist.map(
                lambda i, e: (fix_order(i),
                              urljoin(self.url, Pq(e)('a').attr('href')),
                              Pq(e).text())
            )
            clist.sort(key=lambda s: int(s[0]))
        else:
            raise ValueNotSetError("chap_type")
        return clist

    @retry(HTTPError)
    def get_intro(self):
        if self.intro_url is None:
            if self.intro_sel is None:
                return ''
            intro = self.doc(self.intro_sel).html()
            intro = self.tool().refine(intro)
            return intro
        else:
            intro_page = self.intro_page(self.intro_url, self.intro_sel,
                                         self.headers, self.proxies, self.encoding,
                                         self.tool)
            intro = intro_page.get_content()
            return intro

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
        page = self.page(url, title, self.cont_sel,
                         self.headers, self.proxies, self.encoding,
                         self.tool)
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
        page = self.page(url, title, self.cont_sel,
                         self.headers, self.proxies, self.encoding,
                         self.tool)
        return page.get_content()
