#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from abc import abstractmethod
from enum import Enum
from multiprocessing.dummy import Pool
from urllib.error import HTTPError
from urllib.parse import urljoin

from lxml.etree import XMLSyntaxError
from pyquery import PyQuery as Pq

from .base import BaseNovel
from .decorators import retry
from .error import PropertyNotSetError, ValueNotSetError
from .utils import get_base_url, fix_order, SqlHelper, get_filename


class Page(BaseNovel):

    running = False

    def __init__(self, url, title, selector,
                 headers=None, proxies=None,
                 encoding=None, tool=None):
        super().__init__(url, headers, proxies, encoding, tool)
        self.title = title
        self.selector = selector

    def run(self):
        self.refine = self.tool().refine
        self.doc = self.get_doc()
        self.running = True

    def confirm_run(self):
        if not self.running:
            self.run()

    @retry((HTTPError, XMLSyntaxError))
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_content(self):
        self.confirm_run()
        if self.selector is None:
            return ''
        content = self.doc(self.selector).html()
        content = self.refine(content)
        return content

    def dump(self, path=None, folder=None, num=None):
        self.confirm_run()
        if path is None:
            if num is not None:
                pre = '「{:d}」'.format(num)
            else:
                pre = ''
            name = '{}{}.txt'.format(pre, self.title)
            if folder is None:
                path = os.path.join(os.getcwd(), name)
            else:
                path = os.path.join(folder, name)
        print(self.title)
        with open(path, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n')
            fp.write(self.get_content())


class IntroPage(BaseNovel):

    running = False

    def __init__(self, url, selector,
                 headers=None, proxies=None, encoding=None,
                 tool=None):
        super().__init__(url, headers, proxies, encoding, tool)
        self.selector = selector

    def run(self):
        self.refine = self.tool().refine
        self.doc = self.get_doc()
        self.running = True

    def confirm_run(self):
        if not self.running:
            self.run()

    @retry((HTTPError, XMLSyntaxError))
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    def get_content(self):
        self.confirm_run()
        if self.selector is None:
            return ''
        intro = self.doc(self.selector).html()
        intro = self.refine(intro)
        return intro

    def dump(self, overwrite=True):
        self.confirm_run()
        filename = 'intro.txt'
        print('intro')
        with open(filename, 'w') as fp:
            fp.write('简介')
            fp.write('\n\n\n\n')
            fp.write(self.get_content())


class ChapterType(Enum):
    whole = 1
    path = 2
    last = 3
    last_rev = 4


class SerialNovel(BaseNovel):

    running = False

    def __init__(self, url, cont_sel,
                 intro_url=None, intro_sel=None,
                 chap_sel=None, chap_type=None):
        super().__init__(url)
        self.cont_sel = cont_sel
        self.intro_url = intro_url
        self.intro_sel = intro_sel
        self.page = Page
        self.intro_page = IntroPage
        self.chap_sel = chap_sel
        self.chap_type = chap_type

    def run(self, refresh=False):
        if self.running and not refresh:
            return
        self.refine = self.tool().refine
        self.doc = self.get_doc()
        self.title, self.author = self.get_title_and_author()

        self.db = SqlHelper(':memory:')
        self.db.create_table('''CREATE TABLE chapters
                                (id INTEGER PRIMARY KEY,
                                 url TEXT,
                                 title NTEXT,
                                 text NTEXT)''')
        self.db.insert_many_data('INSERT INTO chapters(id, url, title) VALUES (?, ?, ?)',
                                 self.chapter_list)

        self.db.insert_data('INSERT INTO chapters VALUES (?, ?, ?, ?)',
                            (-1, self.intro_url or self.url, 'Introduction', self.get_intro()))

        cursors = self.db.select_data('SELECT id, url, title FROM chapters WHERE text IS NULL')
        with Pool(100) as p:
            p.starmap(self.update_chapter, cursors.fetchall())

        self.running = True

    def update_chapter(self, i, url, title):
        print(title)
        page = self.page(
            url, title, self.cont_sel,
            self.headers, self.proxies,
            self.encoding, self.tool
        )
        content = page.get_content()
        self.db.update_data('UPDATE chapters SET text=? WHERE id=?', (content, i))

    def close(self):
        self.db.close()
        self.running = False

    @retry((HTTPError, XMLSyntaxError))
    def get_doc(self):
        return Pq(url=self.url, headers=self.headers,
                  proxies=self.proxies, encoding=self.encoding)

    @abstractmethod
    def get_title_and_author(self):
        pass

    @property
    def chapter_list(self):
        if self.chap_sel and self.chap_type:
            return self.chapter_list_with_sel(self.chap_sel, self.chap_type)
        raise PropertyNotSetError('chapter_list')

    def chapter_list_with_sel(self, selector, chap_type):
        clist = self.doc(selector).filter(
            lambda i, e: Pq(e)('a').attr('href')
        )
        if chap_type == ChapterType.whole:
            clist = clist.map(
                lambda i, e: (i,
                              Pq(e)('a').attr('href'),
                              Pq(e).text())
            )
        elif chap_type == ChapterType.path:
            clist = clist.map(
                lambda i, e: (i,
                              urljoin(get_base_url(self.url),
                                      Pq(e)('a').attr('href')),
                              Pq(e).text())
            )
        elif chap_type == ChapterType.last:
            clist = clist.map(
                lambda i, e: (i,
                              urljoin(self.url, Pq(e)('a').attr('href')),
                              Pq(e).text())
            )
        elif chap_type == ChapterType.last_rev:
            clist = clist.map(
                lambda i, e: (fix_order(i),
                              urljoin(self.url, Pq(e)('a').attr('href')),
                              Pq(e).text())
            )
            clist.sort(key=lambda s: int(s[0]))
        else:
            raise ValueNotSetError("chap_type")
        return clist

    @retry(HTTPError)
    def get_intro(self):
        if self.intro_url is None:
            if self.intro_sel is None:
                return ''
            intro = self.doc(self.intro_sel).html()
            intro = self.refine(intro)
            return intro
        else:
            intro_page = self.intro_page(
                self.intro_url, self.intro_sel,
                self.headers, self.proxies, self.encoding,
                self.tool)
            intro = intro_page.get_content()
            return intro

    @property
    def download_dir(self):
        return os.path.join(os.getcwd(),
                            "《{self.title}》{self.author}".format(self=self))

    def _dump_split(self):
        download_dir = self.download_dir
        if not os.path.isdir(download_dir):
            os.makedirs(download_dir)
        print('《{self.title}》{self.author}'.format(self=self))

        cursors = self.db.select_data('SELECT * FROM chapters')
        for i, _, title, text in cursors:
            if title == 'Introduction':
                filename = '{}.txt'.format(title)
            else:
                filename = '「{:d}」{}.txt'.format(i,title)
            path = os.path.join(download_dir, filename)
            with open(path, 'w') as fp:
                fp.write(title)
                fp.write('\n\n\n\n')
                fp.write(text)
                fp.write('\n')

    def dump_split(self):
        self.run()
        self._dump_split()
        self.close()

    def _dump(self, overwrite=True):
        if overwrite:
            filename = '《{self.title}》{self.author}.txt'.format(self=self)
        else:
            filename = get_filename(self.title, self.author)
        print(filename)

        with open(filename, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n')
            fp.write(self.author)

            fp.write('\n\n\n')
            cursor = self.db.select_data('SELECT text FROM chapters WHERE id=-1')
            intro = cursor.fetchone()[0]
            fp.write(intro)

            cursors = self.db.select_data('SELECT * FROM chapters WHERE id>=0')
            for i, _, title, text in cursors:
                fp.write('\n\n\n\n')
                fp.write(title)
                fp.write('\n\n\n')
                fp.write(text)
                fp.write('\n')

    def dump(self, overwrite=True):
        self.run()
        self._dump(overwrite=overwrite)
        self.close()
