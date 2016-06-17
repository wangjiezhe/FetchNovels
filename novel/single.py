#!/usr/bin/env python
# -*- coding: utf-8 -*-

from enum import Enum

from pyquery import PyQuery

from .base import SinglePage
from .config import CACHE_DB
from .models import Article, Website
from .utils import get_filename, connect_database, get_base_url


class TitleType(Enum):
    selector = 1
    meta = 2


class SingleNovel(SinglePage):

    def __init__(self, url, selector,
                 title_sel=None, title_type=None,
                 tid=None, cache=False):
        super().__init__(url, selector,
                         tid=tid, cache=cache)
        self.title_sel = title_sel
        self.title_type = title_type

        self.session = None

    def run(self, refresh=False):
        super().run(refresh=refresh)
        print(self.title)
        if self.cache:
            self.session = connect_database(CACHE_DB)
            self._add_website()
            self._add_article()

    def close(self):
        if self.cache:
            self.session.close()
        self.running = False

    # noinspection PyArgumentList
    def _add_website(self):
        website = self.session.query(Website).filter_by(
            name=self.get_source()
        ).first()

        if not website:
            website = Website(name=self.get_source(),
                              url=get_base_url(self.url))
            self.session.add(website)

    # noinspection PyArgumentList
    def _add_article(self):
        if self.tid is not None:
            article = self.session.query(Article).filter_by(
                id=self.tid, source=self.get_source()
            ).first()
        else:
            article = None
            self.tid = self._new_tid()

        if article is None:
            article = Article(id=self.tid, title=self.title,
                              text=self.get_content(), source=self.get_source())
            self.session.add(article)

    def _new_tid(self):
        return self.session.query(Article).filter(
            Article.source == self.get_source(), Article.id < 0
        ).count() - 1

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

    def _dump(self, overwrite=True):
        filename = get_filename(self.title, overwrite=overwrite)
        print(filename)
        if self.cache:
            content = self.session.query(Article).filter_by(
                id=self.tid, source=self.get_source()
            ).one().text
        else:
            content = self.content
        with open(filename, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n\n')
            fp.write(content)

    def dump(self, overwrite=True):
        self.run()
        self._dump(overwrite=overwrite)
        self.close()
