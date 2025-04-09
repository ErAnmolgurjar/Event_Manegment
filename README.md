# Event Management API (FastAPI)

A RESTful API to manage events and attendees — with scheduling, registration, check-ins, and status tracking. Built using FastAPI, SQLAlchemy, and JWT authentication.

---


## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/event-management-api.git
cd event-management-api
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```


### 4. Seed an Initial User
```bash
python -m app.seed_user
```
It will Creates a default user:

username: admin

password: secret


### 5. Run the App
```bash
uvicorn app.main:app --reload
```

```bash
Visit docs: http://127.0.0.1:8000/docs
```