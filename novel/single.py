#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from enum import Enum
from itertools import count
from urllib.error import HTTPError

from pyquery import PyQuery as Pq

from .base import BaseNovel
from .decorators import retry
from .error import MethodNotSetError, ValueNotSetError


class TitleType(Enum):
    selector = 1
    meta = 2


class SingleNovel(BaseNovel):

    running = False

    def __init__(self, url, cont_sel,
                 title_sel=None, title_type=None):
        super().__init__(url)
        self.url = url
        self.cont_sel = cont_sel
        self.title_sel = title_sel
        self.title_type = title_type

    def run(self):
        self.refine = self.tool().refine
        self.doc = self.get_doc()
        self.title = self.get_title()
        self.running = True

    def confirm_run(self):
        if not self.running:
            self.run()

    @retry(HTTPError)
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_title(self):
        if self.title_sel is None:
            raise MethodNotSetError('get_title')
        if self.title_type == TitleType.selector:
            return self.refine(self.doc(self.title_sel).html())
        elif self.title_type == TitleType.meta:
            return self.doc('meta').filter(
                lambda i, e: Pq(e).attr(self.title_sel[0]) == self.title_sel[1]
            ).attr('content')
        else:
            raise ValueNotSetError('title_type')

    def get_content(self):
        self.confirm_run()
        if self.cont_sel is None:
            raise MethodNotSetError('get_content')
        content = '\n\n\n\n'.join(
            self.doc(self.cont_sel).map(
                lambda i, e: self.refine(Pq(e).html())
            )
        )
        return content

    def dump(self, overwrite=True):
        self.confirm_run()
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
