from pymongo import MongoClient


class Database(object):

    def __init__(self, host, port, name):
        self._client = MongoClient(host, port)
        self._db = self._client[name]

    @property
    def db(self):
        return self._db
