#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager

from . import sources
from .config import GOAGENT


@contextmanager
def use_novel(source, tid, http_proxy=None, session=None):
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

    if source in sources.DEFAULT_NOT_OVERWRITE:
        nov.overwrite = False

    yield nov

    nov.close()


def add_novel(source, tid, http_proxy=None, session=None):
    with use_novel(source, tid, http_proxy, session) as nov:
        nov.run()


def dump_novel(source, tid, http_proxy=None, session=None):
    with use_novel(source, tid, http_proxy, session) as nov:
        nov.run()
        nov.dump()
