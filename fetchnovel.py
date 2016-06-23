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
    overwrite = source in sources.DEFAULT_USE_OVERWRITE

    def dump(t):
        nov = novel_class(t)
        if source in sources.DEFAULT_USE_PROXIES:
            nov.proxies = config.GOAGENT
        nov.dump(overwrite=overwrite)

    config.check_first()

    for tid in tids:
        dump(tid)


if __name__ == '__main__':
    main()
