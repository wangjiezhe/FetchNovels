#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# download_69shu.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

import re
from novel import utils
from urllib.parse import urljoin

SITE_NAME = '69shu'
URLS = ["http://www.69shu.com/2875/"]


class MyNovel(utils.FetchNovel):
    def __init__(self, url):
        super().__init__(url, headers=utils.HEADERS, proxies=utils.GOAGENT)
        self.bookmark_pattern = r'(.+?)(最新章节列表),.+'
        self.title_pattern = r'\1'
        self.search_type = 'class_'
        self.search_text = 'yd_text2'

    @staticmethod
    def get_chapter_url_pattern():
        return r'^/txt/\d+/\d+$'

    def get_chapter_url_from_href(self, href):
        return urljoin(utils.get_base_url(self.url), href)

    def get_author_from_index(self):
        author = self.index.find_all(href=re.compile(r'.+author.+'))[0].text
        return author

    def better_refine(self, text):
        return re.sub(r'\n[^\n]+《' + self.title + r'》$', '', text)


def main():
    for url in URLS:
        novel = MyNovel(url)
        print("Downloading novel: %s" % novel.name)
        novel.download_all()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    input("Press <Enter> to quit!")


if __name__ == '__main__':
    main()
