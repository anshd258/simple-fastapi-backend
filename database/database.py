import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB connection setup
MONGO_URL = os.environ.get("MONGO_URL")
print(f'MONGO_URL: {os.environ.items()}')
client = MongoClient(MONGO_URL)
database = client['hronedb']

# Define collections
products_collection = database['products']
orders_collection = database['orders']