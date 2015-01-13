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
import chardet
import time
from urllib.parse import urlparse, urlunparse, urljoin
from bs4 import BeautifulSoup
from functools import partial
from .error import ValueNotSetError, FuncNotSetError

GOAGENT = {'http': '127.0.0.1:8087'}
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
        if item['name'] == 'Novel':
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


class FetchNovel(object):
    def __init__(self, url, headers=None, proxies=None, index_suf=None):
        self.url = url
        self.headers = headers or {}
        self.proxies = proxies or {}
        self.index_suf = index_suf or ''
        self.get = partial(requests.get, headers=self.headers, proxies=self.proxies)
        self.encoding = None
        self.index = self.get_index()
        self._name = ''
        self._title = ''
        self._author = ''
        self._chapter_url = ''
        self._chapter_name = ''
        self._chapter_url_list = []
        self._search_type = ''
        self._search_text = ''
        self._bookmark_pattern = ''
        self._title_pattern = ''
        self._author_pattern = ''
        # self.get_author_from_index = None
        # self.get_chapter_url_pattern = None
        # self.get_chapter_url_from_href = None
        # self.better_refine = None
        # self.get_chapter_name = None

    @property
    def index_url(self):
        return urljoin(self.url, self.index_suf)

    @property
    def title(self):
        if not self._title:
            self._title = self.get_title_from_index()
        return self._title

    @property
    def name(self):
        if not self._name:
            self._name = self.title + ' - ' + self.author
        return self._name

    @property
    def author(self):
        if not self._author:
            if hasattr(self, 'get_author_from_index') and callable(self.get_author_from_index):
                self._author = self.get_author_from_index()
            else:
                raise FuncNotSetError("get_author_from_index")
        return self._author

    @property
    def download_dir(self):
        return os.path.join(os.getcwd(), self.name)

    @property
    def chapter_url_list(self):
        if not self._chapter_url_list:
            self._chapter_url_list = self.get_chapter_url_list()
        return self._chapter_url_list

    @property
    def chapter_url_pattern(self):
        if hasattr(self, 'get_chapter_url_pattern') and callable(self.get_chapter_url_pattern):
            pattern = self.get_chapter_url_pattern()
            return pattern
        else:
            raise FuncNotSetError("get_chapter_url_pattern")

    @property
    def chapter_url(self):
        return self._chapter_url

    @chapter_url.setter
    def chapter_url(self, href):
        if hasattr(self, 'get_chapter_url_from_href') and callable(self.get_chapter_url_from_href):
            self._chapter_url = self.get_chapter_url_from_href(href)
        else:
            raise FuncNotSetError("get_chapter_url_from_href")

    @property
    def chapter_name(self):
        return self._chapter_name

    @chapter_name.setter
    def chapter_name(self, text):
        if hasattr(self, 'get_chapter_name') and callable(self.get_chapter_name):
            self._chapter_name = self.get_chapter_name(text)
        else:
            self._chapter_name = text

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

    @property
    def bookmark_pattern(self):
        if not self._bookmark_pattern:
            raise ValueNotSetError("bookmark_pattern")
        else:
            return self._bookmark_pattern

    @bookmark_pattern.setter
    def bookmark_pattern(self, pattern):
        self._bookmark_pattern = pattern

    @property
    def title_pattern(self):
        if not self._title_pattern:
            raise ValueNotSetError("title_pattern")
        else:
            return self._title_pattern

    @title_pattern.setter
    def title_pattern(self, pattern):
        self._title_pattern = pattern

    @property
    def author_pattern(self):
        if not self._author_pattern:
            raise ValueNotSetError("author_pattern")
        else:
            return self._author_pattern

    @author_pattern.setter
    def author_pattern(self, pattern):
        self._author_pattern = pattern

    @staticmethod
    def refine_text(text):
        text = text.replace('\r\n', '')
        text = text.replace('\r', '')
        text = text.replace('<br/>', '\n')
        text = text.replace('<p>', '')
        text = text.replace('</p>', '\n')
        text = re.sub(r'<.+>', '', text)
        text = text.strip('\n')
        text = text.strip(' ')
        text = text.strip('\t')
        text = re.sub(r'\n\s+\n', '\n\n', text)
        text = re.sub(r'\n+', '\n', text)
        return text

    @staticmethod
    def detect(buf):
        encoding = chardet.detect(buf).get('encoding')
        if encoding in ["GB2312", "GBK", "GB18030"]:
            return "GB18030"
        else:
            return encoding

    def get_index(self):
        req = self.get(self.index_url)
        if req.ok:
            self.encoding = self.detect(req.content)
            index = BeautifulSoup(req.content, from_encoding=self.encoding)
            return index
        else:
            req.raise_for_status()

    def reload(self):
        self._name = ''
        self._title = ''
        self._author = ''
        self._chapter_url_list = []
        self.index = self.get_index()

    def get_title_from_index(self):
        novel = self.index.title.text
        match = re.match(self.bookmark_pattern, novel)
        title = match.expand(self.title_pattern)
        return title

    def get_chapter_url_list(self):
        chapter_urls = self.index.find_all(href=re.compile(self.chapter_url_pattern))
        chapter_url_list = list(set(chapter_urls))
        chapter_url_list.sort(key=chapter_urls.index)
        return chapter_url_list

    def get_chapter(self):
        req = self.get(self.chapter_url)
        if req.ok:
            chapter = BeautifulSoup(req.content, from_encoding=self.encoding)
            content = chapter.find_all(attrs={self.search_type: self.search_text})
            text = self.refine_text(str(content))
            if hasattr(self, 'better_refine') and callable(self.better_refine):
                text = self.better_refine(text)
            return text
        else:
            if req.status_code == 502:
                print('HTPError: 502 Server Error: Bad Gateway')
                print('Retrying...')
                time.sleep(1)
                return self.get_chapter()
            else:
                req.raise_for_status()

    def download_chapter(self, filepath):
        text = self.get_chapter()
        with open(filepath, 'w') as fp:
            fp.write(text)

    def download_all(self):
        if not os.path.isdir(self.download_dir):
            os.makedirs(self.download_dir)
        for line in self.chapter_url_list:
            self.chapter_url = line['href']
            self.chapter_name = line.text
            filename = self.chapter_name + '.txt'
            filepath = os.path.join(self.download_dir, filename)
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                continue
            else:
                self.download_chapter(filepath)

    def download_test(self):
        target = self.chapter_url_list[-1]
        self.chapter_url = target['href']
        self.chapter_name = target.text
        filename = self.chapter_name + '.txt'
        self.download_chapter(filename)

    def get_chapter_test(self):
        target = self.chapter_url_list[-1]
        self.chapter_url = target['href']
        return self.get_chapter()
