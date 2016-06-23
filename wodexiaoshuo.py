#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Wdxs


def main():
    utils.in_main(Wdxs, config.GOAGENT)


if __name__ == '__main__':
    main()
