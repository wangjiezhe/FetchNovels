#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .. import single, utils

BASE_URL = 'http://www.sis001.com/forum/archiver/tid-{}.html'


class Sis(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         '.archiver_postbody',
                         title_sel='h2',
                         title_type=single.TitleType.selector,
                         tid=tid)
