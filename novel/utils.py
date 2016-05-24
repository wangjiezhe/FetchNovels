#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Some help functions
"""

import re
import sys
from urllib.parse import urlparse, urlunparse


class Tool(object):
    """
    A class to remove needless tags and strings
    """

    def __init__(self):
        self._remove_a = re.compile(r'<a.*?>.*?</a>', re.I)
        self._remove_div = re.compile(r'<div.*?>.*?</div>',
                                      re.I | re.S)
        self._remove_span = re.compile(r'<span.*?>.*?</span>', re.I)
        self._remove_script = re.compile(r'<script.*?>.*?</script>',
                                         re.I | re.S)
        self._replace_br = re.compile(r'<br\s*/\s*>|</\s*br>', re.I)
        self._replace_p = re.compile(r'</?p>', re.I)
        self._replace_xa0 = re.compile(r'\xa0')
        self._replace_u3000 = re.compile(r'\u3000')
        self._remove_ufeff = re.compile(r'\ufeff')
        self._remove_r = re.compile(r'&#13;|\r')
        self.replace_extras = []
        self.remove_extras = []
        self._remove_ot = re.compile(r'<.*?>')

    def replace(self, text):
        """
        Replace and remove needless strings

        Some default options are pre-defined.
        You can add custom options to replace_extras or remove_extras.

        :param text: The original text
        :return: The corrected text
        """
        text = re.sub(self._remove_a, '', text)
        text = re.sub(self._remove_div, '', text)
        text = re.sub(self._remove_script, '', text)
        text = re.sub(self._replace_br, '\n', text)
        text = re.sub(self._replace_p, '\n', text)
        text = re.sub(self._replace_xa0, ' ', text)
        text = re.sub(self._replace_u3000, '  ', text)
        text = re.sub(self._remove_ufeff, '', text)
        text = re.sub(self._remove_r, '', text)
        for s, d in self.replace_extras:
            text = re.sub(s, d, text)
        for pat in self.remove_extras:
            text = re.sub(pat, '', text)
        text = re.sub(self._remove_ot, '', text)
        return text

    def refine(self, text):
        """
        Get a better printed text

        Replace and remove needless strings, and then
        remove too many continuous newlines.

        :param text: The original text
        :return: The corrected text
        """
        text = self.replace(text)

        text = re.sub(r'\n\s+\n', '\n\n', text)

        return text.strip()


def fix_order(i):
    """
    Fix the order of list item.

    Sometimes we get a list of order
    [0<2>, 1<1>, 2<0>, 3<5>, 4<4>, 5<3>, ...],
    and what we need is [2<0>, 1<1>, 0<2>, 5<3>, 4<4>, 3<5>, ...].

    :param i: The original index
    :return: The correct index
    """
    if i % 3 == 0:
        return i + 2
    elif i % 3 == 2:
        return i - 2
    else:
        return i


def base_to_url(base_url, tid):
    """
    Get the url from template

    The base_url must have two replacement fields.
    The second field is just filled with the tid,
    while the first field with the tid which has been
    stripped the last three number.

    :param base_url: The url template
    :param tid: A number or string of numbers
    :return: the correct url
    """
    tid = str(tid)
    return base_url % (tid[:-3] if tid[:-3] != '' else 0, tid)


def get_base_url(url):
    """
    Transform a full url into its base url

    Eg: 'http://example.com/text/file?var=f' -> 'http://example.com'

    :param url: A full url
    :return: The base url
    """
    result = urlparse(url)
    base_url = urlunparse((result.scheme, result.netloc, '', '', '', ''))
    return base_url


def in_main(NovelClass, proxies=None):
    """
    A pre-defined main function

    Get tids for command line parameters, and save content in each files.

    :param NovelClass: The class to get content
    :param proxies: proxy to use
    """
    tids = sys.argv[1:]
    print(tids)
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)
    for tid in tids:
        nov = NovelClass(tid, proxies=proxies)
        nov.dump()
