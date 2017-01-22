#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import single, utils, config

BASE_URL = 'http://www.sis001.com/forum/archiver/tid-{}.html'


class Sis(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         '.archiver_postbody',
                         title_type=single.TitleType.selector,
                         title_sel='h2',
                         tid=tid)
        self.encoding = config.GB
