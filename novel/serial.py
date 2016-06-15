#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
# from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from multiprocessing.dummy import Pool
from urllib.error import HTTPError
from urllib.parse import urljoin

from pyquery import PyQuery

from .config import CACHE_DB
from .models import Novel, Chapter
from .base import BaseNovel, SinglePage
from .decorators import retry
from .utils import get_base_url, fix_order, get_filename, connect_database


class Page(SinglePage):

    def __init__(self, url, title, selector,
                 headers=None, proxies=None,
                 encoding=None, tool=None):
        super().__init__(url, selector, headers, proxies, encoding, tool)
        self.title = title

    def dump(self, overwrite=True, path=None, folder=None, num=None):
        self.run()
        if path is None:
            if num is not None:
                pre = '「{:d}」'.format(num)
            else:
                pre = ''
            filename = '{}{}'.format(
                pre, get_filename(self.title, overwrite=overwrite))
            if folder is None:
                path = os.path.join(os.getcwd(), filename)
            else:
                path = os.path.join(folder, filename)
        print(self.title)
        with open(path, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n')
            fp.write(self.content)
            fp.write('\n')


class IntroPage(SinglePage):

    def __init__(self, url, selector,
                 headers=None, proxies=None, encoding=None,
                 tool=None):
        super().__init__(url, selector, headers, proxies, encoding, tool)
        self.title = 'Introduction'


class ChapterType(Enum):
    whole = 1
    path = 2
    last = 3
    last_rev = 4


class SerialNovel(BaseNovel):

    def __init__(self, url, cont_sel,
                 intro_url=None, intro_sel=None,
                 chap_sel=None, chap_type=None,
                 tid=None):
        super().__init__(url)
        self.tid = tid
        self.cont_sel = cont_sel
        self.intro_url = intro_url
        self.intro_sel = intro_sel
        self.page = Page
        self.intro_page = IntroPage
        self.chap_sel = chap_sel
        self.chap_type = chap_type

        self.session = None

    @classmethod
    def get_source(cls):
        return cls.__name__.lower()

    def new_tid(self):
        return self.session.query(Novel).filter(Novel.id < 0).count() - 1

    def run(self, refresh=False, parallel=True):
        super().run(refresh=refresh)
        self.title, self.author = self.get_title_and_author()

        self.session = connect_database(CACHE_DB)

        if self.tid is not None:
            novel = self.session.query(Novel).filter_by(
                id=self.tid, source=self.get_source()
            ).first()
        else:
            novel = None
            self.tid = self.new_tid()

        if novel is None:
            # noinspection PyArgumentList
            novel = Novel(id=self.tid, title=self.title, author=self.author,
                          intro=self.get_intro(), source=self.get_source())
            self.session.add(novel)

            # noinspection PyArgumentList
            novel.chapters = [Chapter(id=tid, title=title, url=url)
                              for tid, url, title in self.chapter_list]
        else:
            old_chapters_ids = self.session.query(Chapter.id).filter_by(
                novel_id=self.tid, novel_source=self.get_source()
            ).all()
            old_chapters_ids = list(*zip(*old_chapters_ids))
            # noinspection PyArgumentList
            novel.chapters.extend(
                [Chapter(id=cid, title=title, url=url)
                 for cid, url, title in self.chapter_list
                 if cid not in old_chapters_ids])

        empty_chapters = \
            self.session.query(Chapter).filter(Chapter.text.is_(None))

        if parallel:
            # with ThreadPoolExecutor(100) as e:
            #     e.map(self.update_chapter, empty_chapters)
            with Pool(100) as p:
                p.map(self.update_chapter, empty_chapters, 10)
        else:
            for ch in empty_chapters:
                self.update_chapter(ch)

    def update_chapter(self, ch):
        print(ch.title)
        page = self.page(
            ch.url, ch.title, self.cont_sel,
            None, self.proxies,
            self.encoding, self.tool
        )
        page.run()
        ch.text = page.content

    def close(self):
        self.session.close()
        self.running = False

    def get_title_and_author(self):
        return NotImplementedError('get_title_and_author')

    @property
    def chapter_list(self):
        if self.chap_sel and self.chap_type:
            return self.chapter_list_with_sel(self.chap_sel, self.chap_type)
        raise NotImplementedError('chapter_list')

    def chapter_list_with_sel(self, selector, chap_type):
        clist = self.doc(selector).filter(
            lambda i, e: PyQuery(e)('a').attr('href')
        )
        if chap_type == ChapterType.whole:
            clist = clist.map(
                lambda i, e: (i,
                              PyQuery(e)('a').attr('href'),
                              PyQuery(e).text())
            )
        elif chap_type == ChapterType.path:
            clist = clist.map(
                lambda i, e: (i,
                              urljoin(get_base_url(self.url),
                                      PyQuery(e)('a').attr('href')),
                              PyQuery(e).text())
            )
        elif chap_type == ChapterType.last:
            clist = clist.map(
                lambda i, e: (i,
                              urljoin(self.url, PyQuery(e)('a').attr('href')),
                              PyQuery(e).text())
            )
        elif chap_type == ChapterType.last_rev:
            clist = clist.map(
                lambda i, e: (fix_order(i),
                              urljoin(self.url, PyQuery(e)('a').attr('href')),
                              PyQuery(e).text())
            )
            clist.sort(key=lambda s: int(s[0]))
        else:
            raise NameError('chap_type')
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
                None, self.proxies, self.encoding,
                self.tool)
            intro_page.run()
            return intro_page.content

    @property
    def download_dir(self):
        return os.path.join(os.getcwd(),
                            '《{self.title}》{self.author}'.format(self=self))

    def _dump_split(self):
        download_dir = self.download_dir
        if not os.path.isdir(download_dir):
            os.makedirs(download_dir)
        print('《{self.title}》{self.author}'.format(self=self))

        intro = self.session.query(Novel).filter_by(
            id=self.tid, source=self.get_source()
        ).one().intro
        path = os.path.join(download_dir, 'Introduction.txt')
        with open(path, 'w') as fp:
            fp.write('Introduction')
            fp.write('\n\n\n\n')
            fp.write(intro)
            fp.write('\n')

        chapters = self.session.query(Chapter).all()
        for ch in chapters:
            filename = '「{:d}」{}.txt'.format(ch.id, ch.title)
            path = os.path.join(download_dir, filename)
            with open(path, 'w') as fp:
                fp.write(ch.title)
                fp.write('\n\n\n\n')
                fp.write(ch.text)
                fp.write('\n')

    def dump_split(self):
        self.run()
        self._dump_split()
        self.close()

    def _dump(self, overwrite=True):
        filename = get_filename(self.title, self.author, overwrite)
        print(filename)

        with open(filename, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n')
            fp.write(self.author)

            fp.write('\n\n\n')
            intro = self.session.query(Novel).filter_by(
                id=self.tid, source=self.get_source()
            ).one().intro
            fp.write(intro)

            chapters = self.session.query(Chapter).all()
            for ch in chapters:
                fp.write('\n\n\n\n')
                fp.write(ch.title)
                fp.write('\n\n\n')
                fp.write(ch.text)
                fp.write('\n')

    def dump(self, overwrite=True):
        self.run()
        self._dump(overwrite=overwrite)
        self.close()
