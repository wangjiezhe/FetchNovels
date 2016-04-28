#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Error(Exception):

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return repr(self.message)


class NotSetError(Error):

    def __init__(self, value, message):
        super().__init__(message)
        self.value = value

    def __repr__(self):
        return "{self.value} {self.message} not set.".format(self=self)


class ValueNotSetError(NotSetError):

    def __init__(self, message):
        super().__init__("Value", message)


class MethodNotSetError(NotSetError):

    def __init__(self, message):
        super().__init__("Method", message)


class PropertyNotSetError(NotSetError):

    def __init__(self, message):
        super().__init__("Property", message)
