from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .models import EventStatus

class EventCreate(BaseModel):
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int

class EventUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    location: Optional[str]
    max_attendees: Optional[int]
    status: Optional[EventStatus]

class EventOut(BaseModel):
    event_id: int
    name: str
    description: str
    start_time: datetime
    end_time: datetime
    location: str
    max_attendees: int
    status: EventStatus

    class Config:
        orm_mode = True

class AttendeeCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str

class AttendeeOut(BaseModel):
    attendee_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    check_in_status: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None