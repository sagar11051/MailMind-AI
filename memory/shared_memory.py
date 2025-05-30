import sqlite3
from typing import Any, Dict

class SharedMemory:
    def __init__(self, db_path: str = ':memory:'):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS context (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE,
                value TEXT
            )
        ''')
        self.conn.commit()

    def set(self, key: str, value: str):
        self.conn.execute('REPLACE INTO context (key, value) VALUES (?, ?)', (key, value))
        self.conn.commit()

    def get(self, key: str) -> Any:
        cursor = self.conn.execute('SELECT value FROM context WHERE key = ?', (key,))
        row = cursor.fetchone()
        return row[0] if row else None 