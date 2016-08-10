#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

import prettytable
from readchar import readchar
from termcolor import colored, cprint

from . import sources
from .config import save_novel_list, GOAGENT
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
                return self.list_serial(source)
            elif source in sources.ARTICLE_TYPE:
                return self.list_article(source)
            else:
                print('The specific source `{}` does not exists!'.format(source))
        else:
            novel_list = self.session.query(General).all()

            pt = prettytable.PrettyTable()
            pt.field_names = ['id', 'title', 'source']
            pt.valign = 'm'
            for novel in novel_list:
                pt.add_row((novel.id, colored(novel.title, 'green'), novel.source))

            print(pt.get_string())
            return pt

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
            pt.add_row((novel.id, colored(novel.title, 'green'), novel.source))

        if self.verbose > 0:
            length_list = [len(novel.text) for novel in novel_list]
            pt.add_column('length', length_list)

        print(pt.get_string())
        return pt

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
            pt.add_row((novel.id, colored(novel.title, 'green'), novel.author, novel.source))
        if self.verbose > 0:
            pt.hrules = prettytable.ALL
            intro_list = [textwrap.fill(novel.intro, width=40)
                          for novel in novel_list]
            pt.add_column('intro', intro_list, align='l')
        if self.verbose > 1:
            pt.add_column(
                'finish', [novel.finish for novel in novel_list], valign='m')
        if self.verbose > 2:
            pt.add_column(
                'chapters', [len(novel.chapters) for novel in novel_list], valign='m')

        print(pt.get_string())
        return pt

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
                ).all()
            else:
                novel_list = self.session.query(General).filter_by(
                    source=source
                ).all()
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
                return
            else:
                novel_list = self.session.query(Serial).filter_by(
                    source=source, finish=False
                ).all()
        else:
            novel_list = self.session.query(Serial).filter_by(
                finish=False
            ).all()

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
                novel_list = self.session.query(Serial).filter_by(
                    source=source
                ).all()
        else:
            novel_list = self.session.query(Serial).all()

        for novel in novel_list:
            novel.finish = True

    def try_mark_finish(self, source=None, tids=None):
        source = source or self.source
        tids = tids or self.tids

        if source:
            if tids:
                novel_list = self.session.query(Serial).filter(
                    Serial.source == source, Serial.id.in_(tids)
                ).all()
            else:
                novel_list = self.session.query(Serial).filter_by(
                    source=source, finish=False
                ).all()
        else:
            novel_list = self.session.query(Serial).filter_by(
                finish=False
            ).all()

        def try_mark_novel(n):
            print(n.id, colored(n.title, 'green'), n.author, n.source)
            cprint('Mark ths novel as finished? [y/N/q/u/?]', 'cyan')
            yes = readchar().lower()
            if yes == 'y':
                n.finish = True
            elif yes == 'q':
                return -1
            elif yes == 'u':
                n.finish = False
            elif yes == 'n' or yes == '\r':
                return
            else:
                print()
                cprint('y - mark this novel as finished', 'red')
                cprint('n - do not change finish status', 'red')
                cprint('q - quit; do not change finish status of this and any other novels', 'red')
                cprint('u - mark this novel as unfinished', 'red')
                cprint('? - print help', 'red')
                return try_mark_novel(n)

        for novel in novel_list:
            res = try_mark_novel(novel)
            print()
            if res == -1:
                break

    def refresh(self, source=None, tids=None):
        source = source or self.source
        tids = tids or self.tids

        deleted = self.delete(source, tids)
        for s, t in deleted.items():
            self.update(s, t)


def get_schema(s):
    if s in sources.SERIAL_TYPE:
        return Serial
    elif s in sources.ARTICLE_TYPE:
        return Article
    else:
        raise NotImplementedError(s)


def get_class(s):
    return getattr(sources, s.capitalize())


def get_proxies(s):
    if s in sources.CERNET_USE_PROXIES:
        return GOAGENT
    else:
        return None
