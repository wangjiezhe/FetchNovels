#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Dzxsw


def main():
    utils.in_main(Dzxsw, config.GOAGENT)


if __name__ == '__main__':
    main()
