"""
Database Schema & Seed Initialization Script for Polymer Material Selection System.
Usage:
    python init_db.py
or via Flask CLI:
    flask init-db
"""
import sys
from app import app, db
from database import seed_database


def main():
    print("Verifying database connection and schema...")
    with app.app_context():
        try:
            db.create_all()
            inserted, total = seed_database()
            print(f"Success: Database schema ready. Seeded {inserted} new materials. Total available: {total}.")
        except Exception as e:
            print(f"Database initialization failed: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
