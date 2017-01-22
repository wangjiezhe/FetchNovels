#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from novel import base, utils, models, db

BASE_URL = 'https://api.douban.com/v2/group/topic/{}/'  # id
COMMENTS_URL = BASE_URL + 'comments'
PER_PAGE_COUNT = 100

WEBSITE_URL = 'https://www.douban.com/group/'

HEADERS = {
    'Host': 'api.douban.com',
    'Referer': 'api.douban.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36'
}


def refine(text):
    text = text.replace('\r\n', '\n')
    return text


class Doubangroup(base.BaseNovel):

    def __init__(self, topic_id):
        super().__init__(utils.base_to_url(BASE_URL, topic_id),
                         tid=topic_id, cache=True)
        self.comments_url = utils.base_to_url(COMMENTS_URL, topic_id)

        self.req = self.session = None
        self.use_exist_session = False
        self.author_id = self.content = ''
        self.num_comments = 0

    def use_session(self, s):
        if s:
            self.session = s
            self.use_exist_session = True

    def run(self, refresh=True):
        if self.running and not refresh:
            return
        self.refine = refine
        self.req = requests.get(
            self.url, headers=self.headers, proxies=self.proxies
        ).json()
        self.title = self.req['title']
        self.author_id = self.req['author']['id']
        self.num_comments = self.req['comments_count']
        print(self.title)
        if self.cache:
            if not self.use_exist_session:
                self.session = db.new_session()
            self._add_website()
            self._add_article()
            self.session.flush()
        else:
            self.content = self.get_content()
        self.running = True

    def close(self):
        if self.cache and not self.use_exist_session:
            self.session.close()
        self.running = False

    # noinspection PyArgumentList
    def _add_website(self):
        website = self.session.query(models.Website).filter_by(
            name=self.source
        ).first()

        if not website:
            website = models.Website(name=self.source, url=WEBSITE_URL)
            self.session.add(website)

    # noinspection PyArgumentList
    def _add_article(self):
        article = self.session.query(models.Article).filter_by(
            id=self.tid, source=self.source
        ).first()

        if not article:
            article = models.Article(id=self.tid, title=self.title,
                                     text=self.get_content(), source=self.source)
            self.session.add(article)

    def get_content(self):
        content_list = [self.refine(self.req['content'])]

        for i in range(self.num_comments // PER_PAGE_COUNT + 1):
            params = {
                'start': i * PER_PAGE_COUNT,
                'count': PER_PAGE_COUNT
            }
            req = requests.get(
                self.comments_url, headers=self.headers,
                proxies=self.proxies, params=params
            ).json()
            for c in req['comments']:
                if c['author']['id'] != self.author_id:
                    continue
                content_list.append(self.refine(c['text']))

        content = '\n\n\n\n'.join(content_list)
        return content

    def dump(self):
        filename = utils.get_filename(self.title, overwrite=self.overwrite)
        filename = filename.replace('/', '_')
        print(filename)
        if self.cache:
            content = self.session.query(models.Article).filter_by(
                id=self.tid, source=self.source
            ).one().text
        else:
            content = self.content
        with open(filename, 'w') as fp:
            fp.write(content)

    def dump_and_close(self):
        self.run()
        self.dump()
        self.close()
