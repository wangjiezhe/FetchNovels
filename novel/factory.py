#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager
from importlib import import_module

from novel import sources
from novel.config import GOPROXY


@contextmanager
def use_novel(source, tid, http_proxy=None, session=None):
    module = import_module('.sources.' + source, 'novel')
    novel_class = getattr(module, source.capitalize())
    nov = novel_class(tid)
    nov.use_session(session)

    if http_proxy:
        if http_proxy != '---':
            nov.proxies = {'http': http_proxy}
    elif source in sources.CERNET_USE_PROXIES:
        nov.proxies = GOPROXY

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
