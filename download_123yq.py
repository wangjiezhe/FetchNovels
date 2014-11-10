#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# download_123yq.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

import re
from novel import utils

SITE_NAME = '123yq'
ENCODING = 'GB18030'
BOOKMARK_PATTERN = r'(.+?),(.+?)\((.+?)\).+'
NAME_PATTERN = r'\1 - \3'
URLS = ["http://www.123yq.com/read/20/20943/"]
SEARCH_TYPE = 'id'
SEARCH_TEXT = 'TXT'


def get_chapter_url_pattern(url):
    return url + r'\d+?\.shtml'


def get_chapter_url_from_href(url, href):
    return href


def get_name_from_index(index):
    novel = index.title.text
    match = re.match(BOOKMARK_PATTERN, novel)
    return match.expand(NAME_PATTERN)


def main():
    for url in URLS:
        novel = utils.FetchNovel(url, headers=utils.HEADERS,
                                 encoding=ENCODING, proxies=utils.PROXIES)
        novel.get_name_from_index = get_name_from_index
        novel.get_chapter_url_from_href = get_chapter_url_from_href
        novel.get_chapter_url_pattern = get_chapter_url_pattern
        novel.search_type = SEARCH_TYPE
        novel.search_text = SEARCH_TEXT
        print("Downloading novel: %s" % novel.name)
        novel.download()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    input("Press <Enter> to quit!")


if __name__ == '__main__':
    main()