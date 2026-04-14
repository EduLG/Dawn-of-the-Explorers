# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Virtual RPG Table Top is a full-stack idle RPG web application. Players manage a party of heroes, assign jobs, and equip characters — the game progresses passively. The backend exposes a REST API consumed by a React SPA.

## Development Commands

### Docker (recomendado)

```bash
docker compose up --build        # Arranca los 3 servicios (db, backend, frontend)
docker compose up -d             # En segundo plano
docker compose down              # Para y elimina contenedores
docker compose down -v           # También elimina el volumen de PostgreSQL

# Inicializar / seedear la BD (primera vez o tras docker compose down -v)
docker compose exec backend python init_db.py
docker compose exec backend python seed_db.py
```

URLs: frontend → http://localhost:5173 · backend → http://localhost:5000

### Backend (Flask + PostgreSQL)

```bash
cd backend
source venv/bin/activate        # Activate Python virtual environment
flask run                        # Start API server at http://127.0.0.1:5000
python init_db.py                # Create database tables (run once on setup)
python seed_db.py                # Drop and recreate tables with sample data
```

**First-time setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install flask flask-cors flask-jwt-extended flask-sqlalchemy psycopg2-binary python-dotenv
cp .env.example .env             # Fill in DATABASE_URL and JWT_SECRET_KEY
python init_db.py
python seed_db.py
```

### Frontend (React + Vite)

```bash
cd frontend-react
npm install                      # Install dependencies
npm run dev                      # Dev server at http://localhost:5173
npm run build                    # Production build
npm run lint                     # ESLint
npm run preview                  # Preview production build
```

## Architecture

### Backend Layers

```
Routes (Blueprint) → Handlers → Services → Repositories → Models → PostgreSQL
```

- **routes/**: Flask Blueprints, registered under `/api/v1/auth` and `/api/v1/users`
- **handlers/**: Parse requests, call services, format HTTP responses
- **services/**: Business logic — JWT generation, password hashing, rating calculation
- **repositories/**: Database query abstraction over SQLAlchemy
- **models/**: ORM definitions — `User`, `Party`, `Character`, `Job`, `Equipment`, `CharacterEquipment`

Errors propagate via `ServiceError` exceptions with explicit HTTP status codes; all error responses use `{ "error": "message" }`.

### Frontend Layers

```
AppRouter → Pages → Components → Hooks → fetch() → localStorage (JWT)
```

- **routes/AppRouter.jsx**: React Router config; wraps private routes in `ProtectedRoute`
- **pages/**: `Home` (party dashboard) and `Login` (entry point)
- **hooks/useAuth.js**: Login/register logic, token storage
- **hooks/useUser.js**: Fetches `/api/v1/users/me`; uses `AbortController` for cleanup
- **utils/jwt.js**: Decodes JWT payload from `localStorage` key `token`

Backend URL is hardcoded as `http://localhost:5000` in hooks — no frontend `.env` file.

### Data Model

**Rating system:** `CharacterEquipment` → sum of `Equipment.rating` = `Character.rating`; sum of all characters = `Party.rating`.

**Equipment slots:** `head`, `chest`, `primary_hand`, `secondary_hand`, `accessory` — unique per character via DB constraint.

**User → Party (1:1), Party → Characters (1:N), Character ↔ Equipment (M:N via CharacterEquipment)**

## Environment

Backend reads from `backend/.env`:

```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<db_name>
JWT_SECRET_KEY=<secret>
FLASK_DEBUG=True
```

JWT tokens expire after 24 hours (`JWT_ACCESS_TOKEN_EXPIRES`).

## Seed / Test Data

After running `python seed_db.py`:
- User: `eduladron` / `12345678`
- Party: "Heroes Party" with 4 characters (Firion, Sabin, Balthier, Locke)
- 10 job classes, 20 equipment items pre-assigned
