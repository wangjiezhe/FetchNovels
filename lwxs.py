#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Lwxs


def main():
    utils.in_main(Lwxs, config.GOAGENT)


if __name__ == '__main__':
    main()
