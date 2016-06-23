#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import config, utils
from novel.sources import Ttzw


def main():
    utils.in_main(Ttzw, config.GOAGENT)


if __name__ == '__main__':
    main()
