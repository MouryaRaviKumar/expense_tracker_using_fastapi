from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from utils.config import settings

_client: MongoClient | None = None

def connect():
    global _client
    _client = MongoClient(settings.MONGO_URI,serverSelectionTimeoutMS=5000)
    trip_col = get_collection(settings.TRIP_COLLECTION)
    expense_col = get_collection(settings.EXPENSE_COLLECTION)
    trip_col.create_index([("name", ASCENDING)])
    expense_col.create_index([("title", ASCENDING)])

def get_client() -> MongoClient:
    if _client is None:
        connect()
    return _client

def get_collection(collection_name: str) -> Collection:
    return get_client()[settings.DB_NAME][collection_name]

def disconnect() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None