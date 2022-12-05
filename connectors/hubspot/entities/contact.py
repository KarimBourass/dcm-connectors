import requests
import json
import urllib.parse
import pandas as pd
from flatten_json import flatten
import numpy as np
import math


CHUNK_SIZE = 1
CONTACT_BATCH_URL = "https://api.hubapi.com/contacts/v1/contact/batch"
CONTACT_PROPERTIES_URL = "https://api.hubapi.com/properties/v1/contacts/properties"
CONTACT_GET_ALL_URL = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
CONTACT_GET_BY_EMAIL_URL = 'https://api.hubapi.com/contacts/v1/contact/email/{}/profile'
CONTACT_VID_URL = "https://api.hubapi.com/contacts/v1/contact/vid/{}"


class Contact():

    def __init__(self, token):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(token)}

    def get_contact_properties(self):
        check_response = requests.get(CONTACT_PROPERTIES_URL, headers=self.headers)
        properties = check_response.json()

        check_fields = [a['name'] for a in properties]
        return check_fields

    def format_batch_contacts(self, contacts, contact_properties):
        result = []
        for c in contacts:
            my_dict = {"email": c['email']}
            properties = [{"property": k, "value": c[k]} for k in c.keys() if k in contact_properties]
            my_dict['properties'] = properties
            result.append(my_dict)

        # Split arrays
        result = split_array(result)
        return result

    # Create or Update Batch Contact
    # Note: The batch size should not exceed 1000 contacts per request.
    def publish_contact_batch(self, contacts):
        contact_properties = self.get_contact_properties()
        bodies = self.format_batch_contacts(contacts, contact_properties)

        for body in bodies:
            response = requests.post(CONTACT_BATCH_URL, json=list(body), headers=self.headers)
            print(response.status_code)

    def get_all_contacts(self):
        count = 100
        contact_list = []
        parameter_dict = {'count': count}

        has_more = True
        while has_more:
            parameters = urllib.parse.urlencode(parameter_dict)
            get_url = CONTACT_GET_ALL_URL + parameters
            r = requests.get(url=get_url, headers=self.headers)
            response_dict = json.loads(r.text)
            has_more = response_dict['has-more']
            contact_list.extend(response_dict['contacts'])
            parameter_dict['vidOffset'] = response_dict['vid-offset']

        contact_list = [flatten(contact) for contact in contact_list]
        df = pd.json_normalize(contact_list)
        return df

    def get_contact_by_email(self, email):
        url = CONTACT_GET_BY_EMAIL_URL.format(email)
        r = requests.get(url=url, headers=self.headers)
        return r.json()

    def delete_contact_by_email(self, email):
        contact = self.get_contact_by_email(email)
        if 'vid' in contact.keys():
            url = CONTACT_VID_URL.format(contact['vid'])
            response = requests.delete(url, headers=self.headers)
            return response.json()
        else:
            return contact

    # Create or Update Single Contact
    def publish_contact_single(self, contact):
        contact_properties = Contact().get_contact_properties()
        Contact().publish_contact_batch([contact], contact_properties)


def split_array(original_array):
    numberOfSubLists = math.ceil(len(original_array) / CHUNK_SIZE)
    arrays = np.array_split(original_array, numberOfSubLists)
    return arrays
