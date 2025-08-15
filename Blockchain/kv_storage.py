import sqlite3
from typing import Optional, List


class KVSQLiteStore:
    """A lightweight SQLite-backed key-value store with optional atomic writes."""

    def __init__(self, path: str):
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._active_txn = False
        self._conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS kv_data (
                key TEXT PRIMARY KEY,
                value TEXT
            )
            '''
        )
        self._conn.commit()

    def set(self, key: str, value: str) -> None:
        """Insert or update a value for the given key."""
        with self._conn:
            self._conn.execute(
                '''
                INSERT INTO kv_data (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value = excluded.value
                ''',
                (key, value)
            )

    def get(self, key: str) -> Optional[str]:
        """Retrieve a value by key."""
        cur = self._conn.execute(
            'SELECT value FROM kv_data WHERE key = ?',
            (key,)
        )
        row = cur.fetchone()
        return row[0] if row else None

    def remove(self, key: str) -> None:
        """Delete an entry by key."""
        with self._conn:
            self._conn.execute('DELETE FROM kv_data WHERE key = ?', (key,))

    def has_key(self, key: str) -> bool:
        """Check if a key exists."""
        cur = self._conn.execute('SELECT 1 FROM kv_data WHERE key = ?', (key,))
        return cur.fetchone() is not None

    def all_keys(self) -> List[str]:
        """Return a list of all keys in the store."""
        cur = self._conn.execute('SELECT key FROM kv_data')
        return [row[0] for row in cur.fetchall()]

    def begin_atomic(self) -> None:
        """Start an atomic write transaction."""
        if not self._active_txn:
            self._conn.execute('BEGIN')
            self._active_txn = True

    def atomic_set(self, key: str, value: str) -> None:
        """Set a value within an active atomic transaction."""
        if not self._active_txn:
            self.begin_atomic()
        self._conn.execute(
            '''
            INSERT INTO kv_data (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            ''',
            (key, value)
        )

    def commit_atomic(self) -> bool:
        """Commit the current atomic transaction."""
        if not self._active_txn:
            return True
        try:
            self._conn.commit()
            return True
        except sqlite3.Error:
            self._conn.rollback()
            return False
        finally:
            self._active_txn = False

    def close(self) -> None:
        """Close the database connection."""
        if self._active_txn:
            self._conn.rollback()
        self._conn.close()
