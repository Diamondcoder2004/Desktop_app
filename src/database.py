import sqlite3
from typing import List, Tuple, Optional
import yaml


class Database:
    """Class for handling database operations with SQLite."""

    def __init__(self, db_name: str = "snippets.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the snippets table with rich_content for multi-cell snippets."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                language TEXT NOT NULL,
                rich_content TEXT NOT NULL,
                tags TEXT DEFAULT ''
            )
        """)
        self.conn.commit()

    def add_snippet(self, title: str, language: str, cells: list, tags: str = "") -> int:
        """Add a new snippet with multi-cell content."""
        # Convert cells list to YAML
        yaml_content = yaml.dump(cells, allow_unicode=True)
        self.cursor.execute(
            "INSERT INTO snippets (title, language, rich_content, tags) VALUES (?, ?, ?, ?)",
            (title, language, yaml_content, tags)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_snippets(self, search_query: str = "") -> List[Tuple]:
        """Get all snippets, optionally filtered by search query."""
        if search_query:
            query = """
            SELECT id, title, language, rich_content, tags 
            FROM snippets 
            WHERE title LIKE ? OR language LIKE ? OR tags LIKE ? 
            ORDER BY id DESC
            """
            self.cursor.execute(query, (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
        else:
            self.cursor.execute("SELECT id, title, language, rich_content, tags FROM snippets ORDER BY id DESC")

        rows = self.cursor.fetchall()
        snippets = []
        for row in rows:
            try:
                cells = yaml.safe_load(row[3]) if row[3] else []
                snippets.append((row[0], row[1], row[2], cells, row[4]))
            except yaml.YAMLError:
                # Fallback: create a simple code cell
                cells = [{"type": "code", "language": row[2], "content": row[3]}]
                snippets.append((row[0], row[1], row[2], cells, row[4]))

        return snippets

    def get_snippet_by_id(self, snippet_id: int) -> Optional[Tuple]:
        """Get a specific snippet by its ID."""
        self.cursor.execute(
            "SELECT id, title, language, rich_content, tags FROM snippets WHERE id = ?",
            (snippet_id,)
        )
        row = self.cursor.fetchone()
        if row:
            try:
                cells = yaml.safe_load(row[3]) if row[3] else []
                return (row[0], row[1], row[2], cells, row[4])
            except yaml.YAMLError:
                cells = [{"type": "code", "language": row[2], "content": row[3]}]
                return (row[0], row[1], row[2], cells, row[4])
        return None

    def update_snippet(self, snippet_id: int, title: str, language: str, cells: list, tags: str = ""):
        """Update an existing snippet."""
        yaml_content = yaml.dump(cells, allow_unicode=True)
        self.cursor.execute(
            "UPDATE snippets SET title = ?, language = ?, rich_content = ?, tags = ? WHERE id = ?",
            (title, language, yaml_content, tags, snippet_id)
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