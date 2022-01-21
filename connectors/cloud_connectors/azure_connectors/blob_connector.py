#!/usr/bin/python
# -*- coding: utf-8 -*-

from io import BytesIO

import pandas as pd
import pyarrow.parquet as pq

from connectors.cloud_connectors.azure_connectors.azure_storage_handler import AzureStorageHandler
from connectors.connector import Connector


class BlobConnector(Connector, AzureStorageHandler):

    def __init__(self, conn_string):
        super().__init__(conn_string)

    def get_df(self, container, blob, *args, **kwargs):
        my_container = self.blob_service_client.get_container_client(container)
        blob_client = my_container.get_blob_client(blob=blob)
        byte_stream = BytesIO()        
        blob_client.download_blob().readinto(byte_stream)
        extention = self.get_extention(blob_client.blob_name)
        
        if extention is 'parquet':
            return self.read_parquet(byte_stream, *args, **kwargs)
        elif extention is 'csv':
            return self.read_csv(byte_stream, *args, **kwargs)
        elif extention is ['xlsx', 'xls', 'xlsm']:
            return self.read_excel(byte_stream, *args, **kwargs)
        elif extention is "json":
            return self.read_json(byte_stream, *args, **kwargs)
        else:
            raise Exception("UNSUPPORTED FILE FORMAT")


    def read_parquet(self, stream, preview=False, *args,**kwargs):
        partition = pq.read_table(source=stream)
        df = partition.to_pandas()
        stream.close()
        return df

    def read_csv(self, stream, preview=False, *args, **kwargs):
        df = pd.read_csv(stream, sep=';', encoding='utf8', dtype=str)
        stream.close()
        return df

    def read_excel(self, stream, sheet_name=0, preview=False, *args, **kwargs):
        df = pd.read_excel(stream, sheet_name=sheet_name)
        stream.close()
        return df
    
    def read_json(self, stream, preview=False, *args, **kwargs):
        df = pd.read_json(stream) 
        stream.close()
        return df

    def upload_df(self, df, container, blob, sep=";", output_format="csv", *args, **kwargs):
        if output_format == "csv":
            self.upload_df_as_csv(df, container, blob, sep)
        if output_format == "excel":
            self.upload_df_as_excel(df, container, blob)
        if output_format == "json":
            self.upload_df_as_json(df, container, blob)

    def upload_df_as_csv(self, df, container, blob, sep=";"):
        output = df.to_csv(sep=sep, index=False, encoding="utf-8")
        container_client = self.blob_service_client.get_container_client(container)
        blob_client = container_client.get_blob_client(f"{blob}.csv")
        blob_client.upload_blob(output, blob_type="BlockBlob", overwrite=True)

    def upload_df_as_json(self, df, container, blob):
        output = df.to_json(orient='records')
        container_client = self.blob_service_client.get_container_client(container)
        blob_client = container_client.get_blob_client(f"{blob}.json")
        blob_client.upload_blob(output, blob_type="BlockBlob", overwrite=True)

    def upload_df_as_excel(self, df, container, blob):
        writer = BytesIO()
        df.to_excel(writer)
        blob_client = self.blob_service_client.get_blob_client(container, f"{blob}.xlsx")
        blob_client.upload_blob(writer.getvalue(), overwrite=True)

    def get_extention(self, file_name):
        parts = file_name.split('.')

        if len(parts) > 1:
            extention = parts[-1]
        else:
            extention = 'parquet'

        return extention
