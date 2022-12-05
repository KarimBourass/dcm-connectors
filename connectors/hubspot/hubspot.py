from connectors.connector import Connector
from connectors.hubspot.entities.contact import Contact


class HubSpotConnector(Connector):

    def __init__(self, token):
        self.token = token

    def upload_df(self, df, *args, **kwargs):
        entity = kwargs['entity']
        if entity == 'contact':
            Contact(self.token).get_all_contacts()
