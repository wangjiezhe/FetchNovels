#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

import prettytable

from . import sources
from .config import save_novel_list
from .db import add_novel, new_session
from .models import Serial, Website, Article, General
from .utils import get_filename


class NovelFactory(object):

    def __init__(self, source=None, tids=None, http_proxy=None, verbose=None):
        self.source = source
        self.tids = tids or []
        self.http_proxy = http_proxy
        self.verbose = verbose or 0

    def __enter__(self):
        self.session = new_session()
        return self

    # noinspection PyUnusedLocal
    def __exit__(self, *args):
        self.session.flush()
        self.session.close()
        self.save()

    def save(self):
        nl = {w.name: [s.id for s in w.novels]
              for w in self.session.query(Website).all()}
        save_novel_list(nl)

    def list(self, source=None):
        source = source or self.source

        if source:
            if source in sources.SERIAL_TYPE:
                self.list_serial(source)
            elif source in sources.ARTICLE_TYPE:
                self.list_article(source)
            else:
                print('The specific source `{}` does not exists!'.format(source))
        else:
            novel_list = self.session.query(General).all()

            pt = prettytable.PrettyTable()
            pt.field_names = ['id', 'title', 'source']
            pt.valign = 'm'
            for novel in novel_list:
                pt.add_row((novel.id, novel.title, novel.source))

            print(pt.get_string())

    def list_article(self, source=None):
        source = source or self.source

        if source:
            novel_list = self.session.query(Article).filter_by(
                source=source
            ).all()
        else:
            novel_list = self.session.query(Article).all()

        pt = prettytable.PrettyTable()
        pt.field_names = ['id', 'title', 'source']
        pt.valign = 'm'
        for novel in novel_list:
            pt.add_row((novel.id, novel.title, novel.source))

        if self.verbose > 0:
            length_list = [len(novel.text) for novel in novel_list]
            pt.add_column('length', length_list)

        print(pt.get_string())

    def list_serial(self, source=None):
        source = source or self.source

        if source:
            novel_list = self.session.query(Serial).filter_by(
                source=source
            ).all()
        else:
            novel_list = self.session.query(Serial).all()

        pt = prettytable.PrettyTable()
        pt.field_names = ['id', 'title', 'author', 'source']
        pt.valign = 'm'
        for novel in novel_list:
            pt.add_row((novel.id, novel.title, novel.author, novel.source))
        if self.verbose > 0:
            pt.hrules = prettytable.ALL
            intro_list = [textwrap.fill(novel.intro, width=50)
                          for novel in novel_list]
            pt.add_column('intro', intro_list, align='l')
        if self.verbose > 1:
            pt.add_column('finish', [novel.finish for novel in novel_list], valign='m')

        print(pt.get_string())

    def delete_serial(self, source, tid):
        novel = self.session.query(Serial).filter_by(
            source=source, id=tid
        ).one()
        for ch in novel.chapters:
            self.session.delete(ch)
        self.session.delete(novel)

    def delete_article(self, source, tid):
        article = self.session.query(Article).filter_by(
            source=source, id=tid
        ).one()
        self.session.delete(article)

    def delete(self, source=None, tids=None):
        source = source or self.source
        tids = tids or self.tids

        if source:
            if tids:
                novel_list = self.session.query(General).filter(
                    General.source == source, General.id.in_(tids)
                )
            else:
                novel_list = self.session.query(General).filter_by(source=source).all()
        else:
            novel_list = self.session.query(General).all()

        deleted = {}

        for novel in novel_list:
            deleted[novel.source] = deleted.get(novel.source, []) + [novel.id]
            if novel.source in sources.SERIAL_TYPE:
                self.delete_serial(novel.source, novel.id)
            elif novel.source in sources.ARTICLE_TYPE:
                self.delete_article(novel.source, novel.id)
            else:
                print('Something strange may happens here.')

        for s, t in deleted.items():
            print('{}: {}'.format(s, t))

        return deleted

    def update(self, source=None, tids=None):
        source = source or self.source
        tids = tids or self.tids

        if source:
            if tids:
                for tid in tids:
                    add_novel(source, tid,
                              http_proxy=self.http_proxy,
                              session=self.session)
            else:
                novel_list = self.session.query(Serial).filter_by(
                    source=source, finish=False
                ).all()
                for novel in novel_list:
                    add_novel(source, novel.id,
                              http_proxy=self.http_proxy,
                              session=self.session)
        else:
            novel_list = self.session.query(Serial).filter_by(finish=False).all()
            for novel in novel_list:
                add_novel(novel.source, novel.id,
                          http_proxy=self.http_proxy,
                          session=self.session)

    def dump_novel(self, source, tid):
        if source in sources.SERIAL_TYPE:
            self.dump_serial(source, tid)
        elif source in sources.ARTICLE_TYPE:
            self.dump_article(source, tid)
        else:
            print('The specific source `{}` does not exists!'.format(source))

    def dump_serial(self, source, tid):
        novel = self.session.query(Serial).filter_by(
            source=source, id=tid
        ).one()
        filename = get_filename(novel.title, novel.author)
        print(filename)

        with open(filename, 'w') as fp:
            fp.write(novel.title)
            fp.write('\n\n')
            fp.write(novel.author)
            fp.write('\n\n\n')
            fp.write(novel.intro)
            for ch in novel.chapters:
                fp.write('\n\n\n\n')
                fp.write(ch.title)
                fp.write('\n\n\n')
                fp.write(ch.text)
                fp.write('\n')

    def dump_article(self, source, tid):
        novel = self.session.query(Article).filter_by(
            source=source, id=tid
        ).one()
        filename = get_filename(novel.title)
        print(filename)

        with open(filename, 'w') as fp:
            fp.write(novel.title)
            fp.write('\n\n\n\n')
            fp.write(novel.text)
            fp.write('\n')

    def dump(self, source=None, tids=None):
        source = source or self.source
        tids = tids or self.tids

        if source:
            if tids:
                for tid in tids:
                    self.dump_novel(source, tid)
            else:
                site = self.session.query(Website).filter_by(name=source).one()
                for novel in site.novels:
                    self.dump_novel(source, novel.id)
        else:
            novel_list = self.session.query(General).all()
            for novel in novel_list:
                self.dump_novel(novel.source, novel.id)

    def mark_finish(self, source=None, tids=None):
        source = source or self.source
        tids = tids or self.tids

        if source:
            if tids:
                novel_list = self.session.query(Serial).filter(
                    Serial.source == source, Serial.id.in_(tids)
                ).all()
            else:
                novel_list = self.session.query(Serial).filter_by(source=source).all()
        else:
            novel_list = self.session.query(Serial).all()

        for novel in novel_list:
            novel.finish = True

    def refresh(self, source=None, tids=None):
        source = source or self.source
        tids = tids or self.tids

        deleted = self.delete(source, tids)
        for s, t in deleted.items():
            self.update(s, t)
