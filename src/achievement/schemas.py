from datetime import datetime

from pydantic import BaseModel


class AddAchievementClub(BaseModel):
    info: str
    exp: int
    admin_id: int
    club_id: int


class UpdateAchievementClub(BaseModel):
    info: str
    exp: int
    admin_id: int
    club_id: int


class AddAchievementUser(BaseModel):
    info: str
    exp: int
    admin_id: int
    user_id: int
    club_x_achievement_id: int
