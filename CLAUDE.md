# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Virtual RPG Table Top ("Dawn of the Explorers") is a full-stack idle RPG web application. Players manage a party of heroes, assign jobs, equip characters and send the party to explore dungeons — the game progresses passively. The backend exposes a REST API consumed by a React SPA.

Production: frontend on Vercel (https://dawn-of-the-explorers.vercel.app), backend on Railway. An Android app that wraps the same frontend is planned — see `docs/android-plan.md`.

## Working Rules

- **Git operations are done only by the user:** creating branches, commits, merges, pushes, pull requests and tags. Do not run any of them. Leave changes uncommitted in the working tree, explain what changed, and suggest when it is a good moment for each operation. Read-only git commands (`status`, `log`, `diff`) are fine.
- **Deployments and production variables (Railway, Vercel) are changed only by the user.** Say when a change is needed and what to set.
- Explain each step before doing it and wait for confirmation.

## Development Commands

### Docker (recomendado)

```bash
docker compose up --build        # Arranca los 3 servicios (db, backend, frontend)
docker compose up -d             # En segundo plano
docker compose down              # Para y elimina contenedores
docker compose down -v           # También elimina el volumen de PostgreSQL

# Seedear la BD (primera vez o tras docker compose down -v)
docker compose exec backend python seed_db.py
```

Las migraciones (Flask-Migrate) se aplican solas en cada arranque del backend (`run.py`).

URLs: frontend → http://localhost:5173 · backend → http://localhost:5000

### Backend (Flask + PostgreSQL)

```bash
cd backend
source venv/bin/activate        # Activate Python virtual environment
flask run                        # Start API server at http://127.0.0.1:5000
flask db upgrade                 # Apply schema migrations
python seed_db.py                # Drop and recreate tables with sample data
pytest                           # Unit tests (backend/tests/unit)
```

**First-time setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env             # Fill in DATABASE_URL and JWT_SECRET_KEY
flask db upgrade
python seed_db.py
```

`backend/venv/` and `backend/.env` are local only — never commit them.

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

- **routes/**: Flask Blueprints, all registered under `/api/v1/` in `app/__init__.py`:
  - `auth` — `POST /register`, `/login`, `/refresh`, `/demo`
  - `users` — `GET /me`
  - `party` — `POST /setup` (onboarding)
  - `jobs` — `GET`
  - `equipment` — `GET` (by armor type)
  - `inventory` — `GET`, `POST /<id>/equip`, `DELETE /<id>`
  - `dungeons` — `GET`, `GET /exploration/status`, `POST /<id>/explore`
  - `health` — `GET`
  - `characters` — blueprint registered, no routes yet
- **handlers/**: Parse requests, call services, format HTTP responses
- **services/**: Business logic — JWT generation, password hashing, rating calculation, exploration and loot resolution
- **repositories/**: Database query abstraction over SQLAlchemy
- **schemas/**: Marshmallow serialization schemas
- **models/**: ORM definitions — `User`, `Party`, `Character`, `Job`, `Equipment`, `PartyInventory`, `CharacterEquipment`, `Dungeon`, `Exploration`
- **demo/**: In-memory demo mode — `DemoStore` keeps an isolated copy of seed data per demo session and `demo_services.py` mirrors the real services with no DB writes. Handlers branch on `g.is_demo`, set from the JWT claims in `app/__init__.py`.

Errors propagate via `ServiceError` exceptions with explicit HTTP status codes; all error responses use `{ "error": "message" }`.

CORS allows a single origin, read from `FRONTEND_URL`.

### Frontend Layers

```
AppRouter → Pages → Views → Components → Hooks → apiFetch() → localStorage (JWT)
```

- **routes/AppRouter.jsx**: React Router config; wraps private routes in `ProtectedRoute`. Routes: `/login` and `/home/{team,equipment,quests,market,inventory}`
- **pages/**: `Home` (shell: header, navigation, logout, onboarding) and `Login` (login, register, demo)
- **views/**: `TeamView`, `EquipmentView`, `InventoryView`, `QuestsView`, `MarketView` — rendered inside `Home`
- **hooks/**: `useAuth` (login/register/demo, token storage), `useUser` (`/api/v1/users/me`), `useJobs`, `useEquipment`, `useUpdateEquipment`, `useInventory`, `useDungeons`
- **utils/apiFetch.js**: fetch wrapper — adds the `Authorization` header, refreshes the access token on 401 and redirects to `/login` when the refresh fails
- **utils/jwt.js**: Decodes the JWT payload, detects demo tokens

Tokens live in `localStorage` under the keys `token` and `refresh_token`.

The backend base URL comes from `VITE_API_URL` (empty by default). In development the Vite dev server proxies `/api` to the backend container (`vite.config.js`).

### Data Model

**Rating system:** `CharacterEquipment` → sum of `Equipment.rating` = `Character.rating`; sum of all characters = `Party.rating`. Party rating gates dungeon visibility and loot.

**Equipment slots:** `head`, `chest`, `primary_hand`, `secondary_hand`, `accesory` (spelled with one `s` throughout the code) — unique per character via DB constraint.

**Armor type:** a character can only equip items whose `equipment_type` (`plate`, `leather`, `cloth`) matches their job.

**User → Party (1:1), Party → Characters (1:N), Party → PartyInventory (1:N, items the party owns), Character ↔ PartyInventory via CharacterEquipment (what is equipped), Party → Exploration (1:N, one dungeon run each)**

## Environment

Backend reads from `backend/.env`:

```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<db_name>
JWT_SECRET_KEY=<secret>
FLASK_DEBUG=True
FRONTEND_URL=<allowed CORS origin, default http://localhost:5173>
```

Access tokens expire after 15 minutes and refresh tokens after 30 days (`backend/config.py`).

## Seed / Test Data

After running `python seed_db.py`:
- Users: `eduladron` / `12345678` and `eduladron2` / `12345678`
- Party: "Heroes Party" with 4 characters (Firion, Sabin, Balthier, Locke)
- 10 job classes, the full equipment catalogue and 11 dungeons

Demo mode (`POST /api/v1/auth/demo`, "Try Demo" on the login page) needs no account and saves nothing.
