#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import SingletonThreadPool

from novel.config import CACHE_DB
from novel.models import Base


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
