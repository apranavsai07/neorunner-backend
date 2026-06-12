from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.session import Session as SessionModel
from app.models.user import User
from app.core.security import decode_token
from app.schemas.events import SessionCreate, SessionResponse
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/v1/session", tags=["session"])

def get_current_user(token: Optional[str] = None, db: Session = Depends(get_db)) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.post("/start", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def start_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == session_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    new_session = SessionModel(
        id=session_data.id,
        user_id=session_data.user_id,
        started_at=session_data.started_at,
        current_screen=session_data.current_screen,
    )
    
    db.add(new_session)
    db.commit()
    db.refresh(new_session)
    
    return new_session

@router.post("/end/{session_id}", response_model=SessionResponse)
def end_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    session.ended_at = datetime.utcnow()
    db.commit()
    db.refresh(session)
    
    return session
