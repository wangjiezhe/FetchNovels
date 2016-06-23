#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Yq33


def main():
    utils.in_main(Yq33, config.GOAGENT)


if __name__ == '__main__':
    main()
