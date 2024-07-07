from connect_db import get_mongo_client
from pymongo import MongoClient
def insert_cloudflare_scan():
    client: MongoClient = get_mongo_client()
    print(client.get_database("PhishFinder").list_collection_names())




insert_cloudflare_scan()