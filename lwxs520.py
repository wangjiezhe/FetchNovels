#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Lwxs520


def main():
    utils.in_main(Lwxs520, config.GOAGENT)


if __name__ == '__main__':
    main()
