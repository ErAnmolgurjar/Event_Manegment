from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import models, schemas, database, crud, auth
from .database import engine
from typing import List
from datetime import timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    access_token = auth.create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/events", response_model=schemas.EventOut)
def create_event(event: schemas.EventCreate, db: Session = Depends(database.get_db), user: dict = Depends(auth.get_current_user)):
    return crud.create_event(db, event)

@app.put("/events/{event_id}", response_model=schemas.EventOut)
def update_event(event_id: int, event: schemas.EventUpdate, db: Session = Depends(database.get_db), user: dict = Depends(auth.get_current_user)):
    return crud.update_event(db, event_id, event)

@app.post("/events/{event_id}/register", response_model=schemas.AttendeeOut)
def register_attendee(event_id: int, attendee: schemas.AttendeeCreate, db: Session = Depends(database.get_db)):
    return crud.register_attendee(db, event_id, attendee)

@app.post("/attendees/{attendee_id}/checkin", response_model=schemas.AttendeeOut)
def check_in(attendee_id: int, db: Session = Depends(database.get_db), user: dict = Depends(auth.get_current_user)):
    return crud.check_in_attendee(db, attendee_id)

@app.post("/events/{event_id}/bulk-checkin")
def bulk_check_in(event_id: int, file: UploadFile = File(...), db: Session = Depends(database.get_db), user: dict = Depends(auth.get_current_user)):
    return crud.bulk_check_in(db, event_id, file)

@app.get("/events", response_model=List[schemas.EventOut])
def get_events(status: str = None, location: str = None, date: str = None, db: Session = Depends(database.get_db)):
    return crud.list_events(db, status, location, date)

@app.get("/events/{event_id}/attendees", response_model=List[schemas.AttendeeOut])
def get_attendees(event_id: int, db: Session = Depends(database.get_db), user: dict = Depends(auth.get_current_user)):
    return crud.list_attendees(db, event_id)
