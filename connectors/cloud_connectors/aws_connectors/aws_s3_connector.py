import pandas as pd


from connectors.cloud_connectors.aws_connectors.aws_connector import AWSConnector
from connectors.connector import Connector


class AWSS3Connector(Connector, AWSConnector):

    def __init__(self, key_id, key_secret, bucket_name, s3_key):
        super().__init__(key_id, key_secret)
        self.bucket_name = bucket_name
        self.s3_key = s3_key

    
    def get_df(self, *args, **kwargs):
        s3_session = self.session
        response = s3_session.get_object(Bucket=self.bucket_name, Key=self.s3_key)
        df = pd.read_csv(response.get("Body"))
        return df

    def upload_df(self, *args, **kwargs):
        pass