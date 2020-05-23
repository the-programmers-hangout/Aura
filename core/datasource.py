from pymongo import MongoClient

from util.config import config


def datasource():
    # unpack dictionary values
    client = MongoClient(**config['database']['connection'])
    return client.get_database(config['database']['name'])


# create two global variables for mongodb collections used in the application
blacklist = datasource().blacklist
karma = datasource().karma
