
---

### 2. `database.py`
```python
import sqlite3
import hashlib

class CloudDatabase:
    def __init__(self, db_name=":memory:"):
        """Initialize the database connection. Defaults to in-memory for testing."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Create the records table if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hash TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def get_all_records(self):
        """Fetch all existing records for validation."""
        self.cursor.execute("SELECT data_hash, content FROM records")
        return [{"hash": row[0], "content": row[1]} for row in self.cursor.fetchall()]

    def insert_record(self, content):
        """Append a new, unique record to the database."""
        data_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        try:
            self.cursor.execute(
                "INSERT INTO records (data_hash, content) VALUES (?, ?)",
                (data_hash, content)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Fallback in case of race conditions
            return False