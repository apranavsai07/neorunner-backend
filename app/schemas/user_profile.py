from pydantic import BaseModel
from datetime import datetime


class UserProfileCreate(BaseModel):
    user_id: str

    avatar_id: int
    nickname: str

    level: int = 1
    xp: int = 0
    coins: int = 0

    total_distance: float = 0.0
    highest_score: int = 0

    tier: str = "D Tier"

    sessions_collected: int = 0
    enrollment_complete: bool = False
    profile_completed: bool = True


class UserProfileResponse(BaseModel):
    user_id: str

    avatar_id: int
    nickname: str

    level: int
    xp: int
    coins: int

    total_distance: float
    highest_score: int

    tier: str

    sessions_collected: int
    enrollment_complete: bool
    profile_completed: bool

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True