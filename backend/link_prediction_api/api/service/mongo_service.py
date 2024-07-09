import os
import logging
from dotenv import load_dotenv

from utils.connect_db import create_mongo_client

from pymongo import MongoClient

from models.CloudFlareModels import CloudflareScanSubmission

load_dotenv()
logger = logging.getLogger("Link-ML-Service")

def insert_cloudflare_scan(submission: CloudflareScanSubmission):

    client: MongoClient = create_mongo_client(os.getenv('MONGODB_URI'))

    if client is not None:
        db = client.get_database(os.getenv("DATABASENAME"))
        collection = db.get_collection(os.getenv("COLLECTION_NAME"))
        submission_dict = submission.model_dump()
        collection.insert_one(submission_dict)

        client.close()
    else:
        logger.error("Error Connecting to MongoDB Client was None")






