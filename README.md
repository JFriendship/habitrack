# HabiTrack

A FastAPI-based habit tracking application with JWT authentication, PostgreSQL persistence, SQLAlchemy 2.0, Alembic migrations, and Dockerized development.

## Current Status

Implemented so far:
- FastAPI backend scaffold
- Docker and Docker Compose setup
- PostgreSQL integration
- SQLAlchemy 2.0 database layer
- Alembic migrations
- User registration and login
- JWT authentication
- Protected routes
- Habit CRUD
- Habit completion tracking
- Pytest-based testing foundation

Planned next:
- Basic frontend
- Guest mode with localStorage
- Habit syncing from guest mode into an account
- Additional testing and deployment polish

## Tech Stack

- **Backend:** FastAPI, Python 3.12
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0
- **Migrations:** Alembic
- **Auth:** JWT, OAuth2 password flow
- **Testing:** pytest, TestClient
- **Containerization:** Docker, Docker Compose

## Features

### Authentication
- Register a new user
- Log in with email and password
- Receive a JWT access token
- Access protected routes with the token

### Habits
- Create, read, update, and delete habits
- Habits belong to a specific user
- Prevent users from accessing other users’ habits

### Habit Completion
- Mark a habit complete for a given date
- Unmark a completion
- View completion history
- Check whether a habit is completed on a specific date

## Project Structure

```text
habitrack/
├── backend/
│   ├── .env
│   ├── alembic/
│   ├── alembic.ini
│   ├── app/
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routes/
│   │   │       ├── auth.py
│   │   │       ├── db_check.py
│   │   │       ├── health.py
│   │   │       └── habits.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── constants.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   └── dependencies.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── habit.py
│   │   │   ├── habit_completion.py
│   │   │   └── user.py
│   │   ├── repositories/
│   │   │   ├── habit_completion_repositories.py
│   │   │   ├── habit_repository.py
│   │   │   └── user_repository.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── habit.py
│   │   │   ├── habit_completion.py
│   │   │   └── user.py
│   │   ├── services/
│   │   │   ├── habit_completion_service.py
│   │   │   ├── habit_service.py
│   │   │   └── user_service.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
│       ├── api/
│       ├── repositories/
│       └── services/
├── frontend/
└── docker-compose.yml
```

## Environment Variables

Create `backend/.env`:

```env
APP_NAME=Habit Tracker
DEBUG=True
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/habits
SECRET_KEY=YourVeryOwnSecretKeyThatYouShouldProbablyChangeOrYouCouldJustUseThisIfYouWant
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Local Development

### 1. Clone the repository
```bash
git clone https://github.com/JFriendship/habitrack.git
cd habitrack
```

### 2. Start PostgreSQL and the backend
```bash
docker compose up --build
```

### 3. Apply migrations
If migrations are not applied automatically, you should run:

```bash
docker compose exec backend alembic upgrade head
```

### 4. Open the app
- FastAPI docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

## Running Without Docker

If you prefer local Python execution, this is for you:

### 1. Create and activate a virtual environment
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run migrations
```bash
alembic upgrade head
```

### 4. Start the app
```bash
uvicorn app.main:app --reload
```

## Database and Migrations

This project uses Alembic for schema changes.

### Here are some useful commands:

I used this one for generating the new alembic version file.  
You can think of this as `git add` if you are familiar with git.
```bash
docker compose exec backend alembic revision --autogenerate -m "message"
```

Upgrading the head applies the changes that you made to the database.  
This is very similar to using `git commit`.
```bash
docker compose exec backend alembic upgrade head
```

Finally, this command reverts to the database configuration right before the last database configuration change. This reverts to a state before the last alembic revision and upgrade head
```bash
docker compose exec backend alembic downgrade -1
```

## Authentication Flow

1. Register with email and password.
2. Log in to receive a JWT access token.
3. Send the token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

Protected routes use `get_current_user()` to validate the token and load the user.

## Main API Endpoints

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`

### User
- `GET /api/users/me`

### Habits
- `POST /api/habits`
- `GET /api/habits`
- `PUT /api/habits/{habit_id}`
- `DELETE /api/habits/{habit_id}`

### Habit Completion
- `POST /api/habits/{habit_id}/complete`
- `DELETE /api/habits/{habit_id}/complete/{completed_date}`
- `GET /api/habits/{habit_id}/completions`
- `GET /api/habits/{habit_id}/completed-on/{completed_date}`

## Testing

Run tests with:

```bash
docker compose exec backend pytest
```

Or, if you're running locally from `backend/`:

```bash
pytest
```

The test suite uses:
- `TestClient` for API tests
- a test database/session fixture for repository and service tests


## Roadmap

- Build a basic frontend
- Add guest mode with localStorage
- Import guest habits into an account
- Add streaks and completion analytics
- Add better test coverage
- Add deployment documentation
