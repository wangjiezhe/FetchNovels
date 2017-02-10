#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

from pyquery import PyQuery
from termcolor import colored

from novel.base import SinglePage
from novel.db import new_session
from novel.models import Article, Website
from novel.utils import get_filename, get_base_url


class TitleType(Enum):
    selector = 1
    meta = 2


class SingleNovel(SinglePage):

    def __init__(self, url, selector=None,
                 title_type=None, title_sel=None,
                 tid=None, cache=True):
        super().__init__(url, selector,
                         tid=tid, cache=cache)
        self.title_type = title_type
        self.title_sel = title_sel

        self.session = None
        self.use_exist_session = False

    def use_session(self, s):
        if s:
            self.session = s
            self.use_exist_session = True

    def run(self, refresh=False):
        super().run(refresh=refresh)
        print(colored(self.title, 'green'))
        if self.cache:
            if not self.use_exist_session:
                self.session = new_session()
            self._add_website()
            self._add_article()
            self.session.flush()

    def close(self):
        if self.cache and not self.use_exist_session:
            self.session.close()
        self.running = False

    # noinspection PyArgumentList
    def _add_website(self):
        website = self.session.query(Website).filter_by(
            name=self.source
        ).first()

        if not website:
            website = Website(name=self.source,
                              url=get_base_url(self.url))
            self.session.add(website)

    # noinspection PyArgumentList
    def _add_article(self):
        if self.tid is not None:
            article = self.session.query(Article).filter_by(
                id=self.tid, source=self.source
            ).first()
        else:
            article = None

        if not article:
            article = Article(id=self.tid, title=self.title,
                              text=self.get_content(), source=self.source)
            self.session.add(article)

    def get_title(self):
        if not self.title_sel:
            raise NotImplementedError('get_title')
        if self.title_type == TitleType.selector:
            return self.refine(self.doc(self.title_sel).html())
        elif self.title_type == TitleType.meta:
            return self.doc('meta').filter(
                lambda i, e:
                PyQuery(e).attr(self.title_sel[0]) == self.title_sel[1]
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

    def dump(self):
        filename = get_filename(self.title, overwrite=self.overwrite)
        print(filename)
        if self.cache:
            content = self.session.query(Article).filter_by(
                id=self.tid, source=self.source
            ).one().text
        else:
            content = self.content
        with open(filename, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n\n')
            fp.write(content)
            fp.write('\n')

    def dump_and_close(self):
        self.run()
        if self.cache:
            self.update_novel_list()
        self.dump()
        self.close()
