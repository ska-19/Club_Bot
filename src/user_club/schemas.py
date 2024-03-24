from datetime import datetime

from pydantic import BaseModel


class UserJoin(BaseModel):
    club_id: int
    user_id: int
    role: str = 'member'


class UpdateRole(BaseModel):
    club_id: int
    user_id: int
    role: str


class UserDisjoin(BaseModel):
    club_id: int
    user_id: int
