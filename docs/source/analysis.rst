Analysis
========

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
