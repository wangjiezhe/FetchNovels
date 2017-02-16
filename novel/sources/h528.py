#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import single, utils

BASE_URL = 'http://www.h528.com/post/{}.html'


class H528(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         '.post .entry',
                         title_type=single.TitleType.selector,
                         title_sel='.post h2',
                         tid=tid)
