from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from typing import List

class SessionCreate(BaseModel):
    id : str
    user_id: str
    current_screen: Optional[str] = None
    started_at:  int


class SessionResponse(BaseModel):
    id: str
    user_id: str
    started_at: datetime
    current_screen: Optional[str] = None
   
    
    class Config:
        from_attributes = True


class KeyPressEventCreate(BaseModel):
    session_id: str
    system_time: int
    press_time: int
    press_type: int
    key_id: Optional[str] = None
    key_value: Optional[str] = None
    phone_orientation: Optional[str] = None
    screen_name: Optional[str] = None
    activity_id: Optional[str] = None
    text_before: Optional[str] = None
    text_after: Optional[str] = None
    source: Optional[str] = None

class KeyPressEventResponse(KeyPressEventCreate):
    id: int
    created_at: int

    class Config:
        from_attributes = True

class TouchEventCreate(BaseModel):
    session_id: str
    timestamp: int
    event_time: int
    pointer_id: int
    pointer_count: int
    action_type: str
    x: float
    y: float
    pressure: float
    size: float
    orientation: float
    screen_name: Optional[str] = None

class TouchEventResponse(TouchEventCreate):
    id: int
    
    
    class Config:
        from_attributes = True

class ScrollEventCreate(BaseModel):
    session_id: str
    begin_time: int
    current_time: int
    scroll_id: str
    start_x: float
    start_y: float
    current_x: float
    current_y: float
    distance_x: float
    distance_y: float
    pressure: float
    size: float
    orientation: float
    screen_name: Optional[str] = None

class ScrollEventResponse(ScrollEventCreate):
    id: int
    
    
    class Config:
        from_attributes = True

class StrokeEventCreate(BaseModel):
    session_id: str
    stroke_id: str
    start_time: int
    end_time: int
    start_x: float
    start_y: float
    end_x: float
    end_y: float
    start_pressure: float
    end_pressure: float
    start_size: float
    end_size: float
    speed_x: float
    speed_y: float
    orientation: float
    screen_name: Optional[str] = None

class StrokeEventResponse(StrokeEventCreate):
    id: int
    
    
    class Config:
        from_attributes = True

class AuthenticationResultCreate(BaseModel):
    user_id: str
    session_id: str
    prediction: Optional[str] = None
    confidence: Optional[float] = None

class AuthenticationResultResponse(AuthenticationResultCreate):
    id: str
    timestamp: datetime

    class Config:
        from_attributes = True

class UserProfileCreate(BaseModel):
    user_id: str
    sessions_collected: int = 0
    enrollment_complete: bool = False

class UserProfileResponse(BaseModel):
    user_id: str
    sessions_collected: int
    enrollment_complete: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TouchEventBatchCreate(BaseModel):
    events: List[TouchEventCreate]



class ScrollEventBatchCreate(BaseModel):
    events: List[ScrollEventCreate]

class StrokeEventBatchCreate(BaseModel):
    events: List[StrokeEventCreate]

class RawKeyEventBatchCreate(BaseModel):
    events: List[KeyPressEventCreate]