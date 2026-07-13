# GenerativeAI Project

This project is a simple Flask-based user management API that uses SQLAlchemy for database access, Celery for background task processing, and Redis as the message/result broker. It also includes Alembic for database migrations.

## Features

- Create, read, update, and delete users
- Async user listing using Celery tasks
- SQLite database storage
- Database migrations with Alembic
- Redis-backed task execution and result tracking

## Technologies Used

- Python
- Flask
- SQLAlchemy
- Celery
- Redis
- Alembic
- SQLite

## Project Structure

- [server.py](server.py) - Flask application and API routes
- [db/session.py](db/session.py) - Database session setup
- [db/User.py](db/User.py) - User model
- [main.py](main.py) - Simple Streamlit example
- [alembic/](alembic/) - Database migration files
- [alembic.ini](alembic.ini) - Alembic configuration

## Requirements

Install the required packages:

```bash
pip install flask sqlalchemy celery redis alembic
```

## Setup

1. Make sure Redis is running on your machine:

```bash
redis-server
```

2. Start the Flask server:

```bash
python server.py
```

3. Start a Celery worker in a separate terminal:

```bash
celery -A server.celery_app worker --loglevel=info
```

The app will run on:

```bash
http://127.0.0.1:5000
```

## API Endpoints

### Health Check

```bash
curl http://127.0.0.1:5000/
```

### List Users (Async)

```bash
curl http://127.0.0.1:5000/users
```

This returns a task ID and status:

```json
{
  "status": "processing",
  "task_id": "<task-id>"
}
```

To get the result of the task:

```bash
curl http://127.0.0.1:5000/users/<task-id>
```

### Add a User

```bash
curl -X POST http://127.0.0.1:5000/user \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "age": 25,
    "email": "alice@example.com"
  }'
```

### Update a User

```bash
curl -X PUT http://127.0.0.1:5000/updateUser \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1,
    "name": "Alice Updated",
    "age": 26,
    "email": "alice@example.com"
  }'
```

### Delete a User

```bash
curl -X DELETE http://127.0.0.1:5000/deleteUser \
  -H "Content-Type: application/json" \
  -d '{
    "id": 1
  }'
```

## Database

The project uses a SQLite database file named:

```bash
mydb.db
```

The User table includes:

- id
- name
- age
- email

## Migrations

Alembic is configured to manage database migrations. You can use commands like:

```bash
alembic revision --autogenerate -m "message"
alembic upgrade head
```

## Notes

- The async listing endpoint uses Celery and Redis, so the Celery worker must be running for task execution.
- If Redis or the worker is not running, the task will not complete.
