#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum
from urllib.error import HTTPError

from pyquery import PyQuery as Pq

from .base import BaseNovel
from .decorators import retry
from .error import MethodNotSetError, ValueNotSetError
from .utils import get_filename


class TitleType(Enum):
    selector = 1
    meta = 2


class SingleNovel(BaseNovel):

    def __init__(self, url, cont_sel,
                 title_sel=None, title_type=None):
        super().__init__(url)
        self.url = url
        self.cont_sel = cont_sel
        self.title_sel = title_sel
        self.title_type = title_type

    def run(self, refresh=False):
        super().run(refresh=refresh)
        self.doc = self.get_doc()
        self.title = self.get_title()
        self.content = self.get_content()
        self.running = True

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
        if self.cont_sel is None:
            raise MethodNotSetError('get_content')
        content = '\n\n\n\n'.join(
            self.doc(self.cont_sel).map(
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
