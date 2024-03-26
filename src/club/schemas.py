from datetime import datetime, date

from pydantic import BaseModel


class ClubCreate(BaseModel):
    owner: int
    name: str
    dest: str
    photo: str
    bio: str
    links: str
    channel_link: str
    comfort_time: str
    date_created: date


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
