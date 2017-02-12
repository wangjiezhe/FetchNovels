#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import single, utils

BASE_URL = 'https://book3k.com/archives/{}'


class Book3k(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         '.entry-content',
                         title_type=single.TitleType.selector,
                         title_sel='h1',
                         tid=tid)
