#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import single, utils, config

BASE_URL = 'http://www.cool18.com/bbs4/index.php?app=forum&act=threadview&tid={}'


class Cool18Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.append(
            re.compile(r'<.*?bodyend.*?>.*')
        )


class Cool18(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         'pre',
                         title_type=single.TitleType.meta,
                         title_sel=('name', 'Description'),
                         tid=tid)
        self.tool = Cool18Tool
        self.encoding = config.GB
