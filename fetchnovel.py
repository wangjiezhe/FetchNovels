#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

from novel import cli, config


def main():
    source = sys.argv[1]
    tids = sys.argv[2:]

    need_fix = re.match(r'(\d+)(.+)', source)
    if need_fix:
        source = '{g[1]}{g[0]}'.format(g=need_fix.groups())

    print('{}: {}'.format(source, tids))
    if len(tids) == 0:
        print('No specific tid!')
        sys.exit(1)

    config.check_first()

    for tid in tids:
        cli.dump_novel(source, tid)


if __name__ == '__main__':
    main()
