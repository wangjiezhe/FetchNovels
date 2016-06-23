#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

from .models import Base


def create_session(db):
    engine = create_engine(
        'sqlite:///' + db,
        poolclass=SingletonThreadPool,
        pool_size=100
    )
    db_session = sessionmaker(bind=engine, autocommit=True)
    session = db_session()
    Base.metadata.create_all(engine)
    return session
