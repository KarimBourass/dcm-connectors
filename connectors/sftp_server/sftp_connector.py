#!/usr/bin/python
# -*- coding: utf-8 -*-import pandas as pd
from paramiko import Transport, SFTPClient


class SFTPServerConnector:

    def __init__(self, settings):
        self.host = settings["host"]
        self.port = settings["port"]
        self.username = settings["user"]
        self.password = settings["password"]
        self.create_connection(self.host, self.port, self.username, self.password)

    @classmethod
    def create_connection(cls, host, port, username, password):
        transport = Transport(sock=(host, port))
        transport.connect(username=username, password=password)
        cls._connection = SFTPClient.from_transport(transport)

    def close(self):
        self._connection.close()
