from .database import SessionLocal, engine
from . import models
from .crud import create_user

models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Replace with your desired username and password
create_user(db, username="admin", password="secret")

db.close()
