#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

import prettytable

from . import sources
from .config import GOAGENT
from .db import create_session, update_novel
from .models import Serial


def list_novels(source=None, tid=None, show_intro=False, show_finish=False):
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
        for nov in novel_list:
            pt.add_row((nov.id, nov.title, nov.author, nov.source))
        if show_intro:
            pt.hrules = prettytable.ALL
            intro_list = [textwrap.fill(nov.intro, width=50)
                          for nov in novel_list]
            pt.add_column('intro', intro_list, align='l')
        if show_finish:
            pt.add_column('finish', [nov.finish for nov in novel_list], valign='m')

    print(pt.get_string())


def delete_novels(source, tid=None):
    with create_session() as session:
        if tid:
            novel_list = session.query(Serial).filter_by(
                source=source, id=str(tid)
            ).all()
        else:
            novel_list = session.query(Serial).filter_by(source=source).all()
        for nov in novel_list:
            for ch in nov.chapters:
                session.delete(ch)
            session.delete(nov)


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


def refresh_novel(source, tid, http_proxy=None):
    delete_novels(source, tid)
    add_novel(source, tid, http_proxy)


def mark_finish(source, tid):
    with create_session() as session:
        nov = session.query(Serial).filter_by(
            source=source, id=str(tid)
        ).one()
        nov.finish = True
