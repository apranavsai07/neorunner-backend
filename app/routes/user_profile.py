from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.events import UserProfile
from app.schemas.user_profile import (
    UserProfileCreate,
    UserProfileResponse,
)

router = APIRouter(
    prefix="/api/v1/user-profiles",
    tags=["user-profiles"],
)


@router.get(
    "/{user_id}",
    response_model=UserProfileResponse,
)
def get_profile(
    user_id: str,
    db: Session = Depends(get_db),
):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    return profile


@router.post(
    "",
    response_model=UserProfileResponse,
)
def create_profile(
    profile: UserProfileCreate,
    db: Session = Depends(get_db),
):

    new_profile = UserProfile(
        **profile.model_dump()
    )

    new_profile.enrollment_complete = True
    new_profile.profile_completed = True

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return new_profile


@router.put("/{user_id}/stats")
def update_stats(
    user_id: str,
    stats: dict,
    db: Session = Depends(get_db),
):
    profile = (
        db.query(UserProfile)
        .filter(UserProfile.user_id == user_id)
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found",
        )

    profile.xp += stats["xp"]
    profile.coins += stats["coins"]
    profile.total_distance += stats["distance"]
    profile.sessions_collected += 1

    if stats["score"] > profile.highest_score:
        profile.highest_score = stats["score"]

    profile.level = max(
        1,
        (profile.xp // 500) + 1,
    )

    db.commit()
    db.refresh(profile)

    return {
        "message": "Stats updated"
    }