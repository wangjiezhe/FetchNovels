#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

import prettytable

from . import sources
from .config import GOAGENT
from .db import create_session, update_novel
from .models import Serial


def list_novels(source=None, tid=None, show_intro=False, show_finish=False):
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
    pt.valign = 'm'
    for nov in novel_list:
        pt.add_row((nov.id, nov.title, nov.author, nov.source))
    if show_intro:
        pt.hrules = prettytable.ALL
        intro_list = [textwrap.fill(nov.intro.replace, width=50)
                      for nov in novel_list]
        pt.add_column('intro', intro_list, align='l')
    if show_finish:
        pt.add_column('finish', [nov.finish for nov in novel_list], valign='m')
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
            update_novel(source, tid)
        else:
            novel_list = session.query(Serial).filter_by(
                source=source, finish=False
            ).all()
            for novel in novel_list:
                update_novel(source, novel.id)
    else:
        novel_list = session.query(Serial).filter_by(finish=False).all()

        for novel in novel_list:
            update_novel(novel.source, novel.id)

    session.commit()
    session.close()


def add_novel(source, tid):
    return update_novel(source, tid)


def dump_novel(source, tid):
    novel_class = getattr(sources, source.capitalize())
    nov = novel_class(tid)
    if source in sources.DEFAULT_USE_PROXIES:
        nov.proxies = GOAGENT
    overwrite = source not in sources.DEFAULT_NOT_OVERWRITE
    nov.dump(overwrite=overwrite)


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
