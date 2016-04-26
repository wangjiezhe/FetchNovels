#!/usr/bin/env python
# -*- coding: utf-8 -*-


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


class MethodNotSetError(Error):

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return "Method %s not set." % self.message


class PropertyNotSetError(Error):

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return "Property %s not set." % self.message
