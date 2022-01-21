from connectors.connector import Connector
from pymongo import MongoClient

import pandas as pd
import collections

from bson import ObjectId


def flatten(d, parent_key='', sep='_'):
    items = []

    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

class MongoDBConnector(Connector):

    def __init__(self, host=None, user=None, password=None, port=None, database=None,  **kwargs):
        self.host = host
        self.port = port
        self.db = database
        self.user = user
        self.password = password

    def get_client(self):
        if self.user and self.password:
            mongo_uri = f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}?retryWrites=false&authSource=admin"
        else:
            mongo_uri = f"mongodb://{self.host}:{self.port}/{self.db}?retryWrites=false"

        return MongoClient(mongo_uri)

    def upload_df(self, df, collection=None,insertion_script=None,**kwargs):
        client = self.get_client()
        col = client[self.db][collection]

        if insertion_script:
            exec(insertion_script)
        else:
            for row in df.to_dict(orient='records'):
                _id = row.get("_id", ObjectId())
                del row["_id"]
                col.update_one({"_id": _id}, {"$set": row}, upsert=True)


    def get_df(self, collection=None, query=None ,**kwargs):
        db = self.get_client()[self.db]
        col = db[collection]

        evaled_query = []
        if query:
            evaled_query = eval(query)

        result = col.aggregate(evaled_query)

        df = pd.DataFrame([flatten(d) for d in result])
        return df