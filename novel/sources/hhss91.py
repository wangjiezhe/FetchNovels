#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from novel import single, utils

BASE_URL = 'http://91hhss.com/article-show-id-{}.html'


class Hhss91(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         '.pics',
                         tid=tid)

    def get_title(self):
        st = self.doc('title').text()
        return re.match(r'(.*) 90后黑丝', st).group(1)
