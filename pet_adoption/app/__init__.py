from flask import Flask
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # MongoDB connection
    db_username = os.getenv('MONGO_USERNAME')
    db_password = os.getenv('MONGO_PASSWORD')
    db_name = os.getenv('MONGO_DB_NAME')

    mongo_uri = f"mongodb+srv://{db_username}:{db_password}@cluster0.okjtuan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"

    client = MongoClient(mongo_uri)
    db = client[db_name]

    # Store database in app config for blueprints to access
    app.config['animals_collection'] = db['animals']
    app.config['users_collection'] = db['users']

    # Register blueprints
    from app.admin.routes import admin
    app.register_blueprint(admin, url_prefix='/admin')

    # Register main blueprints
    from app.main.routes import main
    app.register_blueprint(main)

    return app

# Registering blueprints: https://realpython.com/flask-blueprint/?utm_source=chatgpt.com
