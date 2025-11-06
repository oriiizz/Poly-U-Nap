# Poly U Nap — Reflex project scaffold

This is a Reflex (Python-first web framework) scaffold for your **Sleep Rating System** exported from Figma.
The goal: a ~95% Python app (UI + logic) using Reflex with local persistence (SQLite) by default,
easy to switch to a hosted PostgreSQL database for production.

## What's included
- `main.py` — Reflex app & page registration
- `state.py` — Reflex `State` class: holds values, methods to add/get reviews, compute scores, toggle dark mode
- `ui.py` — Page UI components (form + dashboard)
- `requirements.txt` — Python dependencies
- `README_DEPLOY.md` — Deployment + hosting guidance (Render/Railway/GCP/Heroku)
- `.env.example` — example environment variables

## Quick start (local)
1. Create a Python venv and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS / Linux
   venv\Scripts\activate   # Windows PowerShell
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run Reflex dev server:
   ```bash
   python main.py
   ```
   Open http://localhost:3000 (Reflex defaults to 3000).

## Notes on database
- By default the app uses SQLite file `poly_unap.db` inside the project directory.
- To use a hosted DB (Postgres), set `DATABASE_URL` in environment (see README_DEPLOY.md).
- The `state.py` contains helper functions to switch between SQLite and Postgres easily.

## Next steps I can do for you if you'd like:
- Convert more of your Figma styling into Reflex/Tailwind utility classes.
- Add authentication + per-user saved reviews.
- Set up a live deploy (Render) and connect a managed Postgres DB.
- Improve charts (use recharts/plotly/chart.js integration).

