# Virtual RPG Table Top — Current Status

A small web project split into a Flask + SQLAlchemy backend and a React + Vite frontend. The app aims to provide a simple virtual tabletop system with users, characters and equippable items.

## Quick overview

- Backend: REST API with JWT auth and models for users, characters, equipment types, equipment and character-equipment assignments. See [`create_app`](backend/app/__init__.py) ([backend/app/**init**.py](backend/app/__init__.py)) and configuration in [backend/config.py](backend/config.py).
- Frontend: React SPA (Vite) using `react-router` and UI primitives from `@radix-ui/themes`. Authentication helpers live in [`useAuth`](frontend-react/src/hooks/useAuth.js) ([frontend-react/src/hooks/useAuth.js](frontend-react/src/hooks/useAuth.js)) and routing is defined in [frontend-react/src/routes/AppRouter.jsx](frontend-react/src/routes/AppRouter.jsx).

## Project structure (important files)

- Backend
  - [backend/run.py](backend/run.py) — start app (creates tables if needed)
  - [backend/init_db.py](backend/init_db.py) — create database tables
  - [backend/seed_db.py](backend/seed_db.py) — simple seed data
  - Auth routes: [backend/app/routes/auth.py](backend/app/routes/auth.py) (`auth_bp`)
  - App factory: [`create_app`](backend/app/__init__.py) — [backend/app/**init**.py](backend/app/__init__.py)
  - Config: [backend/config.py](backend/config.py)
  - DB extension: [backend/app/extensions.py](backend/app/extensions.py)
  - Models:
    - [`User`](backend/app/models/user.py) — [backend/app/models/user.py](backend/app/models/user.py)
    - [`Character`](backend/app/models/character.py) — [backend/app/models/character.py](backend/app/models/character.py)
    - [`EquipmentType`](backend/app/models/equipment_type.py) — [backend/app/models/equipment_type.py](backend/app/models/equipment_type.py)
    - [`Equipment`](backend/app/models/equipment.py) — [backend/app/models/equipment.py](backend/app/models/equipment.py)
    - [`CharacterEquipment`](backend/app/models/character_equipment.py) — [backend/app/models/character_equipment.py](backend/app/models/character_equipment.py)
  - DB schema diagrams: [backend/db/schema.dbml](backend/db/schema.dbml) and [backend/db/schema.dbdiagram](backend/db/schema.dbdiagram)
  - Requirements: [backend/requirements.txt](backend/requirements.txt)

- Frontend
  - Entrypoint: [frontend-react/src/main.jsx](frontend-react/src/main.jsx)
  - Router: [frontend-react/src/routes/AppRouter.jsx](frontend-react/src/routes/AppRouter.jsx)
  - Auth hook: [`useAuth`](frontend-react/src/hooks/useAuth.js) — [frontend-react/src/hooks/useAuth.js](frontend-react/src/hooks/useAuth.js)
  - Login modal: [frontend-react/src/components/modals/LogRegModal.jsx](frontend-react/src/components/modals/LogRegModal.jsx)
  - Protected route: [frontend-react/src/components/ProtectedRoute.jsx](frontend-react/src/components/ProtectedRoute.jsx)
  - Layouts: [frontend-react/src/components/MainLayout.jsx](frontend-react/src/components/MainLayout.jsx), [frontend-react/src/components/LoginLayout.jsx](frontend-react/src/components/LoginLayout.jsx)
  - Pages: [frontend-react/src/pages/Home.jsx](frontend-react/src/pages/Home.jsx), [frontend-react/src/pages/Login.jsx](frontend-react/src/pages/Login.jsx)
  - Vite config: [frontend-react/vite.config.js](frontend-react/vite.config.js)
  - Package: [frontend-react/package.json](frontend-react/package.json)

## How to run (local)

1. Backend
   - Create and activate a virtual environment.
   - Install dependencies:
     ```
     pip install -r [requirements.txt](http://_vscodecontentref_/0)
     ```
   - Create tables:
     ```
     python [init_db.py](http://_vscodecontentref_/1)
     ```
     or start the app (will also create tables):
     ```
     python [run.py](http://_vscodecontentref_/2)
     ```
   - (Optional) Seed example data:
     ```
     python [seed_db.py](http://_vscodecontentref_/3)
     ```
   - Important endpoints:
     - POST /register — implemented in [backend/app/routes/auth.py](backend/app/routes/auth.py)
     - POST /login — implemented in [backend/app/routes/auth.py](backend/app/routes/auth.py)

2. Frontend
   - Install and run:
     ```
     cd frontend-react
     npm install
     npm run dev
     ```
   - The frontend expects the API at http://localhost:5000 and uses [`useAuth`](frontend-react/src/hooks/useAuth.js) for register/login.

## Notes & implementation details

- JWT secret is set in [`create_app`](backend/app/__init__.py) ([backend/app/**init**.py](backend/app/__init__.py)) as `JWT_SECRET_KEY`.
- Schema follows [backend/db/schema.dbml](backend/db/schema.dbml). Uniqueness for equipment per character type is enforced by the unique constraint in [`CharacterEquipment`](backend/app/models/character_equipment.py) ([backend/app/models/character_equipment.py](backend/app/models/character_equipment.py)).
- Frontend stores the JWT access token in localStorage and guards routes with [frontend-react/src/components/ProtectedRoute.jsx](frontend-react/src/components/ProtectedRoute.jsx).
- The auth flow: [`useAuth`](frontend-react/src/hooks/useAuth.js) calls backend endpoints and [frontend-react/src/components/modals/LogRegModal.jsx](frontend-react/src/components/modals/LogRegModal.jsx) uses that hook.

## Known issues / small inconsistencies

- Some table and model names differ slightly from DBML (e.g., pluralization of table names). Verify table names in models vs schema if migrations are added.
- The frontend currently relies on localStorage for the token and has no refresh-token flow.

## Next steps

- Implement CRUD endpoints for characters, equipment and assignments.
- Add validation and better error propagation (frontend should show API messages).
- Add unit and integration tests for backend and frontend components.

---

For implementation details check the files listed above (examples: [`create_app`](backend/app/__init__.py), [`useAuth`](frontend-react/src/hooks/useAuth.js)).
