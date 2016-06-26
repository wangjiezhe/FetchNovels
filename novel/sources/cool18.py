#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from .. import single, utils

BASE_URL = 'http://www.cool18.com/bbs4/index.php?app=forum&act=threadview&tid={}'


class Cool18Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.extend((
            re.compile(r'www\.6park\.com'),
            re.compile(r'<.*?bodyend.*?>.*')
        ))


class Cool18(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         'pre',
                         title_sel=('name', 'Description'),
                         title_type=single.TitleType.meta,
                         tid=tid)
        self.tool = Cool18Tool
