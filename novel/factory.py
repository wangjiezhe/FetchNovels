#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager
from importlib import import_module

from . import sources
from .config import GOAGENT


@contextmanager
def use_novel(source, tid, http_proxy=None, session=None):
    module = import_module('.sources.' + source, 'novel')
    novel_class = getattr(module, source.capitalize())
    nov = novel_class(tid)
    nov.use_session(session)

    if http_proxy:
        if http_proxy != '---':
            nov.proxies = {'http': http_proxy}
    elif source in sources.USE_PROXIES:
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
