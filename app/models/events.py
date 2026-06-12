from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean, Text , BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.base import Base
import uuid
from sqlalchemy import BigInteger
import time

class KeyPressEvent(Base):
    __tablename__ = "raw_key_events"
    
    id = Column(BigInteger, primary_key=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, index=True)
    system_time = Column(BigInteger, nullable=False)
    press_time = Column(BigInteger, nullable=False)
    press_type = Column(Integer, nullable=False)
    key_id = Column(String, nullable=True)
    key_value = Column(String, nullable=True)
    phone_orientation = Column(String, nullable=True)
    screen_name = Column(String, nullable=True)
    created_at = Column(BigInteger,nullable=False,default=lambda: int(time.time() * 1000))
    activity_id = Column(String)
    text_before = Column(Text)
    text_after = Column(Text)
    source = Column(String)
    
    session = relationship("Session", back_populates="keypress_events")

class TouchEvent(Base):
    __tablename__ = "touch_events"
    
    id = Column(BigInteger, primary_key=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, index=True)
    timestamp = Column(BigInteger, nullable=False)
    event_time = Column(BigInteger, nullable=False)
    pointer_id = Column(Integer, nullable=False)
    pointer_count = Column(Integer, nullable=False)
    action_type = Column(String, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    size = Column(Float, nullable=False)
    orientation = Column(Float, nullable=False)
    screen_name = Column(String, nullable=True)
    
    session = relationship("Session", back_populates="touch_events")

class ScrollEvent(Base):
    __tablename__ = "scroll_events"
    
    id = Column(BigInteger, primary_key=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, index=True)
    begin_time = Column(BigInteger, nullable=False)
    current_time = Column(BigInteger, nullable=False)
    scroll_id = Column(String, nullable=False)
    start_x = Column(Float, nullable=False)
    start_y = Column(Float, nullable=False)
    current_x = Column(Float, nullable=False)
    current_y = Column(Float, nullable=False)
    distance_x = Column(Float, nullable=False)
    distance_y = Column(Float, nullable=False)
    pressure = Column(Float, nullable=False)
    size = Column(Float, nullable=False)
    orientation = Column(Float, nullable=False)
    screen_name = Column(String, nullable=True)
    
    
    session = relationship("Session", back_populates="scroll_events")

class StrokeEvent(Base):
    __tablename__ = "stroke_events"
    
    id = Column(BigInteger, primary_key=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, index=True)
    stroke_id = Column(String, nullable=False)
    start_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False)
    start_x = Column(Float, nullable=False)
    start_y = Column(Float, nullable=False)
    end_x = Column(Float, nullable=False)
    end_y = Column(Float, nullable=False)
    start_pressure = Column(Float, nullable=False)
    end_pressure = Column(Float, nullable=False)
    start_size = Column(Float, nullable=False)
    end_size = Column(Float, nullable=False)
    speed_x = Column(Float, nullable=False)
    speed_y = Column(Float, nullable=False)
    orientation = Column(Float, nullable=False)
    screen_name = Column(String, nullable=True)
    
    
    session = relationship("Session", back_populates="stroke_events")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(
        String,
        ForeignKey("users.id"),
        primary_key=True,
    )

    avatar_id = Column(Integer)
    nickname = Column(String)

    level = Column(Integer, default=1)
    xp = Column(Integer, default=0)
    coins = Column(Integer, default=0)

    total_distance = Column(Float, default=0.0)
    highest_score = Column(Integer, default=0)

    tier = Column(String, default="D Tier")

    sessions_collected = Column(Integer, default=0)
    enrollment_complete = Column(Boolean, default=False)
    profile_completed = Column(Boolean, default=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = relationship(
        "User",
        back_populates="profile",
    )

class AuthenticationResult(Base):
    __tablename__ = "authentication_results"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), nullable=False, index=True)
    prediction = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="authentication_results")
    session = relationship("Session", back_populates="authentication_results")
