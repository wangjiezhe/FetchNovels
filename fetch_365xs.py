#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# 365xs.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

import os
import re
import requests
import json
from bs4 import BeautifulSoup

# NOVELS = ["庶女悠然"]
URLS = ["http://www.365xs.org/books/0/493/"]
PROXY = {'http': '127.0.0.1:8087'}
HEADERS = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36"
}
DEFAULT_BOOKMARK_FILE = os.path.expanduser(
    '~/.config/chromium/Default/Bookmarks')
# 由于 chardet 无法正确区分 gb2312 和 gbk, 故直接使用 gb18030.
ENCODING = 'GB18030'
BOOKMARK_PATTERN = r'(.+?)(最新章节)\((.+?)\),.+'
NAME_PATTERN = r'\1 - \3'


def get_novels_from_chromium(bookmark_file=DEFAULT_BOOKMARK_FILE):
    with open(bookmark_file, 'r') as fp:
        bookmarks = json.load(fp)
    for item in bookmarks['roots']['bookmark_bar']['children']:
        if item['name'] == 'novel':
            novels = item['children']
            break
    for item in novels:
        if item['name'] == 'Finished':
            novel_finished = item['children']
            break
    finished_list = []
    finished_url_list = []
    for item in novel_finished:
        if item['url'].find('365xs') != -1:
            match = re.match(BOOKMARK_PATTERN, item['name'])
            finished_list.append(match.expand(NAME_PATTERN))
            finished_url_list.append(item['url'])
    return finished_list, finished_url_list


class FetchNovel(object):
    def __init__(self, url, headers=None, encoding='utf-8', proxies=None):
        self.url = url
        if headers is None:
            self.headers = {}
        else:
            self.headers = headers
        self.encoding = encoding
        self.proxies = proxies
        self.index = self.get_index()
        self.name = self.get_name()
        self.chapter_url_list = self.get_chapter_urls()
        self.download_dir = os.path.join(os.getcwd(), self.name)

    def get_index(self):
        req = requests.get(self.url, headers=self.headers, proxies=self.proxies)
        if req.ok:
            index = BeautifulSoup(req.content, from_encoding=self.encoding)
            return index
        else:
            try:
                req.raise_for_status()
            except requests.HTTPError as exc:
                print(exc)

    def get_name(self):
        novel = self.index.find_all('head')[0].text.strip()
        match = re.match(BOOKMARK_PATTERN, novel)
        return match.expand(NAME_PATTERN)

    def get_chapter_urls(self):
        chapter_url_pattern = r'\d+?\.html'
        chapter_urls = self.index.find_all(href=re.compile(chapter_url_pattern))
        chapter_url_list = list(set(chapter_urls))
        chapter_url_list.sort(key=chapter_urls.index)
        return chapter_url_list

    def download(self):
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir)
        for line in self.chapter_url_list:
            filename = line.text + '.txt'
            filepath = os.path.join(self.download_dir, filename)
            if os.path.exists(filepath):
                continue
            chapter_url = self.url + line['href']
            req = requests.get(chapter_url, headers=self.headers, proxies=self.proxies)
            if req.ok:
                chapter = BeautifulSoup(req.content, from_encoding=self.encoding)
                content = chapter.find_all(id='content')[0]
                text = str(content)
                text = text.replace('<br/>', '\n')
                text = re.sub(r'<.+>', '', text)
                with open(filepath, 'w') as fp:
                    fp.write(text)
            else:
                try:
                    req.raise_for_status()
                except requests.HTTPError as exc:
                    print(exc)


def main():
    # for url in get_novels_from_chromium()[1]
    for url in URLS:
        novel = FetchNovel(url, headers=HEADERS, encoding=ENCODING, proxies=PROXY)
        print("Fetching novel: %s" % novel.name)
        novel.download()
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~END~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    input("Press <Enter> to quit!")


if __name__ == '__main__':
    main()
