from datetime import datetime

from pydantic import BaseModel


class UserJoin(BaseModel):
    club_id: int
    user_id: int
    role: str
