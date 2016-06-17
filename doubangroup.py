#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from novel import base, utils, config, models

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


class DoubanGroup(base.BaseNovel):

    def __init__(self, topic_id):
        super().__init__(utils.base_to_url(BASE_URL, topic_id),
                         tid=topic_id, cache=True)
        self.comments_url = utils.base_to_url(COMMENTS_URL, topic_id)

        self.req = self.session = None
        self.content = ''

    def run(self, refresh=True):
        self.req = requests.get(
            self.url, headers=self.headers, proxies=self.proxies
        ).json()
        if self.cache:
            self.session = utils.connect_database(config.CACHE_DB)
            self._add_website()
            self._add_article()
        else:
            self.content = self.get_content()
        self.running = True

    # noinspection PyArgumentList
    def _add_website(self):
        website = self.session.query(models.Website).filter_by(
            name=self.get_source()
        ).first()

        if not website:
            website = models.Website(name=self.get_source(), url=WEBSITE_URL)
            self.session.add(website)

    # noinspection PyArgumentList
    def _add_article(self):
        article = self.session.query(models.Article).filter_by(
            id=self.tid, source=self.get_content()
        ).first()

        if not article:
            article = models.Article(id=self.tid, title=self.title,
                                     text=self.get_content(), source=self.get_source())
            self.session.add(article)

    @property
    def title(self):
        return self.req['title']

    @property
    def author_id(self):
        return self.req['author']['id']

    @property
    def num_comments(self):
        return self.req['comments_count']

    @staticmethod
    def refine(text):
        text = text.replace('\r\n', '\n')
        return text

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

    def dump(self, overwrite=True):
        self.run()
        print(self.title)
        filename = '{self.title}.txt'.format(self=self)
        filename = filename.replace('/', '_')
        if self.cache:
            content = self.session.query(models.Article).filter_by(
                id=self.tid, source=self.get_source()
            ).one().text
        else:
            content = self.content
        with open(filename, 'w') as fp:
            fp.write(content)


def main():
    utils.in_main(DoubanGroup)

if __name__ == '__main__':
    main()
