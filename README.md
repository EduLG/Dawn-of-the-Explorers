# Dawn Of the Explorers

An exploratory-themed idle RPG where players manage a party of heroes, assign jobs, equip characters, and progress passively as the adventure unfolds.

[![React](https://img.shields.io/badge/React_19-61DAFB?style=flat&logo=react&logoColor=black)](#tech-stack)
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](#tech-stack)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL_16-4169E1?style=flat&logo=postgresql&logoColor=white)](#tech-stack)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](#tech-stack)

**[Check it here](https://dawn-of-the-explorers.vercel.app/)** — no account needed, click **Try Demo** on the login page.

## Tech stack

| Layer          | Technology                                           |
| -------------- | ---------------------------------------------------- |
| Frontend       | React 19 + Vite + Tailwind CSS                       |
| Backend        | Flask + Flask-JWT-Extended + Flask-Migrate (Alembic) |
| Database       | PostgreSQL 16                                        |
| Infrastructure | Docker + Docker Compose                              |

---

## Quick start

The only prerequisite is [Docker](https://docs.docker.com/get-docker/).

```bash
docker compose up --build
```

Seed the database (first time only, or after `down -v`):

```bash
docker compose exec backend python seed_db.py
```

> Schema migrations run automatically on every startup via Flask-Migrate.

| Service  | URL                   |
| -------- | --------------------- |
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:5000 |

**Test account:** `eduladron` / `12345678`

**Demo mode:** click **Try Demo** on the login page — no account required, all features available, nothing is saved.

---

## Development

Hot-reload is enabled for both frontend and backend. Edit files locally and changes reflect immediately without restarting containers.

```bash
docker compose up          # start (foreground)
docker compose up -d       # start (background)
docker compose down        # stop
docker compose down -v     # stop and wipe the PostgreSQL volume
```

### Manual setup (without Docker)

<details>
<summary>Backend</summary>

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # fill in DATABASE_URL and JWT_SECRET_KEY
flask db upgrade           # create tables via migrations
python seed_db.py          # load initial data
flask run
```

</details>

<details>
<summary>Frontend</summary>

```bash
cd frontend-react
npm install
npm run dev
```

</details>

---

## Environment variables

Backend reads from `backend/.env` (or Docker environment):

| Variable         | Required | Description                                                          |
| ---------------- | -------- | -------------------------------------------------------------------- |
| `DATABASE_URL`   | yes      | PostgreSQL connection string — `postgresql://user:pass@host:5432/db` |
| `JWT_SECRET_KEY` | yes      | Secret used to sign JWT tokens. Change before deploying to prod      |
| `FLASK_DEBUG`    | no       | Set to `True` to enable debug mode and auto-reload                   |
| `FRONTEND_URL`   | no       | Allowed CORS origin (default: `http://localhost:5173`)               |

Access tokens expire after **15 minutes**. A refresh token, valid for **30 days**, is issued alongside the access token.

---

## Architecture

### Backend

```
Routes (Blueprint) → Handlers → Services → Repositories → Models → PostgreSQL
```

| Layer           | Responsibility                                                   |
| --------------- | ---------------------------------------------------------------- |
| `routes/`       | Flask Blueprints, URL registration                               |
| `handlers/`     | Parse request, call services, format HTTP response               |
| `services/`     | Business logic — validation, rating calculation, loot resolution |
| `repositories/` | Database query abstraction over SQLAlchemy                       |
| `models/`       | ORM table definitions                                            |
| `demo/`         | In-memory demo layer — mirrors the real stack with no DB writes  |

Errors propagate via `ServiceError(message, status_code)`. All error responses use `{ "error": "message" }`.

### Frontend

```
AppRouter → Pages → Views → Hooks → fetch() → localStorage (JWT)
```

| Layer                  | Responsibility                                                |
| ---------------------- | ------------------------------------------------------------- |
| `routes/AppRouter.jsx` | React Router config; wraps private routes in `ProtectedRoute` |
| `pages/Home.jsx`       | Main shell — header, sidebar, navigation, logout              |
| `pages/Login.jsx`      | Entry point — login, register, demo                           |
| `views/`               | Feature views rendered inside the home shell                  |
| `hooks/`               | Data fetching and mutation hooks                              |
| `utils/jwt.js`         | Decode JWT payload, detect demo tokens                        |

---

## Data model

```
User (1) ──── (1) Party (1) ──── (N) Character (N) ──── (N) Equipment
                    │                                  via CharacterEquipment
                    └── (N) PartyInventory ────────────────┘
                              │
                         tracks which items
                         the party owns
```

### Tables

| Model                | Key fields                                                                           |
| -------------------- | ------------------------------------------------------------------------------------ |
| `User`               | `id` (UUID), `username`, `email`, `password` (hashed)                                |
| `Party`              | `id`, `name`, `level`, `experience`, `user_id` FK                                    |
| `Character`          | `id`, `name`, `party_id` FK, `current_job_id` FK                                     |
| `Job`                | `id`, `name`, `icon`                                                                 |
| `Equipment`          | `id`, `name`, `slot`, `rating`, `equipment_type`                                     |
| `PartyInventory`     | `id`, `party_id` FK, `equipment_id` FK — items the party owns                        |
| `CharacterEquipment` | `id`, `character_id` FK, `inventory_id` FK, `slot` — what is currently equipped      |
| `Dungeon`            | `id`, `name`, `rating`, `min_rating`, `visibility_rating`, `duration`, `loot` (JSON) |
| `Exploration`        | `id`, `party_id`, `dungeon_id`, `started_at`, `ends_at`, `status`, `result` (JSON)   |

### Rating system

- `CharacterEquipment` → sum of `Equipment.rating` = `Character.rating`
- Sum of all character ratings = `Party.rating`
- Party rating gates dungeon visibility and determines loot quantity

### Equipment slots

`head` · `chest` · `primary_hand` · `secondary_hand` · `accesory`

Each slot is unique per character (DB `UniqueConstraint`).

### Armor type — job affinity

| Type      | Jobs                                       |
| --------- | ------------------------------------------ |
| `plate`   | warrior, fender                            |
| `leather` | adventurer, gunslinger, thief, beastmaster |
| `cloth`   | engineer, alchemist, sage, scholar         |

A character can only equip items whose `equipment_type` matches their job's armor type.

### Equipment tiers

10 tiers of power per slot (rating 2 → 82). Each tier contains 10 items, one per job class. Dungeons drop loot from a specific tier.

---

## API reference

All endpoints except `/api/v1/auth/*` require `Authorization: Bearer <token>`.

### Auth — `/api/v1/auth`

| Method | Path        | Auth          | Description                                                             |
| ------ | ----------- | ------------- | ----------------------------------------------------------------------- |
| POST   | `/register` | No            | Create account. Body: `{ username, email, password }`                   |
| POST   | `/login`    | No            | Sign in. Body: `{ username, password }`. Returns access + refresh token |
| POST   | `/refresh`  | Refresh token | Issue a new access token                                                |
| POST   | `/demo`     | No            | Start a demo session. Returns a JWT with `is_demo: true`. No DB write   |

**Password requirements:** minimum 8 characters, at least one uppercase letter, at least one lowercase letter.

### User — `/api/v1/users`

| Method | Path  | Description                                                              |
| ------ | ----- | ------------------------------------------------------------------------ |
| GET    | `/me` | Current user profile including party, characters, equipped items, rating |

### Party — `/api/v1/party`

| Method | Path     | Description                                                                                   |
| ------ | -------- | --------------------------------------------------------------------------------------------- |
| POST   | `/setup` | Name the party and create the 4 initial characters. Body: `{ party_name, characters: [...] }` |

### Jobs — `/api/v1/jobs`

| Method | Path | Description             |
| ------ | ---- | ----------------------- |
| GET    |      | List all 10 job classes |

### Equipment — `/api/v1/equipment`

| Method | Path                     | Description                                                              |
| ------ | ------------------------ | ------------------------------------------------------------------------ |
| GET    | `?equipment_type=<type>` | List all equipment of a given armor type (`plate` / `leather` / `cloth`) |

### Inventory — `/api/v1/inventory`

| Method | Path          | Description                                                       |
| ------ | ------------- | ----------------------------------------------------------------- |
| GET    |               | List all items in the party's inventory with equipped status      |
| POST   | `/<id>/equip` | Equip an item on a character. Body: `{ character_id, slot }`      |
| DELETE | `/<id>`       | Remove an item from inventory. Body: `{ force: true }` to unequip |

### Dungeons — `/api/v1/dungeons`

| Method | Path                  | Description                                                                 |
| ------ | --------------------- | --------------------------------------------------------------------------- |
| GET    |                       | List dungeons visible to the current party rating                           |
| POST   | `/<id>/explore`       | Start an exploration run                                                    |
| GET    | `/exploration/status` | Poll active exploration; resolves and grants loot when `ends_at` is reached |

#### Exploration loot resolution

| Party rating / Dungeon rating | Outcome | Items granted |
| ----------------------------- | ------- | ------------- |
| < 0.60                        | Failure | 0             |
| 0.60 – 0.99                   | Success | 1             |
| 1.00 – 1.16                   | Success | 2             |
| 1.17 – 1.33                   | Success | 3             |
| 1.34 – 1.49                   | Success | 4             |
| ≥ 1.50                        | Success | 5             |

---

## Demo mode

Clicking **Try Demo** on the login page starts an isolated in-memory session:

- A JWT is issued with `is_demo: true` and a unique `demo_session_id`
- All API calls with that token are served by `app/demo/demo_services.py`, which reads and writes to an in-memory `DemoStore` — PostgreSQL is never touched
- Each demo session starts with a pre-built party (Firion, Sabin, Balthier, Locke) fully equipped with Tier 1 gear and Tier 2 items in inventory
- Any new feature added to the real stack is automatically available in demo mode — the intercept happens only at the handler layer (`g.is_demo` routes to demo services)
- Sessions are invalidated when the JWT expires (24 h) or the server restarts

---

## Database migrations

Migrations live in `backend/migrations/versions/`. When the schema changes:

```bash
# Generate a new migration from model changes
docker compose exec backend flask db migrate -m "describe the change"

# Apply pending migrations
docker compose exec backend flask db upgrade

# Roll back one migration
docker compose exec backend flask db downgrade
```

Migrations are applied automatically on every deploy — no manual step needed in production.

---

## Tests

Unit tests cover the backend service layer. No database required.

```bash
cd backend
source venv/bin/activate
python -m pytest tests/unit/ -v
```

**Tools:** `pytest` + `pytest-mock`
