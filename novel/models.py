#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from sqlalchemy import *
from sqlalchemy import Column, Integer, String, Text, ForeignKeyConstraint
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import relationship


@as_declarative()
class Base(object):

    # noinspection PyMethodParameters
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

    def __repr__(self):
        res = '<{}(id: {}, {})>'.format(
            type(self).__name__,
            self.id,
            ', '.join('{}: {}'.format(k, v) for k, v in vars(self).items()
                      if k in self._display_vars())
        )
        return res

    def _display_vars(self):
        return [k for k in vars(self).keys()
                if not k.startswith('_') and k != 'id']


class Novel(Base):
    title = Column(String)
    author = Column(String)
    intro = Column(Text)
    source = Column(String, primary_key=True)

    chapters = relationship('Chapter')

    def __repr__(self):
        res = "<Novel(id: {self.id}, title: '{self.title}', \
author: '{self.author}', chapters: {num:d}, intro: '{self.intro}')>".format(
            self=self, num=len(self.chapters)
        )
        return res


class Chapter(Base):
    url = Column(String)
    title = Column(String)
    text = Column(Text)

    novel_id = Column(Integer, primary_key=True)
    novel_source = Column(String, primary_key=True)

    ForeignKeyConstraint(
        [novel_id, novel_source],
        [Novel.id, Novel.source]
    )
