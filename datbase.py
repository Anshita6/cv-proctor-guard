# database.py
import sqlite3
import time

def initialize_db():
    """Creates a local SQLite database and table if it doesn't exist yet."""
    conn = sqlite3.connect("exam_logs.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS violations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            violation_type TEXT,
            integrity_score REAL
        )
    ''')
    conn.commit()
    conn.close()

def log_violation(violation_type, integrity_score):
    """Logs a timestamped cheating incident into the local database."""
    conn = sqlite3.connect("exam_logs.db")
    cursor = conn.cursor()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO violations (timestamp, violation_type, integrity_score)
        VALUES (?, ?, ?)
    ''', (timestamp, violation_type, integrity_score))
    conn.commit()
    conn.close()
    print(f"[DATABASE LOG] Recorded entry: {violation_type} at {timestamp}")

# Run initialization when the script is imported
initialize_db()