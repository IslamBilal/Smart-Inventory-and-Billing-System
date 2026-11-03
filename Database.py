# PostgreSQL connection configuration
import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

# Load a project-level .env file. Keep the actual .env file out of Git.
load_dotenv(Path(__file__).resolve().parent / ".env")


def connection():
    """Create a PostgreSQL connection from environment variables."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "ecommerce"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
        port=os.getenv("DB_PORT", "5432"),
        connect_timeout=5,
    )


# Existing modules share this connection; a future refactor can use a pool/context manager.
conn = connection()
