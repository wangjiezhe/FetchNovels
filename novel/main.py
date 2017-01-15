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
              bgif2, biquge, dzxsw, feizw, haxtxt, jjwxc, klxsw, lou19,
              lwxs, lwxs520, lwxsw, piaotian, piaotiancc, ranwen, shu69,
              shushu8, sto, ttshuba, ttzw, ttzw5, uks5, wdxs, xs365, yfzww,
              yq33, zhaishu8, doubangroup, ...
        """)
        super().__init__(
            prog='fetchnovels',
            description=description,
            formatter_class=argparse.RawTextHelpFormatter
        )
        self.add_argument('-V', '--version', action='version',
                          version=__version__)

        group = self.add_mutually_exclusive_group()
        group.add_argument('-u', '--update', action='store_true',
                           help='update novels in the database')
        group.add_argument('-d', '--dump-only', action='store_true',
                           help='dump only without update')
        group.add_argument('-l', '--list', action='store_true',
                           help='list novels in the database')
        group.add_argument('-ls', '--list-serial', action='store_true',
                           help='list serials in the database')
        group.add_argument('-la', '--list-article', action='store_true',
                           help='list articles in the database')
        group.add_argument('-D', '--delete', action='store_true',
                           help='delete novels in the database')
        group.add_argument('-m', '--mark-finish', action='store_true',
                           help='mark novels as finished')

        self.add_argument('-v', '--verbose', action='count',
                          help='show in more detail')
        self.add_argument('-r', '--refresh', action='store_true',
                          help='refresh novel in the database')

        proxy_group = self.add_mutually_exclusive_group()
        proxy_group.add_argument('-p', '--proxy', action='store',
                                 help='use specific proxy')
        proxy_group.add_argument('-n', '--no-proxy', action='store_true',
                                 help='do not use any proxies')

        self.add_argument('source', nargs='?',
                          help='download source')
        self.add_argument('tid', nargs='*',
                          help='id for novels to download')


def main():
    parser = MyParser()
    args = parser.parse_args()

    if args.source:
        need_fix = re.match(r'(\d+)(.+)', args.source)
        if need_fix:
            source = '{g[1]}{g[0]}'.format(g=need_fix.groups())
        else:
            source = args.source
    else:
        source = None

    if args.no_proxy:
        proxies = '---'
    else:
        proxies = args.proxy

    config.check_first()

    with cli.NovelCmdline(source, args.tid, proxies, args.verbose) as fac:
        if args.list:
            fac.list()
        elif args.list_serial:
            fac.list_serial()
        elif args.list_article:
            fac.list_article()
        elif args.delete:
            fac.delete()
        elif args.mark_finish:
            fac.try_mark_finish()
        elif args.update:
            if args.refresh:
                fac.refresh()
            else:
                fac.update()
        elif args.dump_only:
            fac.dump()
        elif source:
            print('{}: {}'.format(source, args.tid))
            if not args.tid:
                print('No specific tid to download!')
                sys.exit(1)
            if args.refresh:
                fac.refresh()
            else:
                fac.update()
            fac.dump()
        else:
            parser.print_usage()


if __name__ == '__main__':
    main()
