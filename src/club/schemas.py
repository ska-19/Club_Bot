from datetime import datetime, date

from pydantic import BaseModel
from typing import Optional


class ClubCreate(BaseModel):
    owner: int
    name: str
    dest: str
    bio: str
    channel_link: str


class ClubRead(BaseModel):
    pass


class ClubUpdate(BaseModel):
    name: str
    dest: str
    photo: str
    bio: str
    links: str
    comfort_time: str
    channel_link: str
    date_created: date


class FoundUid(BaseModel):
    uid: str = "havent tried searching"
