import requests
import json
import urllib.parse
import pandas as pd
from flatten_json import flatten
import numpy as np
import math

CHUNK_SIZE = 1
COMPANY_BATCH_URL = "https://api.hubapi.com/companies/v1/company/batch"
COMPANY_PROPERTIES_URL = "https://api.hubapi.com/properties/v1/company/properties"


class Company():
    
    def __init__(self, token):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(token)}
        
    def get_COMPANY_properties(self):
        check_response = requests.get(COMPANY_PROPERTIES_URL, headers=self.headers)
        properties = check_response.json()
        check_fields = [a['name'] for a in properties]
        return check_fields
    
    def format_batch_companies(self, companies, COMPANY_properties):
        result = []
        for c in companies:
            my_dict = {}
            if "vid" in c.keys():
                my_dict.update({"vid": c['vid']})
            elif "email" in c.keys():
                my_dict.update({"email": c['email']})

            properties = [{"property": k, "value": c[k]} for k in c.keys() if k in COMPANY_properties]
            my_dict['properties'] = properties
            result.append(my_dict)

        # Split arrays
        result = split_array(result)
        return result
    
    
    # Create or Update Batch Companies
    # Note: The batch size should not exceed 1000 companies per request.
    def publish_COMPANY_batch(self, companies):
        COMPANY_properties = self.get_COMPANY_properties()
        bodies = self.format_batch_companies(companies, COMPANY_properties)
        print("Bodies: {}".format(bodies))

        for body in bodies:
            response = requests.post(COMPANY_BATCH_URL, json=list(body), headers=self.headers)
            print("Response: {}", response.text)
    
def split_array(original_array):
    numberOfSubLists = math.ceil(len(original_array) / CHUNK_SIZE)
    arrays = np.array_split(original_array, numberOfSubLists)
    return arrays