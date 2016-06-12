#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from .utils import Tool, get_headers


class BaseNovel(ABC):

    def __init__(self, url,
                 headers=None, proxies=None,
                 encoding=None, tool=None):
        self.url = url
        self._headers = headers or get_headers()
        self._proxies = proxies
        self.encoding = encoding
        self.tool = tool or Tool

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

    @abstractmethod
    def dump(self, overwrite=True):
        pass
