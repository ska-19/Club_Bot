from datetime import datetime

from pydantic import BaseModel


class UserJoin(BaseModel):
    club_id: int
    user_id: int
    role: str = 'member'
    balance: int = 0


class UpdateRole(BaseModel):
    club_id: int
    user_id: int
    new_role: str


class UpdateBalance(BaseModel):
    club_id: int
    user_id: int
    plus_balance: int


class User(BaseModel):
    club_id: int
    user_id: int
