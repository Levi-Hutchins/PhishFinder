from api.utils.connect_db import create_mongo_client
from pymongo import MongoClient

def test_db_connection():
    assert isinstance(create_mongo_client(), MongoClient)
