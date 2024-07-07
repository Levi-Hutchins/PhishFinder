from connect_db import get_mongo_client
from pymongo import MongoClient

from models.CloudFlareModels import CloudflareScanSubmission

def insert_cloudflare_scan(submission: CloudflareScanSubmission):
    client: MongoClient = get_mongo_client()




insert_cloudflare_scan()