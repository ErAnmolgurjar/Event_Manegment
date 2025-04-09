from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas
from fastapi import HTTPException, UploadFile
import csv
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, username: str, password: str):
    hashed_password = pwd_context.hash(password)
    user = models.User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_event(db: Session, event: schemas.EventCreate):
    db_event = models.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def update_event(db: Session, event_id: int, event: schemas.EventUpdate):
    db_event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    for key, value in event.dict(exclude_unset=True).items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

def register_attendee(db: Session, event_id: int, attendee: schemas.AttendeeCreate):
    event = db.query(models.Event).filter(models.Event.event_id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    if len(event.attendees) >= event.max_attendees:
        raise HTTPException(status_code=400, detail="Max attendees reached")
    existing = db.query(models.Attendee).filter(models.Attendee.email == attendee.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_attendee = models.Attendee(**attendee.dict(), event_id=event_id)
    db.add(new_attendee)
    db.commit()
    db.refresh(new_attendee)
    return new_attendee

def check_in_attendee(db: Session, attendee_id: int):
    attendee = db.query(models.Attendee).filter(models.Attendee.attendee_id == attendee_id).first()
    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found")
    attendee.check_in_status = True
    db.commit()
    return attendee

def list_events(db: Session, status=None, location=None, date=None):
    query = db.query(models.Event)
    if status:
        query = query.filter(models.Event.status == status)
    if location:
        query = query.filter(models.Event.location == location)
    if date:
        query = query.filter(models.Event.start_time >= date)
    return query.all()

def list_attendees(db: Session, event_id: int):
    return db.query(models.Attendee).filter(models.Attendee.event_id == event_id).all()

def bulk_check_in(db: Session, event_id: int, file: UploadFile):
    reader = csv.DictReader(file.file.read().decode("utf-8").splitlines())
    updated = 0
    for row in reader:
        email = row.get("email")
        attendee = db.query(models.Attendee).filter_by(email=email, event_id=event_id).first()
        if attendee:
            attendee.check_in_status = True
            updated += 1
    db.commit()
    return {"updated": updated}
