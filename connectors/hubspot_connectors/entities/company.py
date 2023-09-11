import requests
import json
import urllib.parse
import pandas as pd
from flatten_json import flatten
import numpy as np
import math

CHUNK_SIZE = 100
COMPANY_BATCH_URL = "https://api.hubapi.com/crm/v3/objects/companies/batch/create"
COMPANY_PROPERTIES_URL = "https://api.hubapi.com/properties/v1/companies/properties/"


class Company():
    
    def __init__(self, token):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(token)}
        
    def get_company_properties(self):
        check_response = requests.get(COMPANY_PROPERTIES_URL, headers=self.headers)
        properties = check_response.json()
        check_fields = [a['name'] for a in properties]
        return check_fields
    
    def format_batch_companies(self, companies, company_properties):
        result = []
        for c in companies:
            props = {}
            my_dict = {}

            for k in c.keys():
                if k in company_properties:
                    props[k] = c[k]

            my_dict['properties'] = props
            result.append(my_dict)

        # Split arrays
        result = split_array(result)
        return result

    def build_companies_vids(self, results, df):
        data = [{"company_vid": r['id'], "id_sf_company": r['properties']['id_sf']} for r in results]
        df = df.append(data, ignore_index=True)
        return df

    
    # Create or Update Batch Companies
    # Note: The batch size should not exceed 1000 companies per request.
    def publish_COMPANY_batch(self, companies):
        company_properties = self.get_company_properties()
        bodies = self.format_batch_companies(companies, company_properties)
        df = pd.DataFrame()  # Initialize an empty DataFrame
        for body in bodies:
            response = requests.post(COMPANY_BATCH_URL, json={"inputs": list(body)}, headers=self.headers)
            if response.status_code == 201:
                df = self.build_companies_vids(response.json()['results'])

        return df

def split_array(original_array):
    numberOfSubLists = math.ceil(len(original_array) / CHUNK_SIZE)
    arrays = np.array_split(original_array, numberOfSubLists)
    return arrays