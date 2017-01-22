#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import single, utils, config

BASE_URL = 'http://bbs.6park.com/bbs4/messages/{}.html'


class Park6(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         title_type=single.TitleType.selector,
                         title_sel='title',
                         tid=tid)
        self.encoding = config.GB

    def get_content(self):
        content = self.doc.html()
        pat = re.compile(r'.*<!--bodybegin-->(.*)<!--bodyend-->.*',
                         re.S)
        content = re.match(pat, content).group(1)
        content = self.refine(content)
        return content
