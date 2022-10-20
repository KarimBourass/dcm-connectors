import os
from connectors.cloud_connectors.gcp_connectors.gcp_connecor import GCPConnector
from connectors.connector import Connector

from google.cloud import storage


class GCPCloudStorageConnector(Connector, GCPConnector):

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    # TODO: Probably its better to get file_Id and sheet_id then load it
    def upload_df(self, df, *args, **kwargs):
        file_name = kwargs["file_name"]
        file_type = kwargs["file_type"]
        path = f"{file_name}.{file_type}"
        if not df.empty:
            bucket_name = kwargs["bucket_name"]
            file_name = kwargs["file_name"]
            client = storage.Client(credentials=self.credentials)
            bucket = client.get_bucket(bucket_name)
            if "target_fields" in kwargs.keys() and file_type == "txt":
                self.upload_txt(df, kwargs["target_fields"], bucket, path)
                return

            bucket.blob(path).upload_from_string(df.to_csv(), 'text/csv')

    def upload_txt(self, df, target_fields, bucket, path):
        with open('output.txt', 'a+') as f:
            f.seek(0)
            for index, row in df.iterrows():
                line =''
                for map_row in target_fields:
                    col_name = map_row['name']
                    if col_name in df:
                        col_value = str(row[col_name])
                    else:
                        col_value = ""
                    line = line + build_column(col_value, map_row['size'])

                new_line = self.build_column(line)
                f.write(new_line)
                f.write('\n')

        bucket.blob(path).upload_from_filename('output.txt')
        os.remove("output.txt")

    def build_column(self, column, length):
        col_length = len(column)    
        if col_length > length:
            return column[0:length]
        elif length == col_length:
            return column
        else:
            diff = length - col_length
            new_column = column + " " * diff
            return new_column
    
    def line_length(self, line, length=870):
        line_length = len(line)    
        if line_length > length:
            return line[0:length]
        elif length == line_length:
            return line
        else:
            diff = length - line_length
            new_line = line + " " * diff
            return new_line