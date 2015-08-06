#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# download_123yq.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

import re
from novel import utils

SITE_NAME = '123yq'
URLS = ["http://www.123yq.com/read/20/20943/",
        "http://www.123yq.com/read/27/27194/",
        "http://www.123yq.com/read/24/24854/"]


class MyNovel(utils.FetchNovel):
    def __init__(self, url):
        super().__init__(url, headers=utils.HEADERS)
        self.bookmark_pattern = r'(.+?),(.+?)\((.+?)\).+'
        self.title_pattern = r'\1'
        self.author_pattern = r'\3'
        self.search_type = 'id'
        self.search_text = 'TXT'

    def get_chapter_url_pattern(self):
        return self.url + r'\d+?\.shtml'

    @staticmethod
    def get_chapter_url_from_href(href):
        return href

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
