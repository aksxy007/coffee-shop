from datetime import datetime
from bson import ObjectId
from db.mongodb_connection import get_db

async def save_session(user_id: str, token: str, expiry: datetime):
    session_data = {
        "user_id": user_id,
        "token": token,
        "expiry": expiry,
        "created_at": datetime.now()
    }
    db = get_db()
    existing_user = await db['sessions'].find_one({user_id:session_data['user_id']})
    if existing_user is None:
        result = await db["sessions"].insert_one(session_data)
    else:
        result = await db['sessions'].find_one_and_update(session_data)
    return str(result.inserted_id)

async def get_session_by_token(token: str):
    db = get_db()
    session = await db["sessions"].find_one({"token": token})
    return session

async def delete_session(token: str):
    db= get_db()
    await db["sessions"].delete_one({"token": token})