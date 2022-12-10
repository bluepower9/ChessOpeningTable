from pymongo import MongoClient
import json

with open('config.json', 'r') as file:
    config = json.load(file)

def connect() -> MongoClient:
    '''
    Connects to and returns MongoClient for database.
    '''
    cluster = config.get('database').get('url')
    client = MongoClient(cluster)

    return client