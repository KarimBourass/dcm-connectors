#!/usr/bin/python
# -*- coding: utf-8 -*-

from connectors.databases_connectors.sql_connectors.sql_connector import SqlConnector
import urllib
from sqlalchemy import create_engine


class SqlServerConnector(SqlConnector):

    def __init__(self, host, user, password, port, database):
        super().__init__(host, user, password, port, database)
        self.driver = "mssql+pymssql"

    def construct_query(self, query, preview, rows):
        if preview:
            query = query.lower()
            query = query.replace("select", "select " + " top " + str(rows))
        return query

    # def get_engine(self):
    #     params = urllib.parse.quote_plus("DRIVER={SQL Server Native Client 11.0};"
    #                                      f"SERVER={self.host};"
    #                                      f"DATABASE={self.database};"
    #                                      f"UID={self.user};"
    #                                      f"PWD={self.password}")
    #
    #     engine = create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    #     return engine
