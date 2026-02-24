An **exploratory-themed IDLE RPG** where players manage a party of heroes, equip characters, and progress passively as the adventure unfolds. The goal is a lightweight, persistent experience that blends idle progression with party and equipment customization.

## Core technologies

- **Frontend**: React + Vite.
- **Backend**: Flask (REST API) with JWT.
- **Database**: PostgreSQL.

## Prerequisites

Make sure you have installed:

- **Node.js** (recommended 18+).
- **Python** (recommended 3.10+).
- **PostgreSQL** (recommended 14+).

## Dependency installation

### 1) Backend (Flask)

1. Enter the backend directory:

   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   # On Windows (PowerShell):
   # .\venv\bin\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install flask flask-cors flask-jwt-extended flask-sqlalchemy psycopg2-binary python-dotenv
   ```

### 2) Frontend (React + Vite)

1. Enter the frontend directory:

   ```bash
   cd frontend-react
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Environment variables (`.env`)

The backend can load local variables from `backend/.env` (using `python-dotenv`).

1. Copy the example file:

   ```bash
   cp backend/.env.example backend/.env
   ```

2. Adjust at least these values:
   - `DATABASE_URL`: PostgreSQL connection string.
   - `JWT_SECRET_KEY`: secret key for signing tokens.
   - `FLASK_DEBUG`: `True`/`False` for debug mode.

## Database configuration (PostgreSQL)

The backend uses the configuration defined in `backend/config.py`:

```python
SQLALCHEMY_DATABASE_URI = "postgresql://eduladron:12341234@localhost:5432/vtt_db"
```

Options:

- **Use the default configuration** by creating the user and database:

  ```bash
  psql -U postgres
  ```

  ```sql
  CREATE USER eduladron WITH PASSWORD '12341234';
  CREATE DATABASE vtt_db OWNER eduladron;
  GRANT ALL PRIVILEGES ON DATABASE vtt_db TO eduladron;
  ```

- **Change credentials**: edit `backend/config.py` with your connection details.

## Initialize and seed the database

With the virtual environment active and from `backend/`:

- Create tables:

  ```bash
  python init_db.py
  ```

- Seed initial data (drops and recreates tables):
  ```bash
  python seed_db.py
  ```

## Running the project

### 1) Backend

From `backend/` with the virtual environment active:

```bash
flask run
```

The server will start at `http://127.0.0.1:5000` by default.

### 2) Frontend

From `frontend-react/`:

```bash
npm run dev
```

Vite will show the local URL (for example `http://localhost:5173`).

## Recommended workflow

1. Start PostgreSQL.
2. Configure the connection string in `backend/config.py`.
3. Create and/or seed the database with `init_db.py` or `seed_db.py`.
4. Start the backend (`flask run`).
5. Start the frontend (`npm run dev`).

## Notes

- If you change the backend port, make sure the frontend points to the new endpoint.
- For a clean environment, avoid committing `venv/` or `node_modules/` folders.
