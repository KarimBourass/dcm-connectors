from connectors.connector import Connector


class HubSpotConnector(Connector):

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def upload_df(self, df, *args, **kwargs):
        print('================ DF')
        print(df)
        print('================ ARGS', args)
        print('================ KWARGS', kwargs)
