from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    id: int
    username: str
    mentor: Optional[bool] = False
    name: str
    surname: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    bio: str
    dob: date
    city: str
    education: str

    class Config:
        arbitrary_types_allowed = True


class UserCUpdate(BaseModel):
    username: str
    name: str
    surname: str

    class Config:
        arbitrary_types_allowed = True


class UserLUpdate(BaseModel):
    links: str

    class Config:
        arbitrary_types_allowed = True
