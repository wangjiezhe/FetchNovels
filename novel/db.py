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
            with NovelFactory(s, tid) as nov:
                nov.add()


class NovelFactory(object):

    def __init__(self, source, tid, http_proxy=None, session=None):
        self.source = source
        self.tid = tid
        self.http_proxy = http_proxy
        self.session = session
        self.nov = None

    def __enter__(self):
        novel_class = getattr(sources, self.source.capitalize())
        self.nov = novel_class(self.tid)
        self.nov.use_session(self.session)

        if self.http_proxy:
            if self.http_proxy != '---':
                self.nov.proxies = {'http': self.http_proxy}
        elif self.source in sources.CERNET_USE_PROXIES:
            self.nov.proxies = GOAGENT

        if self.source in sources.AUTO_MARK_FINISH:
            self.nov.finish = True

        if self.source in sources.DEFAULT_NOT_OVERWRITE:
            self.nov.overwrite = False

        return self.nov

    # noinspection PyUnusedLocal
    def __exit__(self, *args):
        self.nov.close()

    def add(self):
        self.nov.run()

    def dump(self):
        self.nov.dump_and_close()
