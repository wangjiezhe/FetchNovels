#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

import prettytable

from . import sources
from .config import GOAGENT
from .db import create_session, update_novel
from .models import Serial


def list_novels(source=None, tid=None, verbose=None):
    verbose = verbose or 0
    with create_session() as session:
        if source:
            if tid:
                novel_list = session.query(Serial).filter_by(
                    source=source, id=str(tid)
                ).all()
            else:
                novel_list = session.query(Serial).filter_by(source=source).all()
        else:
            novel_list = session.query(Serial).all()

        pt = prettytable.PrettyTable()
        pt.field_names = ['id', 'title', 'author', 'source']
        pt.valign = 'm'
        for novel in novel_list:
            pt.add_row((novel.id, novel.title, novel.author, novel.source))
        if verbose > 0:
            pt.hrules = prettytable.ALL
            intro_list = [textwrap.fill(nov.intro, width=50)
                          for nov in novel_list]
            pt.add_column('intro', intro_list, align='l')
        if verbose > 1:
            pt.add_column('finish', [novel.finish for novel in novel_list], valign='m')

    print(pt.get_string())


def delete_novels(source=None, tid=None):
    with create_session() as session:
        if source:
            if tid:
                novel_list = session.query(Serial).filter_by(
                    source=source, id=str(tid)
                ).all()
            else:
                novel_list = session.query(Serial).filter_by(source=source).all()
        else:
            novel_list = session.query(Serial).all()
        for novel in novel_list:
            for ch in novel.chapters:
                session.delete(ch)
            session.delete(novel)


def update_novels(source=None, tid=None, http_proxy=None):
    with create_session() as session:
        if source:
            if tid:
                update_novel(source, tid, http_proxy)
            else:
                novel_list = session.query(Serial).filter_by(
                    source=source, finish=False
                ).all()
                for novel in novel_list:
                    update_novel(source, novel.id, http_proxy)
        else:
            novel_list = session.query(Serial).filter_by(finish=False).all()

            for novel in novel_list:
                update_novel(novel.source, novel.id, http_proxy)


def add_novel(source, tid, http_proxy=None):
    return update_novel(source, tid, http_proxy)


def dump_novel(source, tid, http_proxy=None):
    novel_class = getattr(sources, source.capitalize())
    nov = novel_class(tid)
    if http_proxy:
        if http_proxy != '---':
            nov.proxies = {'http': http_proxy}
    elif source in sources.DEFAULT_USE_PROXIES:
        nov.proxies = GOAGENT
    overwrite = source not in sources.DEFAULT_NOT_OVERWRITE
    nov.dump(overwrite=overwrite)


def refresh_novel(source=None, tid=None, http_proxy=None):
    if source:
        if tid:
            delete_novels(source, tid)
            add_novel(source, tid, http_proxy)
        else:
            with create_session() as session:
                novel_list = session.query(Serial).filter_by(source=source).all()
                tids = [novel.id for novel in novel_list]
            delete_novels(source)
            for t in tids:
                add_novel(source, t, http_proxy)
    else:
        with create_session() as session:
            novel_list = session.query(Serial).all()
            nl = [(novel.source, novel.tid) for novel in novel_list]
        delete_novels()
        for s, t in nl:
            add_novel(s, t, http_proxy)


def mark_finish(source, tid=None):
    with create_session() as session:
        if tid:
            novel_list = session.query(Serial).filter_by(
                source=source, id=str(tid)
            ).all()
        else:
            novel_list = session.query(Serial).filter_by(source=source).all()
        for novel in novel_list:
            novel.finish = True
