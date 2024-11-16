from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging
from motor.motor_asyncio import AsyncIOMotorCollection
from fastapi import Depends
from db.mongodb_connection import get_db

async def save_chat(chat: BaseModel):
    try:
        chat_dict = chat.dict()# Convert the chat model to a dictionary
        db = get_db()
        result = await db["chats"].insert_one(chat_dict)# Insert into MongoDB
        print("saved")
        return {"message":f"Saved the chat: {result.inserted_id}"}  # Return the inserted document ID
    except Exception as e:
        logging.error(f"Failed to save chat: {e}")
        return {"error":f"Failed to save chat: {e}"}
    
async def check_collection_exists(collection_name):
    db = get_db()
    collections = await db.list_collection_names()
    return collection_name in collections

async def get_chat_history(user_id:str):
    try:
        db =get_db()
        messages =  await db["chats"].find({"user_id":user_id}).sort("createdAt", -1).limit(10).to_list(length=10)
        for chat in messages:
            if 'createdAt' in chat:
                del chat['createdAt']
        
        return messages
    except Exception as e:
        logging.error(f"Failed to get chat history: {e}")
        return []