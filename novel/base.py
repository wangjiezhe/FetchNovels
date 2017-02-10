#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.error import HTTPError
from urllib.parse import urlparse

import pypinyin
from lxml.etree import XMLSyntaxError
from pyquery import PyQuery
from requests import ConnectionError

from novel.config import get_headers, update_and_save_novel_list
from novel.decorators import retry
from novel.utils import Tool


class BaseNovel(object):

    def __init__(self, url,
                 headers=None, proxies=None,
                 encoding='UTF-8', tool=None,
                 tid=None, cache=False):
        self.url = url
        self._headers = headers or get_headers()
        self._proxies = proxies
        self.encoding = encoding
        self.tool = tool or Tool
        self._tid = tid
        self.cache = cache

        self.running = False
        self.overwrite = True
        self.refine = self.doc = None
        self.title = self.author = ''

    @property
    def tid(self):
        if self._tid is not None:
            return str(self._tid)
        else:
            tp = pypinyin.slug(self.title, errors='ignore', separator='_')
            ap = pypinyin.slug(self.author, errors='ignore', separator='_')
            tid = '{} {}'.format(tp, ap)
        return tid

    @classmethod
    def get_source_from_class(cls):
        return cls.__name__.lower()

    def get_source_from_url(self):
        source = urlparse(self.url).netloc
        source = source.lstrip('www.').replace('.', '_')
        return source

    @property
    def source(self):
        return self.get_source_from_class()

    def run(self, refresh=False):
        if self.running and not refresh:
            return
        self.refine = self.tool().refine
        self.doc = self.get_doc()
        self.running = True

    def close(self):
        return

    def update_novel_list(self):
        update_and_save_novel_list(self.source, self.tid)

    @retry((HTTPError, XMLSyntaxError, ConnectionError))
    def get_doc(self):
        return PyQuery(url=self.url, headers=self.headers,
                       proxies=self.proxies, encoding=self.encoding)

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value):
        self._headers = value or {}

    @property
    def proxies(self):
        return self._proxies

    @proxies.setter
    def proxies(self, value):
        self._proxies = value or {}

    def dump(self):
        raise NotImplementedError('dump')

    def dump_and_close(self):
        self.run()
        self.dump()
        self.close()


class SinglePage(BaseNovel):

    def __init__(self, url, selector,
                 headers=None, proxies=None,
                 encoding='UTF-8', tool=None,
                 tid=None, cache=False):
        super().__init__(url, headers, proxies, encoding, tool, tid, cache)
        self.selector = selector

        self.content = ''

    def run(self, refresh=False):
        super().run(refresh=refresh)
        if not self.title:
            self.title = self.get_title()
        if not self.cache:
            self.content = self.get_content()

    def get_content(self):
        if not self.selector:
            return ''
        content = self.doc(self.selector).html() or ''
        content = self.refine(content)
        return content

    def get_title(self):
        if self.title:
            return self.title
        else:
            raise NotImplementedError('get_title')

    def dump(self):
        filename = '{self.title}.txt'.format(self=self)
        print(self.title)
        with open(filename, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n\n')
            fp.write(self.content)
            fp.write('\n')
