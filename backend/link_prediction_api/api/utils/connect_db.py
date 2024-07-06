import os
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()


# Since this is a simple app I am build I'll just create separate connections 


def create_mongo_client() -> MongoClient:

    try:
        client: MongoClient = MongoClient(os.getenv('MONGODB_URI'))
        print("MongoDB connection successful")
        return client
    except Exception as e:
        print(f"An error occurred while connecting to MongoDB: {e}")
        return None
    
    
def get_mongo_client() -> MongoClient:
    return create_mongo_client()
    
