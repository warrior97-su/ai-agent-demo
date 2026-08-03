import sqlite3
from contextlib import contextmanager
from pathlib import Path


class SQLiteMemoryStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        with self._connect() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT,
                    tool_call_id TEXT,
                    tool_calls TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                );
                CREATE INDEX IF NOT EXISTS idx_messages_session
                    ON memories (session_id,id);
                CREATE TABLE IF NOT EXISTS facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    category TEXT NOT NULL,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    source TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_accessed_at TEXT,
                    expires_at TEXT,
                    is_active INTEGER NOT NULL DEFAULT 1,
                    UNIQUE(user_id, category, key)
                );
                CREATE INDEX IF NOT EXISTS idx_facts_active
                    ON facts (user_id, is_active, category);
            """)

    def upsert_fact(
        self,
        user_id: str,
        category: str,
        key: str,
        value: str,
        source: str | None = None,
        expires_at: str | None = None,
    ):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO facts (user_id, category, key, value, source, expires_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id, category, key) DO UPDATE SET
                    value = excluded.value,
                    source = excluded.source,
                    expires_at = excluded.expires_at,
                    is_active = 1,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (user_id, category, key, value, source, expires_at),
            )

    def list_facts(self, user_id: str, limit: int = 20) -> list[dict]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT id, category, key, value, source, created_at, updated_at
                FROM facts
                WHERE user_id = ? AND is_active = 1 AND (expires_at IS NULL OR expires_at > CURRENT_TIMESTAMP)
                ORDER BY updated_at DESC, id DESC
                LIMIT ?
            """,
                (user_id, limit),
            ).fetchall()
            if rows:
                conn.executemany(
                    """
                    UPDATE facts
                    SET last_accessed_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    [(row["id"],) for row in rows],
                )
        return [dict(row) for row in rows]

    def forget_fact(self, user_id: str, category: str, key: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                UPDATE facts
                SET is_active = 0,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ? AND category = ? AND key = ? AND is_active = 1
                """,
                (user_id, category, key),
            )
            return cursor.rowcount > 0

    def clear_facts(self, user_id: str) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                UPDATE facts
                SET is_active = 0,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ? AND is_active = 1
                """,
                (user_id,),
            )
            return cursor.rowcount
