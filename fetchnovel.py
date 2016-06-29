#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import sys

from novel import __version__
from novel import cli, config


class MyParser(argparse.ArgumentParser):

    def __init__(self):
        super().__init__(
            description='Fetch novels from Internet.'
        )
        self.add_argument('-V', '--version', action='version',
                          version=__version__)
        self.add_argument('-u', '--update-all', action='store_true',
                          help='update novels in the database')
        self.add_argument('-l', '--list-all', action='store_true',
                          help='list novels in the database')
        self.add_argument('-v', '--verbose', action='count')
        self.add_argument('-d', '--download-only', action='store_true',
                          help='download novel into database without write it to file')
        self.add_argument('source', nargs='?')
        self.add_argument('tid', nargs='*')


def main():
    parser = MyParser()
    args = parser.parse_args()

    if args.update_all:
        cli.update_novels()
    elif args.list_all:
        if not args.verbose:
            cli.list_novels()
        elif args.verbose == 1:
            cli.list_novels(show_intro=True)
        else:
            cli.list_novels(show_intro=True, show_finish=True)
    elif args.source:
        need_fix = re.match(r'(\d+)(.+)', args.source)
        if need_fix:
            source = '{g[1]}{g[0]}'.format(g=need_fix.groups())
        else:
            source = args.source

        print('{}: {}'.format(source, args.tid))
        if len(args.tid) == 0:
            print('No specific tid!')
            sys.exit(1)

        config.check_first()

        if args.download_only:
            for tid in args.tid:
                cli.update_novels(source, tid)
        else:
            for tid in args.tid:
                cli.dump_novel(source, tid)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
