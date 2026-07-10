# Eco Game Backend

This project is an economic simulation where the backend manages game state, calculations, and business rules. The client communicates with the backend through an API but does not directly control game data.

## Features

- Turn-based economic simulation
- Persistent player state
- Income source management
- API-based communication

## Tech stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest


## Project structure

| Directory | Purpose |
|-----------|---------|
| `app/api` | HTTP endpoints and request handling |
| `app/services` | Business logic and game rules |
| `app/persistence` | Database operations |
| `app/domain` | Core models and schemas |
| `tests` | Automated tests |
## Running locally

Clone the repository and create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run the application:
```bash
uvicorn app.api.api:app --reload
```

## Documentation

More detailed architecture and design information:
- [Project documentation](docs/project.md)