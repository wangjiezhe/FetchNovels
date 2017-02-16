#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import single, utils

BASE_URL = 'http://www.yazhouse8.com/article/{}.html'


class Yazhouse8Tool(utils.Tool):

    def __init__(self):
        super().__init__()
        self.remove_extras.append(
            re.compile(r'^记住地址', re.M)
        )


class Yazhouse8(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         '.content',
                         title_type=single.TitleType.selector,
                         title_sel='h1',
                         tid=tid)
        self.tool = Yazhouse8Tool
