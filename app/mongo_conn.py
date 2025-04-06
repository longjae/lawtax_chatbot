from pymongo import MongoClient
from config import Config
from bson import json_util

client = MongoClient(Config.MONGODB_URI)
db = client[Config.DB_NAME]
collection = db[Config.COLLECTION_NAME]


def get_documents():
    """MongoDB에서 JSON 문서 추출"""
    docs = collection.find()
    return json_util.loads(json_util.dumps(docs))
