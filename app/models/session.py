from sqlalchemy import Column, Integer, String, DateTime, ForeignKey , BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
import uuid

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    started_at = Column(BigInteger,nullable=False)
    current_screen = Column(String, nullable=True)
    
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    keypress_events = relationship("KeyPressEvent", back_populates="session", cascade="all, delete-orphan")
    touch_events = relationship("TouchEvent", back_populates="session", cascade="all, delete-orphan")
    scroll_events = relationship("ScrollEvent", back_populates="session", cascade="all, delete-orphan")
    stroke_events = relationship("StrokeEvent", back_populates="session", cascade="all, delete-orphan")
    authentication_results = relationship("AuthenticationResult", back_populates="session", cascade="all, delete-orphan")
