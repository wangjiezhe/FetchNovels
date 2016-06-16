#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.error import HTTPError

from lxml.etree import XMLSyntaxError
from pyquery import PyQuery
from requests import ConnectionError

from .config import get_headers
from .decorators import retry
from .utils import Tool


class BaseNovel(object):

    def __init__(self, url,
                 headers=None, proxies=None,
                 encoding=None, tool=None):
        self.url = url
        self._headers = headers or get_headers()
        self._proxies = proxies
        self.encoding = encoding
        self.tool = tool or Tool
        self.running = False

        self.refine = self.doc = None
        self.title = self.author = ''

    def run(self, refresh=False):
        if self.running and not refresh:
            return
        self.refine = self.tool().refine
        self.doc = self.get_doc()
        self.running = True

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

    def dump(self, overwrite=True):
        raise NotImplementedError('dump')


class SinglePage(BaseNovel):

    def __init__(self, url, selector,
                 headers=None, proxies=None,
                 encoding=None, tool=None):
        super().__init__(url, headers, proxies, encoding, tool)
        self.selector = selector

        self.content = ''

    def run(self, refresh=False):
        super().run(refresh=refresh)
        if self.title:
            self.title = self.get_title()
        self.content = self.get_content()

    def get_content(self):
        if not self.selector:
            return ''
        content = self.doc(self.selector).html()
        content = self.refine(content)
        return content

    def get_title(self):
        if self.title:
            return self.title
        else:
            raise NotImplementedError('get_title')

    def dump(self, overwrite=True):
        self.run()
        filename = '{self.title}.txt'.format(self=self)
        print(self.title)
        with open(filename, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n\n')
            fp.write(self.content)
            fp.write('\n')
