#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import abstractmethod


class Connector:

    def __init__(self):
        pass

    @abstractmethod
    def get_df(self, *args, **kwargs):
        pass

    @abstractmethod
    def upload_df(self, *args, **kwargs):
        pass
