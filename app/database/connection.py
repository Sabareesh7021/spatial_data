from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.config import DB_NAME, DB_URL

client   = AsyncIOMotorClient(DB_URL)
database = client[DB_NAME]


def get_db():
    return database


