#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import config, utils
from novel.sources import Uks5


def main():
    utils.in_main(Uks5, config.GOAGENT)


if __name__ == '__main__':
    main()
