#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from . import sources
from .config import CACHE_DB
from .models import Base, Serial


def create_session(db=CACHE_DB):
    engine = create_engine(
        'sqlite:///' + db,
        poolclass=SingletonThreadPool,
        pool_size=100
    )
    db_session = sessionmaker(bind=engine, autocommit=True)
    session = db_session()
    Base.metadata.create_all(engine)
    return session


def update_all(db=CACHE_DB):
    session = create_session(db)
    novel_list = session.query(Serial).all()
    for novel in novel_list:
        novel_class = getattr(sources, novel.source.capitalize())
        nov = novel_class(novel.id)
        nov.run()
    session.close()
