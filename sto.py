#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import config, utils
from novel.sources import Sto


def main():
    utils.in_main(Sto, config.GOAGENT)


if __name__ == '__main__':
    main()
