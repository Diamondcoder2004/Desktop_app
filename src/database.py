import sqlite3
from typing import List, Tuple, Optional


class Database:
    """Class for handling database operations with SQLite."""
    
    def __init__(self, db_name: str = "snippets.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the snippets table if it doesn't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                language TEXT NOT NULL,
                code TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_snippet(self, title: str, language: str, code: str) -> int:
        """Add a new snippet to the database."""
        self.cursor.execute(
            "INSERT INTO snippets (title, language, code) VALUES (?, ?, ?)", 
            (title, language, code)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_snippets(self, search_query: str = "") -> List[Tuple[int, str, str, str]]:
        """Get all snippets, optionally filtered by search query."""
        if search_query:
            query = "SELECT * FROM snippets WHERE title LIKE ? OR language LIKE ? ORDER BY id DESC"
            self.cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
        else:
            self.cursor.execute("SELECT * FROM snippets ORDER BY id DESC")
        return self.cursor.fetchall()

    def get_snippet_by_id(self, snippet_id: int) -> Optional[Tuple[int, str, str, str]]:
        """Get a specific snippet by its ID."""
        self.cursor.execute("SELECT * FROM snippets WHERE id = ?", (snippet_id,))
        return self.cursor.fetchone()

    def update_snippet(self, snippet_id: int, title: str, language: str, code: str):
        """Update an existing snippet."""
        self.cursor.execute(
            "UPDATE snippets SET title = ?, language = ?, code = ? WHERE id = ?",
            (title, language, code, snippet_id)
        )
        self.conn.commit()

    def delete_snippet(self, snippet_id: int):
        """Delete a snippet from the database."""
        self.cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()