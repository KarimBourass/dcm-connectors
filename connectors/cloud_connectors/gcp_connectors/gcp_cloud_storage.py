import pandas as pd

from connectors.cloud_connectors.gcp_connectors.gcp_connecor import GCPConnector
from connectors.connector import Connector

from google.cloud import storage


class GCPCloudStorageConnector(Connector, GCPConnector):

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    # def get_df(self, *args, **kwargs):
    #     credentials = self.credentials
    #     query = kwargs["query"]
    #     df = pd.read_gbq(query, project_id=self.project_id, credentials=credentials)
    #     return df

    # TODO: Probably its better to get file_Id and sheet_id then load it
    def upload_df(self, df, *args, **kwargs):
        credentials = self.credentials

        if not df.empty:
            bucket_name = kwargs["bucket_name"]
            file_name = kwargs["file_name"]
            client = storage.Client(credentials=credentials)
            bucket = client.get_bucket(bucket_name)
            bucket.blob(file_name).upload_from_string(df.to_csv(), 'text/csv')
