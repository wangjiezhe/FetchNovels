#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# download_ranwen.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

from novel import utils
from urllib.parse import urljoin

SITE_NAME = 'ranwen'
URLS = ["http://www.ranwen.net/files/article/15/15008/"]


class MyNovel(utils.FetchNovel):
    def __init__(self, url):
        super().__init__(url, headers=utils.HEADERS, proxies=utils.GOAGENT)
        self.bookmark_pattern = r'(.+?)(最新章节列表).+'
        self.title_pattern = r'\1'
        self.search_type = 'id'
        self.search_text = 'content'

    @staticmethod
    def get_chapter_url_pattern():
        return r'^\d+\.html$'

    def get_chapter_url_from_href(self, href):
        return urljoin(self.url, href)

    def get_author_from_index(self):
        author = self.index.find_all(attrs={'name': 'author'})[0]['content']
        return author


def main():
    for url in URLS:
        novel = MyNovel(url)
        print("Downloading novel: %s" % novel.name)
        novel.download_all()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    input("Press <Enter> to quit!")


if __name__ == '__main__':
    main()
