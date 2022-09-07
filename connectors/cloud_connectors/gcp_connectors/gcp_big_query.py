import pandas as pd

from connectors.cloud_connectors.gcp_connectors.gcp_connecor import GCPConnector
from connectors.connector import Connector


class GCPBigQueryonnector(Connector, GCPConnector):

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def get_df(self, *args, **kwargs):
        credentials = self.credentials
        query = kwargs["query"]
        df = pd.read_gbq(query, project_id=self.project_id, credentials=credentials)
        return df

    # TODO: Probably its better to get file_Id and sheet_id then load it
    def upload_df(self, df, *args, **kwargs):
        credentials = self.credentials

        if not df.empty:
            project_name = kwargs["project_name"]
            dataset_name = kwargs["dataset_name"] 
            table_name = kwargs["table_name"]
            destination_table = f"{dataset_name}.{table_name}"
            df.to_gbq(destination_table=destination_table.format(dataset_name, table_name),
                      project_id=project_name, if_exists='replace', credentials=credentials)
