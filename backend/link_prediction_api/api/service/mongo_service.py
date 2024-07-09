import os
import logging
from dotenv import load_dotenv

from pymongo import MongoClient

from utils.connect_db import create_mongo_client
from models.CloudFlareModels import CloudflareScanSubmission

load_dotenv()
logger = logging.getLogger("Link-ML-Service")

def is_duplicate_submission(submission: CloudflareScanSubmission, client: MongoClient) -> bool:
    collection = client.get_database(os.getenv("DATABASENAME")).get_collection(os.getenv("COLLECTION_NAME"))
    if collection.find_one({'result.url': submission.result.url}):
        logger.warning(f"Duplicate submission: Not inserting {submission.model_dump()}")
        return True
    return False

def insert_cloudflare_scan(submission: CloudflareScanSubmission) -> bool:
    client: MongoClient = create_mongo_client()
    if client is None:
        logger.error("Error Connecting to MongoDB: Client was None")
        return False

    if is_duplicate_submission(submission, client):
        return False

    db = client.get_database(os.getenv("DATABASENAME"))
    collection = db.get_collection(os.getenv("COLLECTION_NAME"))
    collection.insert_one(submission.model_dump())
    client.close()
    return True
