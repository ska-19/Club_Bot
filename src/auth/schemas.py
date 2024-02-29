from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from sqlalchemy import TIMESTAMP

class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    mentor: bool = False
    email: str
    name: str
    surname: str
    # dob: datetime
    tel: str
    # date_joined: datetime = datetime.utcnow
    photo: str
    comfort_time: str
    course: str
    faculty: str
    links: str
    bio: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserCreate(schemas.BaseUserCreate):
    id: int
    username: str
    mentor: bool = False
    email: str
    name: str
    surname: str
    # dob: datetime
    tel: str
    # date_joined: datetime = datetime.utcnow
    photo: str
    comfort_time: str
    course: str
    faculty: str
    links: str
    bio: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True


class UserUpdate(schemas.BaseUserCreate):
    username: str
    name: str
    surname: str
    tel: str
    photo: str
    comfort_time: str
    course: str
    faculty: str
    links: str
    bio: str

    class Config:
        arbitrary_types_allowed = True

# class UserRead(schemas.BaseUser[int]):
#     id: int
#     email: str
#     username: str
#     role_id: int
#     is_active: bool = True
#     is_superuser: bool = False
#     is_verified: bool = False
#
#     class Config:
#         orm_mode = True
#
#
# class UserCreate(schemas.BaseUserCreate):
#     username: str
#     email: str
#     password: str
#     role_id: int
#     is_active: Optional[bool] = True
#     is_superuser: Optional[bool] = False
#     is_verified: Optional[bool] = False