from connectors.connector import Connector
from connectors.sftp_server.sftp_connector import SFTPServerConnector
import os


class SftpServer(Connector, SFTPServerConnector):

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def upload_df(self, df, *args, **kwargs):
        file_name = kwargs["file_name"]
        file_type = kwargs["file_type"]
        path = f"{file_name}.{file_type}"
        if not df.empty:
            remote_path = path
            if "target_fields" in kwargs.keys() and file_type == "txt":
                self.upload_txt(df, kwargs["target_fields"], path)
                return

            self._connection.put(localpath=remote_path, remotepath=remote_path, confirm=True)

    def upload_txt(self, df, target_fields, path):
        with open('output.txt', 'a+') as f:
            f.seek(0)
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
        self._connection.put(localpath='output.txt', remotepath=path, confirm=True)
        os.remove("output.txt")

    def build_column(self, column, length):
        if len(column) > length:
            return column
        elif length == len(column):
            return column
        else:
            diff = length - len(column)
            new_column = column + " " * diff
            return new_column
