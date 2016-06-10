#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from abc import abstractmethod
from enum import Enum
from itertools import count
from urllib.error import HTTPError
from urllib.parse import urljoin

from lxml.etree import XMLSyntaxError
from pyquery import PyQuery as Pq

from .base import BaseNovel
from .decorators import retry
from .error import PropertyNotSetError, ValueNotSetError
from .utils import get_base_url, fix_order


class Page(BaseNovel):

    running = False

    def __init__(self, url, title, selector,
                 headers=None, proxies=None,
                 encoding=None, tool=None):
        super().__init__(url, headers, proxies, encoding, tool)
        self.url = url
        self.title = title
        self.selector = selector

    def run(self):
        self.refine = self.tool().refine
        self.doc = self.get_doc()
        self.running = True

    def confirm_run(self):
        if not self.running:
            self.run()

    @retry((HTTPError, XMLSyntaxError))
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_content(self):
        self.confirm_run()
        if self.selector is None:
            return ''
        content = self.doc(self.selector).html()
        content = self.refine(content)
        return content

    def dump(self, path=None, folder=None, num=None):
        self.confirm_run()
        if path is None:
            if num is not None:
                pre = '「{:d}」'.format(num)
            else:
                pre = ''
            name = '{}{}.txt'.format(pre, self.title)
            if folder is None:
                path = os.path.join(os.getcwd(), name)
            else:
                path = os.path.join(folder, name)
        print(self.title)
        with open(path, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n')
            fp.write(self.get_content())


class IntroPage(BaseNovel):

    running = False

    def __init__(self, url, selector,
                 headers=None, proxies=None, encoding=None,
                 tool=None):
        super().__init__(url, headers, proxies, encoding, tool)
        self.url = url
        self.selector = selector

    def run(self):
        self.refine = self.tool().refine
        self.doc = self.get_doc()
        self.running = True

    def confirm_run(self):
        if not self.running:
            self.run()

    @retry((HTTPError, XMLSyntaxError))
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_content(self):
        self.confirm_run()
        if self.selector is None:
            return ''
        intro = self.doc(self.selector).html()
        intro = self.refine(intro)
        return intro

    def dump(self, overwrite=True):
        self.confirm_run()
        filename = 'intro.txt'
        print('intro')
        with open(filename, 'w') as fp:
            fp.write('简介')
            fp.write('\n\n\n\n')
            fp.write(self.get_content())


class ChapterType(Enum):
    whole = 1
    path = 2
    last = 3
    last_rev = 4


class Novel(BaseNovel):

    running = False

    def __init__(self, url, cont_sel,
                 intro_url=None, intro_sel=None,
                 chap_sel=None, chap_type=None):
        super().__init__(url)
        self.cont_sel = cont_sel
        self.intro_url = intro_url
        self.intro_sel = intro_sel
        self.page = Page
        self.intro_page = IntroPage
        self.chap_sel = chap_sel
        self.chap_type = chap_type

    def run(self):
        self.refine = self.tool().refine
        self.doc = self.get_doc()
        self.title, self.author = self.get_title_and_author()
        self.running = True

    def confirm_run(self):
        if not self.running:
            self.run()

    @retry((HTTPError, XMLSyntaxError))
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    @abstractmethod
    def get_title_and_author(self):
        pass

    @property
    def chapter_list(self):
        self.confirm_run()
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
        self.confirm_run()
        if self.intro_url is None:
            if self.intro_sel is None:
                return ''
            intro = self.doc(self.intro_sel).html()
            intro = self.refine(intro)
            return intro
        else:
            intro_page = self.intro_page(
                self.intro_url, self.intro_sel,
                self.headers, self.proxies, self.encoding,
                self.tool)
            intro = intro_page.get_content()
            return intro

    @property
    def download_dir(self):
        return os.path.join(os.getcwd(),
                            "《{self.title}》{self.author}".format(self=self))

    def dump_split(self):
        if not self.running:
            self.run()
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir)
        print('《{self.title}》{self.author}'.format(self=self))
        for i, url, title in self.chapter_list:
            self.dump_chapter(url, title, i + 1)

    @retry(HTTPError)
    def dump_chapter(self, url, title, num):
        page = self.page(
            url, title, self.cont_sel,
            self.headers, self.proxies, self.encoding,
            self.tool)
        page.dump(folder=self.download_dir, num=num)

    def dump(self, overwrite=True):
        if not self.running:
            self.run()
        if overwrite:
            filename = '《{self.title}》{self.author}.txt'.format(self=self)
        else:
            filename = self.get_filename()
        print(filename)
        with open(filename, 'w') as fp:
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
        page = self.page(
            url, title, self.cont_sel,
            self.headers, self.proxies, self.encoding,
            self.tool)
        return page.get_content()

    def get_filename(self):
        filename = '《{self.title}》{self.author}.txt'.format(self=self)
        if os.path.exists(filename):
            for i in count(1):
                filename = '《{self.title}》{self.author}({num:d}).txt'.format(self=self, num=i)
                if not os.path.exists(filename):
                    break
        return filename
