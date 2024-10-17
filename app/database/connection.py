# app/database/connection.py

from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

# Remove the global client and db variables
# client = AsyncIOMotorClient(MONGODB_URI)
# db = client[DATABASE_NAME]

# Define a function to get the database client
def get_database():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DATABASE_NAME]
    return db

async def init_db():
    db = get_database()
    await db["books"].create_index([("title", "text"), ("description", "text")])
