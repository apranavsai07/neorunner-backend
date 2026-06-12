from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session as DBSession
from app.core.database import get_db
from app.models.events import (
    KeyPressEvent,
    TouchEvent,
    ScrollEvent,
    StrokeEvent,
    UserProfile,
    AuthenticationResult,
)
from app.models.session import Session as SessionModel
from app.models.user import User
from app.schemas.events import (
    KeyPressEventCreate,
    KeyPressEventResponse,
    RawKeyEventBatchCreate,
    TouchEventCreate,
    TouchEventResponse,
    TouchEventBatchCreate,
    ScrollEventCreate,
    ScrollEventResponse,
    ScrollEventBatchCreate,
    StrokeEventCreate,
    StrokeEventResponse,
    StrokeEventBatchCreate,
    UserProfileCreate,
    UserProfileResponse,
    AuthenticationResultCreate,
    AuthenticationResultResponse,
)
from typing import List

router = APIRouter(prefix="/api/v1", tags=["events"])

@router.post("/keypress-event", response_model=KeyPressEventResponse, status_code=status.HTTP_201_CREATED)
def create_keypress_event(
    event: KeyPressEventCreate,
    db: DBSession = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.id == event.session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    new_event = KeyPressEvent(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.post("/touch-event", response_model=TouchEventResponse, status_code=status.HTTP_201_CREATED)
def create_touch_event(
    event: TouchEventCreate,
    db: DBSession = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.id == event.session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    new_event = TouchEvent(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.post("/scroll-event", response_model=ScrollEventResponse, status_code=status.HTTP_201_CREATED)
def create_scroll_event(
    event: ScrollEventCreate,
    db: DBSession = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.id == event.session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    new_event = ScrollEvent(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.post("/stroke-event", response_model=StrokeEventResponse, status_code=status.HTTP_201_CREATED)
def create_stroke_event(
    event: StrokeEventCreate,
    db: DBSession = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.id == event.session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    new_event = StrokeEvent(**event.dict())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event



@router.post("/authentication-results", response_model=AuthenticationResultResponse, status_code=status.HTTP_201_CREATED)
def create_authentication_result(
    result: AuthenticationResultCreate,
    db: DBSession = Depends(get_db)
):
    user = db.query(User).filter(User.id == result.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    session = db.query(SessionModel).filter(SessionModel.id == result.session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    new_result = AuthenticationResult(**result.dict())
    db.add(new_result)
    db.commit()
    db.refresh(new_result)
    return new_result

@router.get("/keypress-event/session/{session_id}", response_model=List[KeyPressEventResponse])
def get_keypress_events_by_session(
    session_id: str,
    db: DBSession = Depends(get_db)
):
    events = db.query(KeyPressEvent).filter(KeyPressEvent.session_id == session_id).all()
    return events

@router.get("/touch-event/session/{session_id}", response_model=List[TouchEventResponse])
def get_touch_events_by_session(
    session_id: str,
    db: DBSession = Depends(get_db)
):
    events = db.query(TouchEvent).filter(TouchEvent.session_id == session_id).all()
    return events

@router.get("/scroll-event/session/{session_id}", response_model=List[ScrollEventResponse])
def get_scroll_events_by_session(
    session_id: str,
    db: DBSession = Depends(get_db)
):
    events = db.query(ScrollEvent).filter(ScrollEvent.session_id == session_id).all()
    return events

@router.get("/stroke-event/session/{session_id}", response_model=List[StrokeEventResponse])
def get_stroke_events_by_session(
    session_id: str,
    db: DBSession = Depends(get_db)
):
    events = db.query(StrokeEvent).filter(StrokeEvent.session_id == session_id).all()
    return events
@router.post("/touch-events/batch")
def create_touch_events_batch(
    payload: TouchEventBatchCreate,
    db: DBSession = Depends(get_db)
):
    if not payload.events:
        return {"inserted": 0}

    events = [
        TouchEvent(**event.dict())
        for event in payload.events
    ]

    db.bulk_save_objects(events)
    db.commit()

    return {"inserted": len(events)}

@router.post("/scroll-events/batch")
def create_scroll_events_batch(
    payload: ScrollEventBatchCreate,
    db: DBSession = Depends(get_db)
):
    if not payload.events:
        return {"inserted": 0}

    

    events = [
        ScrollEvent(**event.dict())
        for event in payload.events
    ]

    db.bulk_save_objects(events)
    db.commit()

    return {
        "inserted": len(events)
    }
@router.post("/stroke-events/batch")
def create_stroke_events_batch(
    payload: StrokeEventBatchCreate,
    db: DBSession = Depends(get_db)
):
    if not payload.events:
        return {"inserted": 0}

    

    events = [
        StrokeEvent(**event.dict())
        for event in payload.events
    ]

    db.bulk_save_objects(events)
    db.commit()

    return {
        "inserted": len(events)
    }
@router.post("/raw-key-events/batch")
def create_raw_key_events_batch(
    payload: RawKeyEventBatchCreate,
    db: DBSession = Depends(get_db)
):
    if not payload.events:
        return {"inserted": 0}

    

    events = [
        KeyPressEvent(**event.dict())
        for event in payload.events
    ]

    db.bulk_save_objects(events)
    db.commit()

    return {
        "inserted": len(events)
    }