#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Shu69


def main():
    utils.in_main(Shu69, config.GOAGENT)


if __name__ == '__main__':
    main()
