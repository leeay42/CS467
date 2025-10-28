from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env file
app.secret_key = os.getenv('SECRET_KEY')