#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import sys
import textwrap

from novel import __version__
from novel import cli, config


class MyParser(argparse.ArgumentParser):

    def __init__(self):
        description = textwrap.dedent("""\
            Fetch novels from Internet, and write into file.

            Available sources:
              bgif2, biquge, dzxsw, feizw, haxtxt, klxsw, lwxs, lwxs520, lwxsw,
              piaotian, piaotiancc, ranwen, shu69, shushu8, sto, ttshuba,
              ttzw, ttzw5, uks5, wodexiaoshuo, xs365, yfzww, yq33, zhaishu8,
              cool18, sdragon, sis, doubangroup, ...
        """)
        super().__init__(
            description=description,
            formatter_class=argparse.RawTextHelpFormatter
        )
        self.add_argument('-V', '--version', action='version',
                          version=__version__)
        self.add_argument('-u', '--update-all', action='store_true',
                          help='update novels in the database')
        self.add_argument('-l', '--list-all', action='store_true',
                          help='list novels in the database')
        self.add_argument('-v', '--verbose', action='count',
                          help='show in more detail')
        self.add_argument('-d', '--download-only', action='store_true',
                          help='download novel into database without write it to file')
        self.add_argument('source', nargs='?',
                          help='download source')
        self.add_argument('tid', nargs='*',
                          help='id for novels to download')


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
