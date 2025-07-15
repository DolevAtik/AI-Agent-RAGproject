from pymongo import MongoClient
from app.config import Config

class MongoDBClient:
    def __init__(self):
        self.client = MongoClient(Config.MONGODB_HOST, Config.MONGODB_PORT)
        self.db = self.client[Config.MONGODB_DB]
        self.logs_collection = self.db.query_logs