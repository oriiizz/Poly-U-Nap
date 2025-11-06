# state.py - Reflex State class with simple SQLite persistence (switchable to Postgres)
import os
import sqlite3
from datetime import datetime
import reflex as rx
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv('DATABASE_URL') or os.path.join(os.getcwd(), 'poly_unap.db')

def get_conn():
    # If DATABASE_URL is set and starts with 'postgres', you can adapt this helper
    # to use psycopg2 or SQLAlchemy. For local use, we default to sqlite.
    if DB_PATH.startswith('postgres'):
        # Placeholder: in production you'd use psycopg2 or SQLAlchemy.
        raise RuntimeError('Postgres URL detected - please adapt connection code for hosted DB.')
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            rating INTEGER,
            hours REAL,
            quality INTEGER,
            comment TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class AppState(rx.State):
    # UI state
    location: str = ''
    rating: int = 3
    hours: float = 7.0
    quality: int = 3
    comment: str = ''
    dark_mode: bool = False

    # Dashboard cache (kept in memory for fast updates)
    cached_stats: Dict[str, Any] = {}

    def toggle_dark(self):
        self.dark_mode = not self.dark_mode

    # Example score formula: hours * 10 + quality * 2 + rating * 3
    @staticmethod
    def compute_score(hours: float, quality: int, rating: int) -> float:
        return round(hours * 10 + quality * 2 + rating * 3, 2)

    def submit_review(self):
        conn = get_conn()
        c = conn.cursor()
        c.execute('INSERT INTO reviews (location, rating, hours, quality, comment, created_at) VALUES (?,?,?,?,?,?)',
                  (self.location, int(self.rating), float(self.hours), int(self.quality), self.comment, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
        # reset form fields (optional)
        self.location = ''
        self.rating = 3
        self.hours = 7.0
        self.quality = 3
        self.comment = ''
        # update stats cache
        self.update_stats()

    def get_reviews(self, limit: int = 100):
        conn = get_conn()
        c = conn.cursor()
        c.execute('SELECT * FROM reviews ORDER BY created_at DESC LIMIT ?', (limit,))
        rows = c.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def update_stats(self):
        reviews = self.get_reviews(1000)
        if not reviews:
            self.cached_stats = {'count': 0, 'avg_hours': 0, 'avg_quality': 0, 'avg_rating': 0}
            return
        count = len(reviews)
        avg_hours = sum(r['hours'] for r in reviews) / count
        avg_quality = sum(r['quality'] for r in reviews) / count
        avg_rating = sum(r['rating'] for r in reviews) / count
        self.cached_stats = {
            'count': count,
            'avg_hours': round(avg_hours,2),
            'avg_quality': round(avg_quality,2),
            'avg_rating': round(avg_rating,2),
        }

    def on_mount(self):
        # called when the page mounts in Reflex
        self.update_stats()

