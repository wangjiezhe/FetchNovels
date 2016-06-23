#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from novel import sources, config


def main():
    source = sys.argv[1]
    tids = sys.argv[2:]
    print('{}: {}'.format(source, tids))
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)

    novel_class = getattr(sources, source.capitalize())

    def dump(t):
        nov = novel_class(t)
        if source in sources.USE_PROXIES:
            nov.proxies = config.GOAGENT
        nov.dump()

    config.check_first()

    # num = len(tids)
    # with Pool(num) as p:
    #     p.map(dump, tids)
    for tid in tids:
        dump(tid)


if __name__ == '__main__':
    main()
