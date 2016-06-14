#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Some constants
"""

import os

GOAGENT = {'http': '127.0.0.1:8087'}
GB = 'GB18030'

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

def check_first():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)