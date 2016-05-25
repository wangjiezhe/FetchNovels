#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class BaseNovel(ABC):

    @abstractmethod
    def dump(self, overwrite=True):
        pass
