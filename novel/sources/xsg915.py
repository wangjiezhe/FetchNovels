#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import single, utils

BASE_URL = 'http://www.xsg915.com/xiaoshuo/{}.html'


class Xsg915Tool(utils.Tool):

    def __init__(self):
        super().__init__(remove_font=False)


class Xsg915(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         '.content',
                         title_type=single.TitleType.selector,
                         title_sel='h1',
                         tid=tid)
        self.tool = Xsg915Tool
