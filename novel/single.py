#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from enum import Enum
from itertools import count
from urllib.error import HTTPError

from pyquery import PyQuery as Pq

from .decorators import retry
from .error import MethodNotSetError, ValueNotSetError
from .utils import Tool


class TitleType(Enum):
    selector = 1
    meta = 2


class Novel(object):

    def __init__(self, url, cont_sel,
                 title_sel=None, title_type=None,
                 headers=None, proxies=None, encoding=None,
                 tool=Tool):
        self.url = url
        self.cont_sel = cont_sel
        self.title_sel = title_sel
        self.title_type = title_type
        self.headers = headers or {}
        self.proxies = proxies or {}
        self.encoding = encoding
        self.tool = tool()

        self.doc = self.get_doc()
        self.title = self.get_title()

    @retry(HTTPError)
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_title(self):
        if self.title_sel is None:
            raise MethodNotSetError('get_title')
        if self.title_type == TitleType.selector:
            return self.tool.refine(self.doc(self.title_sel).html())
        elif self.title_type == TitleType.meta:
            return self.doc('meta').filter(
                lambda i, e: Pq(e).attr(self.title_sel[0]) == self.title_sel[1]
            ).attr('content')
        else:
            raise ValueNotSetError('title_type')

    def get_content(self):
        if self.cont_sel is None:
            raise MethodNotSetError('get_content')
        content = '\n\n\n\n'.join(
            self.doc(self.cont_sel).map(
                lambda i, e: self.tool.refine(Pq(e).html())
            )
        )
        return content

    def dump(self, overwrite=True):
        print(self.title)
        if overwrite:
            filename = '{self.title}.txt'.format(self=self)
        else:
            filename = self.get_filename()
        content = self.get_content()
        with open(filename, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n\n')
            fp.write(content)

    def get_filename(self):
        filename = '{self.title}.txt'.format(self=self)
        if os.path.exists(filename):
            for i in count(1):
                filename = '{self.title}({num:d}).txt'.format(self=self, num=i)
                if not os.path.exists(filename):
                    break
        return filename
