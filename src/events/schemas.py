from datetime import datetime, date

from pydantic import BaseModel


class EventCreate(BaseModel):
    club_id: int
    host_id: int
    name: str
    date: date
    sinopsis: str
    contact: str
    speaker: str


class EventUpdate(BaseModel):
    club_id: int
    host_id: int
    name: str
    date: date
    sinopsis: str
    contact: str
    speaker: str


class EventReg(BaseModel):
    user_id: int
    event_id: int
    confirm: bool
    reg_date: date