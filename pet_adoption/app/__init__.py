from flask import Flask
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from urllib.parse import quote_plus

# Load environment variables from the project .env explicitly. Using an explicit path avoids
# an AssertionError that can happen when find_dotenv() inspects call frames (seen when
# running python -c or in some interactive contexts).
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(base_dir, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    # Fallback to default behavior (search current working directory etc.)
    load_dotenv()

# MongoDB connection
db_username = quote_plus(os.getenv('MONGO_USERNAME'))  # Add quote_plus
db_password = quote_plus(os.getenv('MONGO_PASSWORD'))  # Add quote_plus
db_name = os.getenv('MONGO_DB_NAME')

# Validate required env vars early and provide a clear message if missing.
if not db_username or not db_password or not db_name:
    raise RuntimeError(
        "Missing MongoDB environment variables. Please set MONGO_USERNAME, MONGO_PASSWORD, and MONGO_DB_NAME "
        "(for example, create a `pet_adoption/.env` file with those values or export them in your shell)."
    )

# Build the Atlas connection URI. If you use a different host/URI, replace this with your MONGO_URI.
mongo_uri = f"mongodb+srv://{db_username}:{db_password}@cluster0.okjtuan.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0&tlsAllowInvalidCertificates=true"
client = MongoClient(mongo_uri)
db = client[db_name]

def create_app():
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    @app.route('/test-data')
    def test_data():
        animals = list(db['animals'].find({}, {'_id': 0}).limit(5))
        users = list(db['users'].find({}, {'_id': 0}).limit(5))
        return {
            'pets_count': db['animals'].count_documents({}),
            'users_count': db['users'].count_documents({}),
            'sample_pets': animals,
            'sample_users': users
        }
    
    # Register blueprints
    from app.admin.routes import admin
    app.register_blueprint(admin, url_prefix='/admin')
    
    # Register auth blueprint
    try:
        from app.auth.routes import auth
        app.register_blueprint(auth, url_prefix='/auth')
    except ImportError:
        pass
    
    # Register main blueprint (root routes)
    try:
        from app.main.routes import main
        app.register_blueprint(main)
    except ImportError:
        # If main blueprint is missing, keep app running but root will 404
        pass
    
    return app

# Registering blueprints: https://realpython.com/flask-blueprint/?utm_source=chatgpt.com
