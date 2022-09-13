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
        if not df.empty:
            bucket_name = kwargs["bucket_name"]
            file_name = kwargs["file_name"]
            client = storage.Client(credentials=self.credentials)
            bucket = client.get_bucket(bucket_name)
            if "target_fields" in args.keys():
                self.upload_txt(df, args["args"], bucket)
                return

            bucket.blob(file_name).upload_from_string(df.to_csv(), 'text/csv')




    def upload_txt(self, df, target_fields, bucket):
            with open('output.txt', 'w') as f:
                for index, row in df.iterrows():
                    for map_row in target_fields:
                        col_name = map_row['name']
                        if col_name in df:
                            col_value = str(row[col_name])
                        else:
                            col_value = ""

                        new_column = self.build_column(col_value, map_row['size'])
                        f.write(new_column)

                    f.write('\n')

            bucket.blob('output.txt').upload_from_file(file_obj=f, rewind=True)



    def build_column(self, column, length):
        if len(column) > length:
            return column
        elif length == len(column):
            return column
        else:
            diff = length - len(column)
            new_column = column + " "*diff
            return new_column