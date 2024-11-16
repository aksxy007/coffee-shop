from pydantic import BaseModel
from datetime import datetime

class Chat(BaseModel):
    user_id: str
    role: str
    content: str
    createdAt: datetime = datetime.now()