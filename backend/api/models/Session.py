from datetime import datetime
from pydantic import BaseModel
from typing import List


class Session(BaseModel):
    user_id: str
    token: str
    expiry: datetime
    chats: List[str]
    created_at: datetime = datetime.utcnow()