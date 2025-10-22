from dotenv import load_dotenv
import os
from pymongo import MongoClient

load_dotenv(os.path.join(os.path.dirname(__file__), 'CS467',  '.env'))

def get_project():
    db_username = os.getenv('MONGO_USERNAME')
    db_password = os.getenv('MONGO_PASSWORD')
    db_name = os.getenv('MONGO_DB_NAME')

    mongo_uri = f"mongodb+srv://{db_username}:{db_password}@cluster0.okjtuan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"

    client = MongoClient(mongo_uri)
    db = client[db_name]
    return db
