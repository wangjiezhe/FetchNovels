#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from functools import wraps


def retry(ExceptionToTrack, tries=5, delay=5):
    def dec_retry(func):
        @wraps(func)
        def func_retry(*args, **kwargs):
            m_delay = delay
            for _ in range(tries):
                try:
                    return func(*args, **kwargs)
                except ExceptionToTrack as e:
                    print("Wait %d seconds to retry ..." % m_delay)
                    sleep(m_delay)
                    m_delay *= 2
            return func(*args, **kwargs)

        return func_retry

    return dec_retry
