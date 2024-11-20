from datetime import datetime
from pydantic import BaseModel
from typing import List


class Session(BaseModel):
    user_id: str
    token: str
    expiry: datetime
    created_at: datetime = datetime.now()