#!/usr/bin/env python
# -*- coding: utf-8 -*-
from abc import abstractmethod
from enum import Enum
from urllib.error import HTTPError

from lxml.etree import XMLSyntaxError
from pyquery import PyQuery as Pq

from .base import BaseNovel
from .decorators import retry
from .utils import get_filename


class SinglePage(BaseNovel):

    def __init__(self, url, selector,
                 headers=None, proxies=None,
                 encoding=None, tool=None):
        super().__init__(url, headers, proxies, encoding, tool)
        self.selector = selector

        self.doc = None
        self.title = self.content = ''

    @retry((HTTPError, XMLSyntaxError))
    def run(self, refresh=False):
        super().run(refresh=refresh)
        self.doc = self.get_doc()
        self.content = self.get_content()
        # self.running = True

    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_content(self):
        if not self.selector:
            return ''
        content = self.doc(self.selector).html()
        content = self.refine(content)
        return content

    @abstractmethod
    def dump(self, overwrite=True):
        pass


class TitleType(Enum):
    selector = 1
    meta = 2


class SingleNovel(SinglePage):

    def __init__(self, url, selector,
                 title_sel=None, title_type=None):
        super().__init__(url, selector)
        self.title_sel = title_sel
        self.title_type = title_type

    def run(self, refresh=False):
        super().run(refresh=refresh)
        self.title = self.get_title()
        self.running = True

    def get_title(self):
        if self.title_sel is None:
            raise NotImplementedError('get_title')
        if self.title_type == TitleType.selector:
            return self.refine(self.doc(self.title_sel).html())
        elif self.title_type == TitleType.meta:
            return self.doc('meta').filter(
                lambda i, e: Pq(e).attr(self.title_sel[0]) == self.title_sel[1]
            ).attr('content')
        else:
            raise NameError('title_type')

    def get_content(self):
        if not self.selector:
            raise NotImplementedError('get_content')
        content = '\n\n\n\n'.join(
            self.doc(self.selector).map(
                lambda i, e: self.refine(Pq(e).html())
            )
        )
        return content

    def dump(self, overwrite=True):
        self.run()
        print(self.title)
        filename = get_filename(self.title, overwrite=overwrite)
        with open(filename, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n\n')
            fp.write(self.content)
