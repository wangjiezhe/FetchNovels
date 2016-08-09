#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Get novels in the bookcase of websites which powered by `JIEQI CMS`
"""

import os
import sys
from urllib.parse import quote, urlparse, parse_qs

from pyquery import PyQuery

from novel import config, cli, utils

ENCODING = config.GB

BOOKCASE_URL = {
    'yq33': 'http://www.33yq.com/wodeshujia.aspx',
    'piaotian': 'http://www.piaotian.net/modules/article/bookcase.php',
    'biquge': 'http://www.biquge.la/modules/article/bookcase.php',
}


def get_token(source):
    token_file = os.path.join(config.CACHE_DIR, '{}.token'.format(source))
    with open(token_file) as fp:
        token_list = fp.readlines()
    token_list = [t.strip() for t in token_list]
    return 'jieqiUserName={t[0]},jieqiUserPassword={t[1]}'.format(t=token_list)


def get_tids(source):
    cookies = {'jieqiUserInfo': quote(get_token(source), encoding=ENCODING)}
    try:
        url = BOOKCASE_URL[source]
    except KeyError:
        raise NotImplementedError(source)
    doc = PyQuery(url, headers=config.get_headers(), encoding=ENCODING,
                  proxies=utils.get_proxies(source), cookies=cookies)
    tid_list = doc('td.even a').filter(
        lambda i, e: PyQuery(e).attr('href').startswith('http')
    ).map(
        lambda i, e: PyQuery(e).attr('href')
    ).map(
        lambda i, e: parse_qs(urlparse(e).query)['aid']
    )
    return tid_list


def sync():
    source = sys.argv[1]
    tids = get_tids(source)
    print('{}: {}'.format(source, list(tids)))
    with cli.NovelFactory(source, tids) as fac:
        fac.update()


if __name__ == '__main__':
    sync()
