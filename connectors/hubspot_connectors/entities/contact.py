import requests
import pandas as pd
from flatten_json import flatten
import numpy as np
import math


CHUNK_SIZE = 1
CONTACT_CREATE_BATCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/batch/create"
CONTACT_UPDATE_BATCH_URL = "https://api.hubapi.com/crm/v3/objects/contacts/batch/update"
CONTACT_PROPERTIES_URL = "https://api.hubapi.com/properties/v1/contacts/properties"


class Contact():

    def __init__(self, token):
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'Bearer {}'.format(token)}

    def get_contact_properties(self):
        check_response = requests.get(
            CONTACT_PROPERTIES_URL, headers=self.headers)
        properties = check_response.json()
        check_fields = [a['name'] for a in properties]
        return check_fields

    def format_batch_contacts(self, contacts, contact_properties):
        result = []
        for c in contacts:
            props = {}
            my_dict = {}

            for k in c.keys():
                if k in contact_properties:
                    props[k] = c[k]

            my_dict['properties'] = props
            result.append(my_dict)
            if 'association_type_id' in c.keys():
                associations = [
                    {
                        "to": {
                            "id": c['company_vid']
                        },
                        "types": [
                            {
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId": c['association_type_id']
                            }
                        ]
                    }
                ]
                my_dict['associations'] = associations
                

        # Split arrays
        result = split_array(result)
        return result

    # Note: The batch size should not exceed 1000 contacts per request.
    def publish_contact_batch(self, contacts):
        contact_properties = self.get_contact_properties()
        bodies = self.format_batch_contacts(contacts, contact_properties)

        for body in bodies:
            response = requests.post(CONTACT_CREATE_BATCH_URL, json={"inputs": list(body)}, headers=self.headers)
            print(response.json())
            
        return None




def split_array(original_array):
    numberOfSubLists = math.ceil(len(original_array) / CHUNK_SIZE)
    arrays = np.array_split(original_array, numberOfSubLists)
    return arrays
