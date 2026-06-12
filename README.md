# NeoRunner Behavioral Biometric Backend

FastAPI backend for NeoRunner's continuous authentication system. Collects and persists HMOG-compatible behavioral biometric events.

## Features

- User registration & login with JWT authentication
- Session management
- HMOG-compatible raw keystroke event collection
- Touch, scroll, and stroke event ingestion
- PostgreSQL persistence with SQLAlchemy ORM
- Pydantic validation
- Full OpenAPI documentation

## Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 12+

### Installation

1. Clone the repository
```bash
git clone <repo>
cd neorunner-backend
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Create `.env` file from template
```bash
cp .env.example .env
```

5. Configure PostgreSQL connection in `.env`
```
DATABASE_URL=postgresql://user:password@localhost:5432/neorunner_db
SECRET_KEY=your-secret-key-here
```

6. Run migrations (if using Alembic)
```bash
alembic upgrade head
```

7. Start the server
```bash
python main.py
```

Or using Uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Health Check
- `GET /` - Root info
- `GET /health` - Health status

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token

### Session Management
- `POST /api/v1/session/start` - Start new session
- `POST /api/v1/session/end/{session_id}` - End session

### Events (Behavioral Biometric Data)
- `POST /api/v1/events/raw-keypress` - Create raw keystroke event
- `POST /api/v1/events/touch` - Create touch event
- `POST /api/v1/events/scroll` - Create scroll event
- `POST /api/v1/events/stroke` - Create stroke event
- `GET /api/v1/events/raw-keypress/session/{session_id}` - Get keystroke events
- `GET /api/v1/events/touch/session/{session_id}` - Get touch events
- `GET /api/v1/events/scroll/session/{session_id}` - Get scroll events
- `GET /api/v1/events/stroke/session/{session_id}` - Get stroke events

## Example Requests

### Register User
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123",
    "email": "user@example.com",
    "full_name": "Test User"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

### Start Session
```bash
curl -X POST "http://localhost:8000/api/v1/session/start" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<user_id_from_login>",
    "current_screen": "login"
  }'
```

### Create Raw Keystroke Event
```bash
curl -X POST "http://localhost:8000/api/v1/events/raw-keypress" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<user_id>",
    "session_id": "<session_id>",
    "activity_id": "login",
    "screen_name": "login",
    "system_time": 1680000000100,
    "press_time": 100,
    "press_type": 0,
    "key_id": "a",
    "key_value": "a",
    "phone_orientation": "portrait",
    "text_before": "",
    "text_after": "a",
    "source": "hardware"
  }'
```

### Create Touch Event
```bash
curl -X POST "http://localhost:8000/api/v1/events/touch" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "<user_id>",
    "session_id": "<session_id>",
    "timestamp": 1680000000100,
    "event_time": 100,
    "pointer_id": 1,
    "pointer_count": 1,
    "action_type": "down",
    "x": 150.5,
    "y": 300.2,
    "pressure": 0.8,
    "size": 0.5,
    "orientation": 0.0,
    "screen_name": "login"
  }'
```

## Database Schema

### Users
- id (UUID)
- username (unique)
- email (unique)
- hashed_password
- full_name
- is_active
- created_at
- updated_at

### Sessions
- id (UUID)
- user_id (FK)
- started_at
- ended_at
- current_screen
- created_at

### Raw Key Events (HMOG-compatible)
- id (UUID)
- user_id (FK)
- session_id (FK)
- activity_id
- screen_name
- system_time
- press_time
- press_type (0=DOWN, 1=UP, 2=TEXT_COMMIT, 3=BACKSPACE, 4=COMPOSITION)
- key_id
- key_value
- phone_orientation
- text_before
- text_after
- source (hardware, soft_keyboard, legacy)
- created_at

### Touch Events
- id, user_id, session_id, timestamp, event_time, pointer_id, pointer_count, action_type, x, y, pressure, size, orientation, screen_name, created_at

### Scroll Events
- id, user_id, session_id, begin_time, current_time, scroll_id, start_x, start_y, current_x, current_y, distance_x, distance_y, pressure, size, orientation, screen_name, created_at

### Stroke Events
- id, user_id, session_id, stroke_id, start_time, end_time, start_x, start_y, end_x, end_y, start_pressure, end_pressure, start_size, end_size, speed_x, speed_y, orientation, screen_name, created_at

## Development

### Run tests
```bash
pytest
```

### Generate Alembic migrations
```bash
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

### Format code
```bash
black .
```

### Lint
```bash
pylint app/
```

## Architecture

```
neorunner-backend/
├── app/
│   ├── core/           # Config, database, security
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic validation schemas
│   └── routes/         # API endpoint handlers
├── main.py             # Application entry point
├── requirements.txt    # Dependencies
├── .env.example        # Configuration template
└── README.md
```

## Future Work

- ML inference for continuous authentication
- Feature engineering from raw events
- Anomaly detection endpoints
- User behavior profile analysis
- Admin dashboard
