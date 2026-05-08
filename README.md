# Dawn Of the Explorers

An exploratory-themed idle RPG where players manage a party of heroes, assign jobs, equip characters, and progress passively as the adventure unfolds.

## Tech stack

- **Frontend**: React 19 + Vite + Tailwind CSS
- **Backend**: Flask + JWT + Flask-Migrate (Alembic)
- **Database**: PostgreSQL
- **Infrastructure**: Docker + Docker Compose

## Quick start

The only prerequisite is having [Docker](https://docs.docker.com/get-docker/) installed.

```bash
docker compose up --build
```

Then seed the database (first time only):

```bash
docker compose exec backend python seed_db.py
```

> Schema migrations run automatically on every startup via Flask-Migrate.

| Service  | URL                   |
| -------- | --------------------- |
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:5000 |

**Test account:** `eduladron` / `12345678`

## Development

Hot-reload is enabled for both frontend and backend — edit files locally and changes reflect immediately without restarting the containers.

```bash
docker compose up          # start
docker compose down        # stop
docker compose down -v     # stop and wipe the database volume
```

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

## Tests

Unit tests cover the backend service layer. No database required.

```bash
cd backend
source venv/bin/activate
python -m pytest tests/unit/ -v
```

**Tools:** `pytest` + `pytest-mock`

## Manual setup (without Docker)

<details>
<summary>Backend</summary>

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env       # set DATABASE_URL and JWT_SECRET_KEY
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
