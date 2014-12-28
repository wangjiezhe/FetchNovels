#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# download_365xs.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

import re
from novel import utils
from urllib.parse import urljoin

SITE_NAME = '365xs'
URLS = ["http://www.365xs.org/books/0/493/"]


class MyNovel(utils.FetchNovel):
    def __init__(self, url):
        super().__init__(url, headers=utils.HEADERS, proxies=utils.GOAGENT)
        self.bookmark_pattern = r'(.+?)(最新章节)\((.+?)\),.+'
        self.title_pattern = r'\1'
        self.author_pattern = r'\3'
        self.search_type = 'id'
        self.search_text = 'content'

    @staticmethod
    def get_chapter_url_pattern():
        return r'^\d+?\.html$'

    def get_chapter_url_from_href(self, href):
        return urljoin(self.url, href)

    def get_author_from_index(self):
        novel = self.index.title.text
        match = re.match(self.bookmark_pattern, novel)
        author = match.expand(self.author_pattern)
        return author


def main():
    for url in URLS:
        novel = MyNovel(url)
        print("Downloading novel: {}".format(novel.name))
        novel.download_all()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    input("Press <Enter> to quit!")


if __name__ == '__main__':
    main()
