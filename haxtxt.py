#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Haxtxt


def main():
    utils.in_main(Haxtxt, config.GOAGENT)


if __name__ == '__main__':
    main()
