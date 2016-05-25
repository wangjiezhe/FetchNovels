#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from novel import utils

BASE_URL = 'https://api.douban.com/v2/group/topic/{}/'  # id
COMMENTS_URL = BASE_URL + 'comments'
PER_PAGE_COUNT = 100

HEADERS = {
    'Host': 'api.douban.com',
    'Referer': 'api.douban.com',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.101 Safari/537.36'
}


class DoubanGroup(object):

    def __init__(self, topic_id, proxies=None):
        self.topic_url = utils.base_to_url(BASE_URL, topic_id)
        self.comments_url = utils.base_to_url(COMMENTS_URL, topic_id)
        self.req = requests.get(self.topic_url, headers=HEADERS).json()

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
                self.comments_url, headers=HEADERS, params=params
            ).json()
            for c in req['comments']:
                if c['author']['id'] != self.author_id:
                    continue
                content_list.append(self.refine(c['text']))

        content = '\n\n\n\n'.join(content_list)
        return content

    def dump(self, overwrite=True):
        print(self.title)
        filename = '{self.title}.txt'.format(self=self)
        filename = filename.replace('/', '_')
        with open(filename, 'w') as fp:
            fp.write(self.get_content())


def main():
    utils.in_main(DoubanGroup)

if __name__ == '__main__':
    main()
