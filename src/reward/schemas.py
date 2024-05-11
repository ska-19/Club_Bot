from datetime import datetime

from pydantic import BaseModel


class AddRewardClub(BaseModel):
    info: str
    exp: int
    admin_id: int
    club_id: int


class UpdateRewardClub(BaseModel):
    info: str
    exp: int
    admin_id: int
    club_id: int


class AddRewardUser(BaseModel):
    admin_id: int
    user_id: int
    club_x_reward_id: int
