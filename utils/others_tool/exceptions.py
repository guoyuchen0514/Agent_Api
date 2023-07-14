# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time : 2023-03-01 11:11
# @Author : 皆人
# @File : exceptions.py
# @Software: PyCharm


class MyBaseFailure(Exception):
    pass


class JsonpathExtractionFailed(MyBaseFailure):
    pass


class NotFoundError(MyBaseFailure):
    pass


class FileNotFound(FileNotFoundError, NotFoundError):
    pass


class SqlNotFound(NotFoundError):
    pass


class AssertTypeError(MyBaseFailure):
    pass


class DataAcquisitionFailed(MyBaseFailure):
    pass


class ValueTypeError(MyBaseFailure):
    pass


class SendMessageError(MyBaseFailure):
    pass


class ValueNotFoundError(MyBaseFailure):
    pass
