#!/usr/bin/python
# -*- coding: utf-8 -*-

from azure.storage.blob import BlobServiceClient


class AzureStorageHandler:
    def __init__(self, conn_string):
        self.conn_string = conn_string
        self.blob_service_client = BlobServiceClient.from_connection_string(self.conn_string)

    def list_containers(self):
        return self.blob_service_client.list_containers()

    def list_blobs_in_container(self, container, prefix=None):
        return self.blob_service_client.get_container_client(container).list_blobs(name_starts_with=prefix)
