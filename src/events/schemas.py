from datetime import date
from pydantic import BaseModel


class EventCreate(BaseModel):
    name: str
    club_id: int
    host_id: int
    date: date
    sinopsis: str
    contact: str
    speaker: str
    reward: int = -1


class EventUpdate(BaseModel):
    club_id: int
    host_id: int
    name: str
    date: date
    sinopsis: str
    contact: str
    speaker: str
    reward: int = -1


class EventReg(BaseModel):
    user_id: int
    event_id: int


class Data(BaseModel):
    users: dict