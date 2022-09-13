#!/usr/bin/python
# -*- coding: utf-8 -*-import pandas as pd
from google.oauth2 import service_account


class GCPConnector:

    def __init__(self, settings):
        self.project_id = settings["project_id"]
        if(settings["type"]=="gcs"):
          self.client_x509_cert_url = f"https://www.googleapis.com/robot/v1/metadata/x509/cloud-storage%40{self.project_id}.iam.gserviceaccount.com"
        elif (settings["type"]=="gcp"):
          self.client_x509_cert_url = f"https://www.googleapis.com/robot/v1/metadata/x509/big-query%40{self.project_id}.iam.gserviceaccount.com"
        private_key = settings["private_key"].replace("\\n", "\n")

        credentials = {
            "type": "service_account",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "project_id": self.project_id,
            "private_key_id":settings["private_key_id"],
            "private_key": private_key,
            "client_email": settings["client_email"],
            "client_id": settings["client_id"],
            "client_x509_cert_url": self.client_x509_cert_url
        }

        self.credentials = service_account.Credentials.from_service_account_info(credentials)
