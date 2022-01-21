#!/usr/bin/python
# -*- coding: utf-8 -*-

from io import BytesIO
from multiprocessing.pool import ThreadPool

import pyarrow as pa

from connectors.cloud_connectors.azure_connectors.azure_storage_handler import AzureStorageHandler
from connectors.connector import Connector


class CollectionConnector(Connector, AzureStorageHandler):

    def __init__(self, conn_string=None, container="uploads"):
        super().__init__(conn_string)
        self.container = container
        self.container_client = self.blob_service_client.get_container_client(self.container)

    def download_all_blobs_in_container(self, prefix=None):
        blobs_list = self.list_blobs_in_container(self.container, prefix=prefix)
        blobs_list = sorted(blobs_list, key=lambda b: b.creation_time)
        result = self.run(blobs_list)
        return result

    def run(self, blobs):
        with ThreadPool(processes=int(10)) as pool:
            return pool.map(self.get_parquet_table, blobs)

    def get_parquet_table(self, blob):
        blob_client = self.container_client.get_blob_client(blob=blob.name)
        byte_stream = BytesIO()
        blob_client.download_blob().readinto(byte_stream)
        partition = pa.parquet.read_table(source=byte_stream)
        byte_stream.close()
        return partition

    def get_df(self, *args, **kwargs):
        domain_id = kwargs.get("domain_id")
        tables = self.download_all_blobs_in_container(prefix=f'{domain_id}/')

        if len(tables) > 0:
            return pa.concat_tables(tables, promote=True).to_pandas()
        else:
            return pa.table([]).to_pandas()

    def upload_df(self, *args, **kwargs):
        pass
