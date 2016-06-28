#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

import prettytable

from . import sources
from .config import GOAGENT
from .db import create_session
from .models import Serial


def list_novels(source=None, tid=None, intro=False):
    session = create_session()
    if source:
        if tid:
            novel_list = session.query(Serial).filter_by(
                source=source, id=str(tid)
            ).all()
        else:
            novel_list = session.query(Serial).filter_by(source=source).all()
    else:
        novel_list = session.query(Serial).all()
    session.close()

    pt = prettytable.PrettyTable()
    pt.field_names = ['id', 'title', 'author', 'source']
    for field in pt.field_names:
        pt.valign[field] = 'm'
    for nov in novel_list:
        pt.add_row((nov.id, nov.title, nov.author, nov.source))
    if intro:
        pt.hrules = prettytable.ALL
        intro_list = [textwrap.fill(nov.intro, width=50) for nov in novel_list]
        pt.add_column('intro', intro_list, align='l')
    print(pt.get_string())


def delete_novels(source, tid=None):
    session = create_session()
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
    session.commit()
    session.close()


def update_novels(source=None, tid=None):
    session = create_session()

    if source:
        if tid:
            _update_novel(source, tid)
        else:
            novel_list = session.query(Serial).filter_by(
                source=source, finish=False
            ).all()
            for novel in novel_list:
                _update_novel(source, novel.id)
    else:
        novel_list = session.query(Serial).filter_by(finish=False).all()

        for novel in novel_list:
            _update_novel(novel.source, novel.id)

    session.commit()
    session.close()


def _update_novel(source, tid):
    novel_class = getattr(sources, source.capitalize())
    nov = novel_class(tid)
    if source in sources.DEFAULT_USE_PROXIES:
        nov.proxies = GOAGENT
    nov.run()
    nov.close()


def add_novel(source, tid):
    return _update_novel(source, tid)


def dump_novel(source, tid):
    novel_class = getattr(sources, source.capitalize())
    nov = novel_class(tid)
    if source in sources.DEFAULT_USE_PROXIES:
        nov.proxies = GOAGENT
    nov.dump()


def refresh_novel(source, tid):
    delete_novels(source, tid)
    add_novel(source, tid)


def mark_finish(source, tid):
    session = create_session()
    nov = session.query(Serial).filter_by(
        source=source, id=str(tid)
    ).one()
    nov.finish = True
    session.commit()
    session.close()
