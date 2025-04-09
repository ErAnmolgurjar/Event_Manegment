# Event Management API (FastAPI)

A RESTful API to manage events and attendees — with scheduling, registration, check-ins, and status tracking. Built using FastAPI, SQLAlchemy, and JWT authentication.

---


## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/event-management-api.git
cd event-management-api
```

2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install Dependencies

```bash
pip install -r requirements.txt
```


5. Seed an Initial User
```bash
python -m app.seed_user
```
Creates a default user:

username: admin

password: secret


6. Run the App
```bash
uvicorn app.main:app --reload
```

Visit docs: http://127.0.0.1:8000/docs

Authentication
Get JWT token:

http
Copy
Edit
POST /token
Content-Type: application/x-www-form-urlencoded
Body:

ini
Copy
Edit
username=admin
password=secret
Use the returned token as:

makefile
Copy
Edit
Authorization: Bearer <your_token>
API Endpoints
Create Event
http
Copy
Edit
POST /events/
Authorization: Bearer <token>
Body:

json
Copy
Edit
{
  "name": "My Event",
  "description": "Fun event",
  "start_time": "2025-05-01T10:00:00",
  "end_time": "2025-05-01T12:00:00",
  "location": "New York",
  "max_attendees": 100
}
Update Event
http
Copy
Edit
PUT /events/{event_id}
Authorization: Bearer <token>
Register Attendee
http
Copy
Edit
POST /events/{event_id}/register
Body:

json
Copy
Edit
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone_number": "1234567890"
}
Check-In Attendee
http
Copy
Edit
POST /events/{event_id}/checkin/{attendee_id}
Authorization: Bearer <token>
List Events
http
Copy
Edit
GET /events/
Query params:

status

location

date

Example:

http
Copy
Edit
GET /events/?status=scheduled&location=NY
List Attendees
http
Copy
Edit
GET /events/{event_id}/attendees
Optional query param:

check_in_status=true or false

Bulk Check-In (CSV)
http
Copy
Edit
POST /events/{event_id}/bulk-checkin
Authorization: Bearer <token>
Content-Type: multipart/form-data
Form field:

file: CSV file with column attendee_id

Seed User Script Example
python
Copy
Edit
# app/seed_user.py
from app.database import SessionLocal, engine
from app.models import Base
from app.crud import create_user

Base.metadata.create_all(bind=engine)
db = SessionLocal()
create_user(db, username="admin", password="secret")
db.close()
Run it:

bash
Copy
Edit
python -m app.seed_user
