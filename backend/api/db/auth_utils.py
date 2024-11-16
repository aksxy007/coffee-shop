from models.Register import UserRegister
from pydantic import BaseModel
from db.mongodb_connection import get_db
from pymongo.results import InsertOneResult

import logging
async def register_user(payload:BaseModel):
    try:
        user = payload.dict()
        user_dict = {"username":user['username'],"email":user['email'],"password":user['password']}
        db = get_db()
        newUser: InsertOneResult = await db['users'].insert_one(user_dict)

        # Return the inserted user ID or the full document
        if newUser.inserted_id:
            return {"id": str(newUser.inserted_id), "username": user_dict["username"], "email": user_dict["email"]}

        return None
    except Exception as e:
        logging.error(f"Failed to create user: {e}")
        return None
    

async def get_user_by_email(email: str):
    """Get user by email"""
    try:
        db = get_db()
        user = await db['users'].find_one({"email": email})
        return user
    except Exception as e:
        logging.error(f"Failed to retrieve user by email {email}: {e}")
        return None

