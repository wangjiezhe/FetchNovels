#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Xs365


def main():
    utils.in_main(Xs365, config.GOAGENT)


if __name__ == '__main__':
    main()
