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
ENCODING = 'GB18030'
URLS = ["http://www.69shu.com/2875/"]
BOOKMARK_PATTERN = r'(.+?)(最新章节列表),.+'
NAME_PATTERN = r'\1'
SEARCH_TYPE = 'class_'
SEARCH_TEXT = 'yd_text2'


def get_chapter_url_pattern(url):
    return r'^/txt/\d+/\d+$'


def get_chapter_url_from_href(url, href):
    return urljoin(utils.get_base_url(url), href)


def get_name_from_index(index):
    novel = index.title.text
    match = re.match(BOOKMARK_PATTERN, novel)
    author = index.find_all(href=re.compile(r'.+author.+'))[0].text
    return match.expand(NAME_PATTERN) + ' - ' + author


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
        novel.download_all()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    input("Press <Enter> to quit!")


if __name__ == '__main__':
    main()
