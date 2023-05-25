from connectors.connector import Connector
from connectors.sftp_server.sftp_connector import SFTPServerConnector
import os
from datetime import datetime

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
            start_row = f"00000000NOMPARTN CREDITQUOT 8    {datetime.today().strftime('%Y%m%d')}00734161                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     "
            f.write(start_row)
            f.write('\r\n')
            for index, row in df.iterrows():
                for map_row in target_fields:
                    col_name = map_row['name']
                    if col_name in df:
                        col_value = str(row[col_name])
                    else:
                        col_value = ""

                    line = line + self.build_column(col_value, map_row)
                    
                new_line = self.build_line(line)
                f.write(new_line)
                f.write('\r\n')
                
            end_row = f"99999999NOMPARTN CREDIT     8    {datetime.today().strftime('%Y%m%d')}0073416100000014                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             "
            f.write(end_row)
            f.write('\r\n')
                   
        self._connection.put(localpath='output.txt', remotepath=path, confirm=True)
        os.remove("output.txt")

    def build_column(column, map_row):
        length = map_row['size']
        col_length = len(column)
        if col_length > length:
            return column[:length]
        elif length == col_length:
            return column
        else:
            diff = length - col_length
            if map_row['type'] == "int":
                new_column = ("0" * diff) + column
            else:
                new_column = column + " " * diff
            return new_column

    def build_line(line, length=870):
        line_length = len(line)
        if line_length > length:
            return line[0:length]
        elif length == line_length:
            return line
        else:
            diff = length - line_length
            new_line = line + " " * diff
            return new_line