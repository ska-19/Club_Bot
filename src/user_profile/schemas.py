from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    id: int  # tg id
    username: str  # tg username
    mentor: bool = False
    name: str  # tg name
    surname: str  # tg surname
    # date_joined: datetime = datetime.utcnow
    # password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    class Config:
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    name: str
    surname: str
    email: str
    tel: str
    photo: str  # ссылка на фото
    comfort_time: str  # удобное время для встреч
    course: str
    faculty: str
    links: str  # ссылки на соц сети
    bio: str  # о себе
    dob: date
    city: str
    education: str

    class Config:
        arbitrary_types_allowed = True


# class UserRead(BaseModel):
#     id: int
#     username: str
#     mentor: bool = False
#     email: str
#     name: str
#     surname: str
#     # dob: datetime
#     tel: str
#     # date_joined: datetime = datetime.utcnow
#     photo: str
#     comfort_time: str
#     course: str
#     faculty: str
#     links: str
#     bio: str
#     is_active: bool = True
#     is_superuser: bool = False
#     is_verified: bool = False
#
#     class Config:
#         orm_mode = True
#         arbitrary_types_allowed = True
