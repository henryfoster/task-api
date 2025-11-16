#!/usr/bin/env python3
import sys
from sqlalchemy import create_engine, text
import os

def main():
    try:
        engine = create_engine(os.getenv("DATABASE_URL"))
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("database connection successful")
        sys.exit(0)
    except Exception as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
