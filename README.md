# Bakery POS System

Production-oriented bakery management platform. This repository currently contains **Phase 1: Platform Foundation** only: organization/location tenancy, authentication, RBAC primitives, health checks, and the frontend application shell.

## Stack

- Django and Django REST Framework
- PostgreSQL
- JWT access tokens with rotating, revocable refresh tokens in an HttpOnly cookie
- Next.js, TypeScript, and Tailwind CSS
- Docker Compose

## Run locally with Docker

1. Copy `.env.example` to `.env` and replace the secret/password values.
2. Run `docker compose up --build`.
3. Open `http://localhost:3000`.

The API is available at `http://localhost:8000/api/v1/` and its health endpoint is `http://localhost:8000/api/v1/health/`.

Create an initial administrator:

```bash
docker compose exec backend python manage.py createsuperuser
```

Run checks:

```bash
docker compose exec backend pytest
docker compose exec backend ruff check .
docker compose exec frontend npm run lint
docker compose exec frontend npm test
```

## Local execution without Docker

The backend supports SQLite only for local tests and lightweight development. PostgreSQL is the production and Compose database.

```bash
cd backend
python -m venv .venv
python -m pip install -e ".[dev]"
$env:DATABASE_URL = "sqlite:///db.sqlite3"  # PowerShell
python manage.py migrate
python manage.py runserver
```

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

## Security notes

- Never commit `.env`; `.env.example` contains placeholders only.
- Production requires a strong `DJANGO_SECRET_KEY`, HTTPS, `JWT_COOKIE_SECURE=true`, and explicit host/origin allowlists.
- Access tokens are held in browser memory. Refresh tokens are HttpOnly cookies and are rotated and blacklistable.
- Cookie-backed authentication actions require Django CSRF tokens in addition to SameSite cookie controls.
- Tenant-owned API queries must be scoped through an active organization membership.
- Production deployments should run migrations as a distinct release step before scaling application containers.
