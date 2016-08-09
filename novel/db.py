#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import SingletonThreadPool

from . import sources
from .config import CACHE_DB, GOAGENT, load_novel_list, save_novel_list
from .models import Base, Website


@contextmanager
def create_session(db=CACHE_DB, pool_size=100):
    session = new_session(db, pool_size)
    try:
        yield session
        session.flush()
    except:
        session.rollback()
        raise
    else:
        session.close()


def new_session(db=CACHE_DB, pool_size=100):
    engine = create_engine(
        'sqlite:///' + db,
        poolclass=SingletonThreadPool,
        pool_size=pool_size
    )
    db_session = scoped_session(sessionmaker(
        bind=engine,
        autoflush=True,
        autocommit=True
    ))
    session = db_session()
    Base.metadata.create_all(engine)
    return session


def sync_db_to_list():
    with create_session() as session:
        nl = {}
        for w in session.query(Website).all():
            nl[w.name] = [s.id for s in w.novels]
    save_novel_list(nl)


def sync_list_to_db():
    nl = load_novel_list()
    for s, tids in nl.items():
        for tid in tids:
            add_novel(s, tid)


def add_novel(source, tid, http_proxy=None, session=None):
    novel_class = getattr(sources, source.capitalize())
    nov = novel_class(tid)
    nov.use_session(session)

    if http_proxy:
        if http_proxy != '---':
            nov.proxies = {'http': http_proxy}
    elif source in sources.CERNET_USE_PROXIES:
        nov.proxies = GOAGENT

    if source in sources.AUTO_MARK_FINISH:
        nov.finish = True

    nov.run()
    nov.close()


def dump_novel(source, tid, http_proxy=None):
    novel_class = getattr(sources, source.capitalize())
    nov = novel_class(tid)

    if http_proxy:
        if http_proxy != '---':
            nov.proxies = {'http': http_proxy}
    elif source in sources.CERNET_USE_PROXIES:
        nov.proxies = GOAGENT

    if source in sources.AUTO_MARK_FINISH:
        nov.finish = True

    overwrite = source not in sources.DEFAULT_NOT_OVERWRITE

    nov.dump(overwrite=overwrite)
