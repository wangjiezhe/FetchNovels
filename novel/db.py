#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from . import sources
from .config import CACHE_DB, GOAGENT, load_novel_list, save_novel_list
from .models import Base, Website


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


def update_novel(source, tid, http_proxy=None):
    novel_class = getattr(sources, source.capitalize())
    nov = novel_class(tid)
    if http_proxy:
        if http_proxy != '---':
            nov.proxies = {'http': http_proxy}
    elif source in sources.DEFAULT_USE_PROXIES:
        nov.proxies = GOAGENT
    nov.run()
    nov.close()
