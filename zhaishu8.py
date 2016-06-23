#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Zhaishu8


def main():
    utils.in_main(Zhaishu8, config.GOAGENT)


if __name__ == '__main__':
    main()
