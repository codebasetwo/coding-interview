# Interview Assistant — Coding Challenge Generator

Help beginners and experienced engineers practice for coding interviews. This repository contains a FastAPI backend, a React frontend (Vite), and Celery tasks for background jobs (email notifications).

The app generates coding challenges, tracks a daily quota per user, and stores a user's challenge history so they can review past attempts and explanations.

## Key features
- Generate AI-assisted coding challenges (multiple choice + explanation)
- Per-user daily quota with automatic reset
- User authentication (signup, signin, token-based)
- History of generated challenges
- Email verification and password reset via background Celery tasks

## Repository layout

- `backend/` — FastAPI backend (source in `backend/src/`)
- `frontend/coding-interview/` — React + Vite frontend
- `Makefile` — development helpers to start backend, frontend and Celery worker
- `pyproject.toml` — backend Python project configuration

## Prerequisites

- Python 3.11+
- Node.js 16+ and npm (for the frontend)
- Redis (for Celery broker and result backend)
- PostgreSQL (or the database configured in `DATABASE_URL`)

You'll also want a `.env` file at the repository root (or set environment variables in your environment) with the settings used by the backend (see "Environment variables" below).

## Quick start — Development

The Makefile includes convenient targets to run the backend, frontend and Celery worker concurrently. From the repository root, run:

```bash
# start backend dev server, celery worker and frontend dev server together
make dev
```

Notes:
- `make dev` sets `PYTHONPATH=.` so `backend/src` packages import properly.
- If you prefer to run services separately, use the Makefile targets:

```bash
# start only the backend dev server (FastAPI CLI)
make run-server

# start only the celery worker (foreground)
make run-celery

# start the frontend dev server (Vite)
make run-frontend
```

Open the frontend in your browser (Vite will print the dev URL, commonly `http://localhost:5173`) and the API runs at `http://localhost:8000` (FastAPI dev server).

## Production deployment (suggested)

The repo doesn't include a production-ready deploy script, but the recommended approach is:

1. Build the frontend:

```bash
cd frontend/coding-interview

# serve the `dist` directory with your preferred static web server (nginx, Caddy, etc.)
```

2. Run the backend with a fastapi production or dev(if you want to add changes.):

```bash
# Example using uvicorn directly
PYTHONPATH=. fastapi dev backend/src/
```

3. Start Celery workers in the production environment (ensure Redis URL is configured):

```bash
PYTHONPATH=. celery -A backend.src.celery_tasks.celery_app worker --loglevel=info
```

4. Use a process manager (systemd, supervisor, docker-compose, Kubernetes) to keep services running.

## Environment variables

Create a `.env` file at the project root or export these vars in your environment. The backend reads settings via `pydantic-settings` (see `backend/src/config.py`). Typical variables include:

```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
API_PREFIX=/api/v1
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
JWT_SECRETE=your_jwt_secret
JWT_ALGORITHM=HS256
MAIL_USERNAME=...
MAIL_PASSWORD=...
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_FROM=you@example.com
MAIL_FROM_NAME="Interview Assistant"
OPENAI_API_KEY=sk-...
```

Adjust names and values to your environment. Do not commit secrets to source control.

## Running locally (step-by-step)

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install backend dependencies. This project uses `pyproject.toml` (Hatch). If you prefer pip, you can create a `requirements.txt` or use pip to install directly from the project; otherwise install with pip from the project env:

```bash
# Example using uv (using pyproject.toml file)
uv sync

```

3. Install frontend dependencies:

```bash
cd frontend/coding-interview
npm install
```

4. Start development servers with `make dev` (recommended) or the individual `make` targets above.

## API (high level)

- `POST /api/v1/auth/signup` — create account
- `POST /api/v1/auth/signin` — login (returns tokens)
- `POST /api/v1/challenges/generate-challenge` — generate a challenge (authenticated)
- `GET /api/v1/challenges/quota` — get current user's quota
- `GET /api/v1/challenges/my-history` — user challenge history

Refer to the backend route definitions in `backend/src` for exact request/response shapes and additional endpoints.

## Troubleshooting

- "Module 'logging' has no attribute 'config'" when starting Celery: ensure you don't have a local module named `logging.py` shadowing the stdlib and that you start Celery with `PYTHONPATH=.` so imports are resolved correctly (the Makefile sets this).
- If the frontend fails to call API: check CORS and that the frontend dev server origin is allowed by the backend.
- If you see authentication errors, verify tokens are stored in `localStorage` (frontend) and `JWT_SECRETE` and other auth env vars are set.

## Development notes

- Database migrations: this repo can be wired to Alembic for migrations. If you don't have migrations configured, creating tables via SQLModel's `create_all` is an option for local development.
- Background tasks: Celery is used to send email (verify/reset). Make sure Redis is running and `REDIS_URL` is set.

## Contributing

Contributions are welcome. Please open issues or pull requests for bugs or improvements. Follow standard Git workflow (feature branch, tests, PR).

## License

This project is provided as-is. Add a license file (e.g., `LICENSE`) if you want to specify terms.
