#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from .config import CACHE_DB, load_novel_list, save_novel_list
from .models import Base, Website
from .novels import update_novel


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
