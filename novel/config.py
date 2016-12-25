#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Some constants
"""

import json
import os
from random import randrange

GOAGENT = {'http': '127.0.0.1:8087'}
GOPROXY = {'http': '127.0.0.1:8088'}
GB = 'GB18030'
BIG = 'Big5'

UAS = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/51.0.2704.84 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/50.0.2661.76 YaBrowser/16.6.0.6383 (beta) Safari/537.36',
)

HOME_DIR = os.path.expanduser('~')
CACHE_DIR = os.path.join(HOME_DIR, '.cache', 'novel')
CACHE_DB = os.path.join(CACHE_DIR, 'cache.db')
NOVEL_LIST_JSON = os.path.join(CACHE_DIR, 'novel_list.json')


def get_headers():
    ua = UAS[randrange(len(UAS))]
    headers = {'User-Agent': ua}
    return headers


def check_first():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)


def load_novel_list():
    if not os.path.exists(NOVEL_LIST_JSON):
        return dict()

    with open(NOVEL_LIST_JSON) as fp:
        nl = json.load(fp)
    return nl


def update_novel_list(nl, source, tid):
    if source in nl:
        if tid not in nl[source]:
            nl[source].append(tid)
    else:
        nl[source] = [tid]
    return nl


def save_novel_list(nl):
    with open(NOVEL_LIST_JSON, 'w') as fp:
        json.dump(nl, fp, indent=2)


def update_and_save_novel_list(source, tid):
    nl = load_novel_list()
    nl = update_novel_list(nl, source, tid)
    save_novel_list(nl)
