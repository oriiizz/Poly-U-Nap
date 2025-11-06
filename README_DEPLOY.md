# Deployment & Hosting Guide (short)

## Option A — Render (recommended for simplicity)
1. Create a Render account.
2. Create a new Web Service and connect your GitHub repo.
3. Set build/start commands in Render:
   - Build command: `pip install -r requirements.txt`
   - Start command: `python main.py`
4. Add a managed Postgres on Render and set the `DATABASE_URL` env var in the service settings.
5. Deploy — your app will be public with HTTPS.

## Option B — Railway / Heroku
- Similar flow: push to GitHub, connect, set `DATABASE_URL` (Postgres add-on), configure start command.

## Environment variables
- `DATABASE_URL` — If empty, app uses local SQLite file `poly_unap.db`.
- `SECRET_KEY` — (optional) for session features if added.

