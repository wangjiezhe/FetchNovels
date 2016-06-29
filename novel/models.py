#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from sqlalchemy import *
from sqlalchemy import Column, Integer, String, Text, ForeignKeyConstraint, Boolean
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship


@as_declarative()
class Base(object):

    # noinspection PyMethodParameters
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    def __repr__(self):
        return '<{}({})>'.format(type(self).__name__, self.column_items_ignore_text)

    @property
    def columns(self):
        return self.__table__.columns.keys()

    @property
    def column_items(self):
        return {c: getattr(self, c) for c in self.columns}

    @property
    def column_items_ignore_text(self):
        return {k.name: self._short_item(k)
                for k in self.__table__.columns.values()}

    def _short_item(self, k):
        if isinstance(k.type, Text):
            return '{} characters'.format(len(getattr(self, k.name)))
        else:
            return getattr(self, k.name)

    def to_json(self):
        return self.column_items


class Website(Base):
    name = Column(String, primary_key=True)
    url = Column(String)

    novels = relationship('General', backref='website',
                          order_by='General.id')


class General(Base):
    id = Column(String, primary_key=True)
    title = Column(String)
    source = Column(String, primary_key=True)

    ForeignKeyConstraint(
        [source], [Website.name]
    )


# serial.SerialNovel
class Serial(General):
    id = Column(String, primary_key=True)
    title = Column(String)
    author = Column(String)
    intro = Column(Text)
    source = Column(String, primary_key=True)
    finish = Column(Boolean, default=False)

    chapters = relationship('Chapter', backref='novel',
                            order_by='Chapter.id')

    ForeignKeyConstraint(
        [id, source, title],
        [General.id, General.source, General.title]
    )


# serial.Page
class Chapter(Base):
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    text = Column(Text)

    novel_id = Column(Integer, primary_key=True)
    novel_source = Column(String, primary_key=True)

    ForeignKeyConstraint(
        [novel_id, novel_source],
        [Serial.id, Serial.source]
    )


# single.SingleNovel
class Article(General):
    id = Column(String, primary_key=True)
    title = Column(String)
    text = Column(Text)
    source = Column(String, primary_key=True)

    ForeignKeyConstraint(
        [id, title, source],
        [General.id, General.title, General.source]
    )
