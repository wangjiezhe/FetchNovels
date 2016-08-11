.. FetchNovels documentation master file, created by
   sphinx-quickstart on Wed Aug 10 19:02:29 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FetchNovels's documentation!
=======================================

Contents:

.. toctree::
   :maxdepth: 2


This project helps you to download novels from Internet, and easily write into files.


Usage
-----

::

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


Analysis
--------

This project use ``PyQuery`` to parse text, and ``PhantomJS`` for some websites which need to load JavaScript.
It use ``Sqlite`` to store data, default in ``~/.cache/novel/cache.db``, and ``SQLAlchemy`` for ORM.

config.py
    Some constants, like proxy, encoding, headers, etc., and some functions with cache files.

db.py
    Functions that works with database.

models.py
    ORM models.

utils.py
    Some helper functions, and class to clean up the text.

decorators.py
    Decorator to automatically retry when meeting HTTPError or broken response.

base.py
    Basic class, must be covered.

serial.py
    Classes to download novel in many pages.

single.py
    Classes to download novel in one page.

cli.py
    Integrated. Use introspection to get the right class to use.

main.py
    The command line entry.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

