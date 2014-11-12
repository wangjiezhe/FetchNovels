#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# utils.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

import os
import re
import requests
import json
from urllib.parse import urlparse, urlunparse
from bs4 import BeautifulSoup
from .error import ValueNotSetError, FuncNotSetError

PROXIES = {'http': '127.0.0.1:8087'}
HEADERS = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36"
}
DEFAULT_BOOKMARK_FILE = os.path.expanduser(
    '~/.config/chromium/Default/Bookmarks')


def get_novels_from_chromium(site_name, bookmark_pattern, name_pattern,
                             bookmark_file=DEFAULT_BOOKMARK_FILE):
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
        if item['url'].find(site_name) != -1:
            match = re.match(bookmark_pattern, item['name'])
            finished_list.append(match.expand(name_pattern))
            finished_url_list.append(item['url'])
    return finished_list, finished_url_list


def get_base_url(url):
    result = urlparse(url)
    base_url = urlunparse((result.scheme, result.netloc, '', '', '', ''))
    return base_url


def refine_text(text):
    text = text.replace('\r\n', '')
    text = text.replace('\r', '')
    text = text.replace('<br/>', '\n')
    text = re.sub(r'<.+>', '', text)
    text = text.strip('\n')
    text = text.strip(' ')
    return text


class FetchNovel(object):
    def __init__(self, url, headers=None, encoding='utf-8', proxies=None):
        self.url = url
        self.headers = headers or {}
        self.encoding = encoding
        self.proxies = proxies or {}
        self.index = self.get_index()
        self.refine_text = refine_text
        self.better_refine = None
        self._name = ''
        self._chapter_url = ''
        self._chapter_url_list = []
        self._search_type = ''
        self._search_text = ''
        self.get_name_from_index = None
        self.get_chapter_url_pattern = None
        self.get_chapter_url_from_href = None

    @property
    def name(self):
        if not self._name:
            if callable(self.get_name_from_index):
                self._name = self.get_name_from_index(self.index)
            else:
                raise FuncNotSetError("get_name_from_index")
        return self._name

    @property
    def download_dir(self):
        return os.path.join(os.getcwd(), self.name)

    @property
    def chapter_url_list(self):
        if not self._chapter_url_list:
            self._chapter_url_list = self.get_chapter_urls()
        return self._chapter_url_list

    @property
    def chapter_url_pattern(self):
        if callable(self.get_chapter_url_pattern):
            pattern = self.get_chapter_url_pattern(self.url)
            return pattern
        else:
            raise FuncNotSetError("get_chapter_url_pattern")

    @property
    def chapter_url(self):
        return self._chapter_url

    @chapter_url.setter
    def chapter_url(self, href):
        if callable(self.get_chapter_url_pattern):
            self._chapter_url = self.get_chapter_url_from_href(self.url, href)
        else:
            raise FuncNotSetError("get_chapter_url_from_href")

    @property
    def search_type(self):
        if not self._search_type:
            raise ValueNotSetError("search_type")
        else:
            return self._search_type

    @search_type.setter
    def search_type(self, stype):
        self._search_type = stype

    @property
    def search_text(self):
        if not self._search_text:
            raise ValueNotSetError("search_text")
        else:
            return self._search_text

    @search_text.setter
    def search_text(self, text):
        self._search_text = text

    def get_index(self):
        req = requests.get(self.url, headers=self.headers, proxies=self.proxies)
        if req.ok:
            index = BeautifulSoup(req.content, from_encoding=self.encoding)
            return index
        else:
            req.raise_for_status()

    def get_chapter_urls(self):
        chapter_urls = self.index.find_all(href=re.compile(self.chapter_url_pattern))
        chapter_url_list = list(set(chapter_urls))
        chapter_url_list.sort(key=chapter_urls.index)
        return chapter_url_list

    def download_chapter(self, filepath):
        req = requests.get(self.chapter_url, headers=self.headers, proxies=self.proxies)
        if req.ok:
            chapter = BeautifulSoup(req.content, from_encoding=self.encoding)
            search_cmd = "chapter.find_all(%s=\"%s\")[0]" \
                         % (self.search_type, self.search_text)
            content = eval(search_cmd)
            text = self.refine_text(str(content))
            if callable(self.better_refine):
                text = self.better_refine(text)
            with open(filepath, 'w') as fp:
                fp.write(text)
        else:
            req.raise_for_status()

    def download_all(self):
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir)
        for line in self.chapter_url_list:
            filename = line.text + '.txt'
            filepath = os.path.join(self.download_dir, filename)
            if os.path.exists(filepath):
                continue
            self.chapter_url = line['href']
            self.download_chapter(filepath)

    def download_test(self):
        target = self.chapter_url_list[-1]
        filename = target.text + '.txt'
        self.chapter_url = target['href']
        self.download_chapter(filename)
