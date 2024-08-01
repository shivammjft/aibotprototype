import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_client = MongoClient(os.getenv('MONGO_URI'))
db = mongo_client['AIBOT']  
collection = db['company']  