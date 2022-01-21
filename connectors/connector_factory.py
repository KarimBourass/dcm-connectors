#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from connectors.cloud_connectors.azure_connectors.blob_connector import BlobConnector
from connectors.databases_connectors.sql_connectors.postgres_connector import PostgresConnector
from connectors.databases_connectors.sql_connectors.sql_server_connector import SqlServerConnector
from connectors.databases_connectors.sql_connectors.oracle_connector import OracleConnector


class ConnectorFactory(ABC):
    """Helper class that provides a standard way to create a Data Checker using factory method"""

    @abstractmethod
    def _(self):
        pass

    @staticmethod
    def get_data(connector_settings):
        """Factory method that returns a data connector"""

        type = connector_settings["type"]
        if type == 'sqlserver':
            connector = SqlServerConnector(connector_settings["host"], connector_settings["user"],
                                           connector_settings["password"],connector_settings["port"],
                                           connector_settings["database"])
            return connector
        elif type == 'azure_blob_storage':
            connector = BlobConnector(connector_settings["url"])
            return connector
        elif type == 'postgres':
            connector = PostgresConnector(connector_settings["host"], connector_settings["user"],
                                          connector_settings["password"], connector_settings["port"],
                                          connector_settings["database"])
            return connector
        elif type == 'oracledb':
            # connector = OracleConnector(connector_settings["host"], connector_settings["user"],
            #                               connector_settings["password"], connector_settings["port"],
            #                               connector_settings.get("database"), connector_settings.get("service_name"))
            connector = OracleConnector(**connector_settings)
            return connector
        else:
            print(f'{type} is not a valid check')
            # raise ValueError(f'{check_code} is not a valid check')
            return None
