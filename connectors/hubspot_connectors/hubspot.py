from connectors.connector import Connector
from connectors.hubspot_connectors.entities.contact import Contact


class HubSpotConnector(Connector):

    def __init__(self, token):
        self.token = token

    def upload_df(self, df, *args, **kwargs):
        entity = kwargs['entity']
        if entity == 'contact':
            contacts = df.to_dict('records')
            Contact(self.token).publish_contact_batch(contacts)
