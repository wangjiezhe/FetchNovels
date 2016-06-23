#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Sis


def main():
    utils.in_main(Sis, config.GOAGENT)


if __name__ == '__main__':
    main()
