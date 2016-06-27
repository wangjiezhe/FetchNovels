#!/usr/bin/env python
# -*- coding: utf-8 -*-

import textwrap

import prettytable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from . import sources
from .config import CACHE_DB, load_novel_list, save_novel_list, GOAGENT
from .models import Base, Serial, Website


def create_session(db=CACHE_DB, pool_size=100):
    engine = create_engine(
        'sqlite:///' + db,
        poolclass=SingletonThreadPool,
        pool_size=pool_size
    )
    db_session = sessionmaker(bind=engine)
    session = db_session()
    Base.metadata.create_all(engine)
    return session


def update_all_novels():
    session = create_session()
    novel_list = session.query(Serial).all()
    session.close()

    for novel in novel_list:
        novel_class = getattr(sources, novel.source.capitalize())
        nov = novel_class(novel.id)
        if novel.source in sources.DEFAULT_USE_PROXIES:
            nov.proxies = GOAGENT
        nov.run()
        nov.close()


def list_all_novels(intro=False):
    session = create_session()
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


def update_novel(source, tid):
    novel_class = getattr(sources, source.capitalize())
    nov = novel_class(tid)
    if source in sources.DEFAULT_USE_PROXIES:
        nov.proxies = GOAGENT
    nov.run()

add_novel = update_novel


def refresh_novel(source, tid):
    delete_novels(source, tid)
    update_novel(source, tid)


def sync_db_to_list():
    session = create_session()
    nl = {}
    for w in session.query(Website).all():
        nl[w.name] = [s.id for s in w.novels]
    save_novel_list(nl)


def sync_list_to_db():
    nl = load_novel_list()
    for s, tids in nl.items():
        for tid in tids:
            update_novel(s, tid)
