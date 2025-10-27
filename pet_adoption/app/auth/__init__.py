from flask import Flask
from dotenv import load_dotenv
import os

# Needed to set secret key used for session
# Should be set in root directory I think, but saving here

#load_dotenv()  # Loads variables from .env file
#app.secret_key = os.getenv('SECRET_KEY')
app.secret_key = 'temporary-dev-key-12345'