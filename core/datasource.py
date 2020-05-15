from pymongo import MongoClient

# Database Class using MongoClient from pymongo
from util.config import config


def datasource():
    client = MongoClient(**config['database']['connection'])
    return client.get_database(config['database']['name'])


blacklist = datasource().blacklist
karma = datasource().karma
