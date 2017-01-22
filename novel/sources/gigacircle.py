#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import single, utils

BASE_URL = 'http://tw.gigacircle.com/{}'


class Gigacircle(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         '.usercontent',
                         title_type=single.TitleType.meta,
                         title_sel=('property', 'og:title'),
                         tid=tid)
