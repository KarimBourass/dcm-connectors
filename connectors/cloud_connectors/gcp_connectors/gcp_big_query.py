import pandas as pd

from connectors.cloud_connectors.gcp_connectors.gcp_connecor import GCPConnector
from connectors.connector import Connector


class GCPBigQueryonnector(Connector, GCPConnector):

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.bucket_name = kwargs["bucket_name"]


    def get_df(self, *args, **kwargs):
        credentials = self.credentials
        query = f'"""{kwargs["kwargs"]}"""'
        df = pd.read_gbq(query, project_id=self.project_id, credentials=credentials)
        return df

    def upload_df(self, *args, **kwargs):
        pass