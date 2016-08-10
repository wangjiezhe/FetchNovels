FetchNovels
===========

[![unstable](http://badges.github.io/stability-badges/dist/unstable.svg)](http://github.com/badges/stability-badges)

[![GPL Licence](https://badges.frapsoft.com/os/gpl/gpl.svg?v=103)](https://opensource.org/licenses/GPL-3.0/)
[![Dependency Status](https://dependencyci.com/github/wangjiezhe/FetchNovels/badge)](https://dependencyci.com/github/wangjiezhe/FetchNovels)

Fetch novels from internet.

A renewed version.


Usage
-----

    usage: fetchnovels [-h] [-V] [-u | -d | -l | -ls | -la | -D | -m] [-v] [-r]
                       [-p PROXY | -n]
                       [source] [tid [tid ...]]

    Fetch novels from Internet, and write into file.

    Available sources:
      bgif2, biquge, dzxsw, feizw, haxtxt, klxsw, lwxs, lwxs520, lwxsw,
      piaotian, piaotiancc, ranwen, shu69, shushu8, sto, ttshuba,
      ttzw, ttzw5, uks5, wdxs, xs365, yfzww, yq33, zhaishu8,
      doubangroup, ...

    positional arguments:
      source                download source
      tid                   id for novels to download

    optional arguments:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -u, --update          update novels in the database
      -d, --dump-only       dump only without update
      -l, --list            list novels in the database
      -ls, --list-serial    list serials in the database
      -la, --list-article   list articles in the database
      -D, --delete          delete novels in the database
      -m, --mark-finish     mark novels as finished
      -v, --verbose         show in more detail
      -r, --refresh         refresh novel in the database
      -p PROXY, --proxy PROXY
                            use specific proxy
      -n, --no-proxy        do not use any proxies


Todo
----

* [ ] Get novel in forum
* [ ] Login to get token
* [x] Add option to dump directly from database (for no network connection case)
* [ ] Fix text width for id and intro
