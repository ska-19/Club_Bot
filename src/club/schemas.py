from datetime import datetime

from pydantic import BaseModel


class ClubCreate(BaseModel):
    owner: str
    name: str
    dest: str
    photo: str
    bio: str
    links: str
    comfort_time: str


class ClubRead(BaseModel):
    pass


class ClubUpdate(BaseModel):
    pass
