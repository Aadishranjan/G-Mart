from bson.objectid import ObjectId
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
    

def update_product(product_id, name, quantity, price, img, products_collection):
    existing = products_collection.find_one({
        "_id": {"$ne": ObjectId(product_id)},
        "name": {"$regex": f"^{name}$", "$options": "i"}
    })
    if existing:
        return {"error": "Product with this name already exists."}

    result = products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {
            "name": name,
            "quantity": quantity,
            "price": price,
            "img": img
        }}
    )
    return result.modified_count > 0    