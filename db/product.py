from pymongo import MongoClient
from db.database import db

products_collection = db["product"]

def insert_product(name, quantity, price, img):
    existing_product = products_collection.find_one({
        "name": {"$regex": f"^{name}$", "$options": "i"}
    })

    if existing_product:
        return False  # Product already exists
    
    product = {
        "name": name,
        "quantity": quantity,
        "price": price,
        "img": img
    }
    products_collection.insert_one(product)
    return True  # Successfully inserted