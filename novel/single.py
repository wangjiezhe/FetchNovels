#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

from pyquery import PyQuery

from .base import SinglePage
from .utils import get_filename


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
                lambda i, e: PyQuery(e).attr(self.title_sel[0]) == self.title_sel[1]
            ).attr('content')
        else:
            raise NameError('title_type')

    def get_content(self):
        if not self.selector:
            raise NotImplementedError('get_content')
        content = '\n\n\n\n'.join(
            self.doc(self.selector).map(
                lambda i, e: self.refine(PyQuery(e).html())
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
