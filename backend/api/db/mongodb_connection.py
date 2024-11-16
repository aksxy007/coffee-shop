from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import logging

load_dotenv()

client = None
db = None

async def connect_to_mongo():
    global client, db
    try:
        client  = AsyncIOMotorClient(os.getenv('MONGO_URL'))
        db = client[os.getenv('MONGODB_DATABASE_NAME')]
        logging.info("Connected to mongodb")
    except Exception as e:
        logging.error(f"Failed to connect to mongo: {e}")
        
async def close_mongo_connection():
    global client
    try:
        if client:
            client.close()
            logging.info("MongoDB connection closed")
    except Exception as e:
        logging.error(f"Failed to close MongoDB connection: {e}")
        
        
def get_db():
    # Ensure the connection is open
    if not client:
        raise ValueError("MongoDB connection is not established")
    return db