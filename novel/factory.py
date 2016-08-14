#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import sources
from .config import GOAGENT


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
