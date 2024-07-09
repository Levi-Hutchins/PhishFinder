import logging
from pymongo import MongoClient
from dotenv import load_dotenv




# Since this is a simple app I am build I'll just create separate connections 
load_dotenv()
logger = logging.getLogger("Link-ML-Service")


def create_mongo_client() -> MongoClient:
    try:
        client: MongoClient = MongoClient(URI)
        return client
    except Exception as e:
        logger.error(f"An error occurred while connecting to MongoDB: {e}")
        return None
    
    

    
