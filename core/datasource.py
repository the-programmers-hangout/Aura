from pymongo import MongoClient


# Database Class using MongoClient from pymongo
from util.config import config


class DataSource(object):

    def __init__(self, host, port, username, password, name):
        self._client = MongoClient(host=host, port=port, username=username, password=password,
                                   authMechanism='SCRAM-SHA-256')
        self._db = self._client.get_database(name)

    @property
    def db(self):
        return self._db


blacklist = DataSource(config['database']['host'], config['database']['port'],
           config['database']['username'], config['database']['password'],
           config['database']['name']).db.blacklist

karma = DataSource(config['database']['host'], config['database']['port'],
                       config['database']['username'], config['database']['password'],
                       config['database']['name']).db.karma