from datetime import datetime, date

from pydantic import BaseModel


class EventCreate(BaseModel):
    name: str
    club_id: int
    host_id: int
    date: date
    sinopsis: str
    contact: str
    speaker: str
    reward: int


class EventUpdate(BaseModel):
    club_id: int
    host_id: int
    date: date
    sinopsis: str
    contact: str
    speaker: str


class EventReg(BaseModel):
    user_id: int
    event_id: int
    # confirm: bool


class Data(BaseModel):
    users: dict