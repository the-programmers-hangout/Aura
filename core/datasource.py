from pymongo import MongoClient


# Database Class using MongoClient from pymongo
class DataSource(object):

    def __init__(self, host, port, username, password, name):
        self._client = MongoClient(host=host, port=port, username=username, password=password,
                                   authMechanism='SCRAM-SHA-256')
        self._db = self._client.get_database(name)

    @property
    def db(self):
        return self._db
