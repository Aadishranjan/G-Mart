from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["G-Mart"]

print("✅ Connected to MongoDB")