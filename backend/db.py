# python
# File: `backend/db.py`
# Ensures the connection string includes sslmode=require and connects with DictCursor.

import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import psycopg2
from psycopg2.extras import DictCursor

load_dotenv()

def get_db_connection():
    url = os.environ.get('POSTGRES_URL')
    if not url:
        raise RuntimeError("POSTGRES_URL not set in environment")

    # Ensure SSL is required for Supabase / pooled endpoints
    if 'sslmode=' not in url:
        if '?' in url:
            url = url + '&sslmode=require'
        else:
            url = url + '?sslmode=require'

    conn = psycopg2.connect(url, cursor_factory=DictCursor)
    return conn
