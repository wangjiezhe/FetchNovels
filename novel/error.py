#!/usr/bin/env python3
# -*- coding: utf8 -*-
#
# error.py
# Copyright (c) 2014 Wang Jiezhe <wangjiezhe@gmail.com>
# Released under GPLv3 or later.

class Error(Exception):
    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return repr(self.message)


class ValueNotSetError(Error):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return "Value %s not set." % self.message

class FuncNotSetError(Error):
    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return "Function %s not set." % self.message

