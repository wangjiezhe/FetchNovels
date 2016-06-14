#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import single, utils, config

BASE_URL = 'http://ebook.s-dragon.org/forum/archiver/?tid-{}.html'


class Sdragon(single.SingleNovel):

    def __init__(self, tid):
        super().__init__(utils.base_to_url(BASE_URL, tid),
                         '.archiver_postbody',
                         title_sel='h2',
                         title_type=single.TitleType.selector)


def main():
    utils.in_main(Sdragon, config.GOAGENT)


if __name__ == '__main__':
    main()
