# python
"""
backend/update_password.py

Use the variables below to set a demo user id and plain password instead of using sys.argv.
"""

import subprocess
import sys
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import DictCursor
import os

load_dotenv()  # optional: loads POSTGRES_URL from a .env file

# --- Edit these variables for a demo run ---
USER_ID = 6
PLAIN_PASSWORD = "shubh123"
HASH_SCRIPT = "hash_password.py"
# --------------------------

def get_hashed_password(plain: str) -> str:
    proc = subprocess.run([sys.executable, HASH_SCRIPT, plain], capture_output=True, text=True, check=True)
    return proc.stdout.strip()

def update_password_in_db(user_id: int, hashed: str):
    url = os.environ.get('POSTGRES_URL')
    if not url:
        raise RuntimeError("POSTGRES_URL not set in environment (set it or export a full connection URL)")
    conn = psycopg2.connect(url, cursor_factory=DictCursor)
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE employee SET password = %s WHERE id = %s;", (hashed, user_id))
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        hashed = get_hashed_password(PLAIN_PASSWORD)
        print("Generated hash:", hashed)
        update_password_in_db(USER_ID, hashed)
        print(f"Updated password for id={USER_ID}")
    except subprocess.CalledProcessError as e:
        print("Error generating hash:", e.stderr or e)
        sys.exit(2)
    except Exception as e:
        print("DB update error:", e)
        sys.exit(3)
