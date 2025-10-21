from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_project():
    db_username = os.getenv('MONGO_USERNAME')
    db_password = os.getenv('MONGO_PASSWORD')
    
    mongo_uri = f"mongodb+srv://{db_username}:{db_password}@cluster0.okjtuan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(mongo_uri)
    
    return client
