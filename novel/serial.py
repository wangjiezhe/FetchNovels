#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from enum import Enum
from multiprocessing.dummy import Pool
from urllib.parse import urljoin

from pyquery import PyQuery
from termcolor import colored

from novel.base import BaseNovel, SinglePage
from novel.db import new_session
from novel.models import Serial, Chapter, Website
from novel.utils import get_base_url, get_filename


class Page(SinglePage):

    def __init__(self, url, title, selector,
                 headers=None, proxies=None,
                 encoding='UTF-8', tool=None):
        super().__init__(url, selector, headers, proxies, encoding, tool)
        self.title = title

    def dump(self, path=None, folder=None, num=None):
        if not path:
            if num is not None:
                pre = '「{:d}」'.format(num)
            else:
                pre = ''
            filename = '{}{}'.format(
                pre, get_filename(self.title, overwrite=self.overwrite))
            if not folder:
                path = os.path.join(os.getcwd(), filename)
            else:
                path = os.path.join(folder, filename)
        print(self.title)
        with open(path, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n\n')
            fp.write(self.content)
            fp.write('\n')

    def dump_and_close(self, path=None, folder=None, num=None):
        self.run()
        self.dump(path, folder, num)


class IntroPage(SinglePage):

    def __init__(self, url, selector,
                 headers=None, proxies=None, encoding='UTF-8',
                 tool=None):
        super().__init__(url, selector, headers, proxies, encoding, tool)
        self.title = 'Introduction'


class ChapterType(Enum):
    whole = 1
    path = 2
    last = 3


class SerialNovel(BaseNovel):

    def __init__(self, url, cont_sel=None,
                 intro_url=None, intro_sel=None,
                 chap_type=None, chap_sel=None,
                 tid=None, cache=True):
        super().__init__(url, tid=tid, cache=cache)
        self.cont_sel = cont_sel
        self.intro_url = intro_url
        self.intro_sel = intro_sel
        self.page = Page
        self.intro_page = IntroPage
        self.chap_type = chap_type
        self.chap_sel = chap_sel

        self.finish = False
        self.session = None
        self.use_exist_session = False

    def use_session(self, s):
        if s:
            self.session = s
            self.use_exist_session = True

    def run(self, refresh=False):
        super().run(refresh=refresh)
        self.title, self.author = self.get_title_and_author()
        print(colored(self.title, 'green'), self.author)

        if self.cache:
            if not self.use_exist_session:
                self.session = new_session()
            self._add_website()
            self._add_novel()
            self._update_chapters()
            self.session.flush()

    # noinspection PyArgumentList
    def _add_website(self):
        website = self.session.query(Website).filter_by(
            name=self.source
        ).first()

        if not website:
            website = Website(name=self.source,
                              url=get_base_url(self.url))
            self.session.add(website)

    # noinspection PyArgumentList
    def _add_novel(self):
        if self.tid is not None:
            novel = self.session.query(Serial).filter_by(
                id=self.tid, source=self.source
            ).first()
        else:
            novel = None

        if not novel:
            novel = Serial(id=self.tid, title=self.title, author=self.author,
                           intro=self.get_intro(), source=self.source)
            self.session.add(novel)

            novel.chapters = [Chapter(id=tid, title=title, url=url)
                              for tid, url, title in self.chapter_list]
        else:
            old_chapters_ids = self.session.query(Chapter.id).filter_by(
                novel_id=self.tid, novel_source=self.source
            ).all()
            old_chapters_ids = list(*zip(*old_chapters_ids))
            novel.chapters.extend(
                [Chapter(id=cid, title=title, url=url)
                 for cid, url, title in self.chapter_list
                 if cid not in old_chapters_ids])

        if self.finish:
            novel.finish = True

    def _update_chapters(self):
        empty_chapters = self.session.query(Chapter).filter_by(
            novel_id=self.tid, novel_source=self.source
        ).filter(Chapter.text.is_(None))

        with Pool(100) as p:
            p.map(self._update_chapter, empty_chapters, 10)

    def _update_chapter(self, ch):
        print(ch.title)
        page = self.page(
            ch.url, ch.title, self.cont_sel,
            None, self.proxies, self.encoding,
            self.tool
        )
        page.run()
        ch.text = page.content

    def close(self):
        if self.cache and not self.use_exist_session:
            self.session.close()
        self.running = False

    def get_title_and_author(self):
        raise NotImplementedError('get_title_and_author')

    @property
    def chapter_list(self):
        if self.chap_sel and self.chap_type:
            return self._chapter_list_with_sel(self.chap_sel, self.chap_type)
        raise NotImplementedError('chapter_list')

    def _chapter_list_with_sel(self, selector, chap_type):
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
        else:
            raise NameError('chap_type')
        return clist

    def get_intro(self):
        if not self.intro_url:
            if not self.intro_sel:
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

        if self.cache:
            intro = self.session.query(Serial).filter_by(
                id=self.tid, source=self.source
            ).one().intro
        else:
            intro = self.get_intro()
        path = os.path.join(download_dir, 'Introduction.txt')
        with open(path, 'w') as fp:
            fp.write('Introduction')
            fp.write('\n\n\n\n')
            fp.write(intro)
            fp.write('\n')

        if self.cache:
            novel = self.session.query(Serial).filter_by(
                id=self.tid, source=self.source
            ).one()
            for ch in novel.chapters:
                filename = '「{:d}」{}.txt'.format(ch.id + 1, ch.title)
                path = os.path.join(download_dir, filename)
                with open(path, 'w') as fp:
                    fp.write(ch.title)
                    fp.write('\n\n\n\n')
                    fp.write(ch.text)
                    fp.write('\n')
        else:
            for i, url, title in self.chapter_list:
                self._dump_chapter(url, title, i + 1)

    def _dump_chapter(self, url, title, num):
        page = self.page(
            url, title, self.cont_sel,
            None, self.proxies, self.encoding,
            self.tool)
        page.dump_and_close(folder=self.download_dir, num=num)

    def dump_split(self):
        self.run()
        self._dump_split()
        self.close()

    def dump(self):
        filename = get_filename(self.title, self.author, self.overwrite)
        print(filename)

        with open(filename, 'w') as fp:
            fp.write(self.title)
            fp.write('\n\n')
            fp.write(self.author)

            fp.write('\n\n\n')
            if self.cache:
                novel = self.session.query(Serial).filter_by(
                    id=self.tid, source=self.source
                ).one()
                fp.write(novel.intro)
                for ch in novel.chapters:
                    fp.write('\n\n\n\n')
                    fp.write(ch.title)
                    fp.write('\n\n\n')
                    fp.write(ch.text)
                    fp.write('\n')
            else:
                fp.write(self.get_intro())
                for _, url, title in self.chapter_list:
                    fp.write('\n\n\n\n')
                    fp.write(title)
                    fp.write('\n\n\n')
                    fp.write(self._get_chapter(url, title))
                    fp.write('\n')

    def _get_chapter(self, url, title):
        print(title)
        page = self.page(
            url, title, self.cont_sel,
            None, self.proxies, self.encoding,
            self.tool
        )
        page.run()
        return page.content

    def dump_and_close(self):
        self.run()
        if self.cache:
            self.update_novel_list()
        self.dump()
        self.close()
