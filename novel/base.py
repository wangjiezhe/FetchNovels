#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .config import get_headers
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

        self.refine = None

    def run(self, refresh=False):
        if self.running and not refresh:
            return
        self.refine = self.tool().refine
        # self.running = True

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
