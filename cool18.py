#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Cool18


def main():
    utils.in_main(Cool18, config.GOAGENT, overwrite=False)


if __name__ == '__main__':
    main()
