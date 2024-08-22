from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.telegram_bot

def save_user_string(user_id, user_string):
    db.strings.update_one({"user_id": user_id}, {"$set": {"string": user_string}}, upsert=True)

def get_user_string(user_id):
    return db.strings.find_one({"user_id": user_id})["string"]

def is_allowed_user(user_id):
    return db.permissions.find_one({"user_id": user_id}) is not None

# Tambahkan lebih banyak fungsi untuk menangani izin, sudo, dan log.
