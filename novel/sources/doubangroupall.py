#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel.sources import doubangroup


class Doubangroupall(doubangroup.Doubangroup):

    def __init__(self, topic_id):
        super().__init__(topic_id, author_only=False)
