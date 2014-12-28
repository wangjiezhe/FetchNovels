#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# download_feisuzw.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

import re
from novel import utils
from urllib.parse import urljoin

SITE_NAME = 'feisuzw'
URLS = ["http://www.feisuzw.com/Html/1765/"]


class MyNovel(utils.FetchNovel):
    def __init__(self, url):
        super().__init__(url, headers=utils.HEADERS, index_suf='Index.html')
        self.bookmark_pattern = r'(.+?)( - 飞速中文网 - ).+'
        self.title_pattern = r'\1'
        self.search_type = 'id'
        self.search_text = 'content'

    @staticmethod
    def get_chapter_url_pattern():
        return r'^\d+\.html$'

    def get_chapter_url_from_href(self, href):
        return urljoin(self.url, href)

    @staticmethod
    def better_refine(text):
        return re.sub(r'www.feisuzw.com\s+飞速中文网', '', text, flags=re.I)

    def get_author_from_index(self):
        for item in self.index.find_all('span'):
            m = re.match(r'^(文 / )(.+)$', item.text)
            if m is not None:
                author = m.expand(r'\2')
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
