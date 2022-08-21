import pandas as pd


from connectors.cloud_connectors.aws_connectors.aws_connector import AWSConnector
from connectors.connector import Connector


class AWSS3Connector(Connector, AWSConnector):

    def __init__(self, key_id, key_secret, bucket_name):
        super().__init__(key_id, key_secret)
        self.bucket_name = bucket_name
   
   
    def read_df(self, extention, byte_stream):
        if extention == 'text/csv':
            return pd.read_csv(byte_stream)
        elif extention == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            return pd.read_excel(byte_stream.read(), sheet_name=0)
        else:
            raise Exception("UNSUPPORTED FILE FORMAT")
    
    def get_df(self, *args, **kwargs):
        s3_key = kwargs.get('s3_key',None)
        s3_session = self.session
        response = s3_session.get_object(Bucket=self.bucket_name, Key=s3_key)
        header = response["ResponseMetadata"].get("HTTPHeaders")
        df = self.read_df(header["content-type"], response.get("Body"))
        return df

    def upload_df(self, *args, **kwargs):
        pass

    


    
