#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# download_22mt.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

import re
from novel import utils
from urllib.parse import urljoin

SITE_NAME = '22mt'
URLS = ["http://www.22mt.la/xiaohuadetieshengaoshou/"]


class MyNovel(utils.FetchNovel):
    def __init__(self, url):
        super().__init__(url, headers=utils.HEADERS)
        self.bookmark_pattern = r'(.+?)(最新章节).+'
        self.title_pattern = r'\1'
        self.search_type = 'id'
        self.search_text = 'booktext'

    @staticmethod
    def get_chapter_url_pattern():
        return r'^/\w+/\d+/$'

    def get_chapter_url_from_href(self, href):
        return urljoin(utils.get_base_url(self.url), href)

    @staticmethod
    def better_refine(text):
        start ='一秒记住【墨坛文学网】www.22mt.la/manghuangji为您提供精彩小说阅读。'
        text = re.sub(start + r'\n', '', text)
        text = text.strip()
        return text

    @staticmethod
    def get_chapter_name(text):
        return re.sub(r'/.+$', '', text)

    def get_author_from_index(self):
        for item in self.index.find_all('p'):
            m = re.match(r'^(作者: )(.+)$', item.text)
            if m is not None:
                author = m.expand(r'\2')
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
