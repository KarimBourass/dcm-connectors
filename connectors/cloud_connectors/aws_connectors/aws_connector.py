#!/usr/bin/python
# -*- coding: utf-8 -*-
import boto3


from connectors.connector import Connector


class AWSConnector:

    def __init__(self, key_id, key_secret):
        self.key_id = key_id
        self.key_secret = key_secret
        self.session = boto3.client("s3", aws_access_key_id=key_id, aws_secret_access_key=key_secret)

