# Dawn Of the Explorers

An exploratory-themed idle RPG where players manage a party of heroes, assign jobs, equip characters, and progress passively as the adventure unfolds.

## Tech stack

- **Frontend**: React 19 + Vite + Tailwind CSS
- **Backend**: Flask + JWT
- **Database**: PostgreSQL
- **Infrastructure**: Docker + Docker Compose

## Quick start

The only prerequisite is having [Docker](https://docs.docker.com/get-docker/) installed.

```bash
docker compose up --build
```

Then initialize the database (first time only):

```bash
docker compose exec backend python init_db.py
docker compose exec backend python seed_db.py
```

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

## Tests

Unit tests cover the backend service layer (32 tests). No database required.

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
python init_db.py
python seed_db.py
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
