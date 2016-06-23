#!/usr/bin/env python
# -*- coding: utf-8 -*-

from novel import utils, config
from novel.sources import Klxsw


def main():
    utils.in_main(Klxsw, config.GOAGENT)


if __name__ == '__main__':
    main()
