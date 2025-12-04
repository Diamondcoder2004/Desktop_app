import sqlite3
from typing import List, Tuple, Optional
import yaml

import sqlite3
import os
from pathlib import Path
from typing import List, Tuple, Optional
import yaml


class Database:
    """Class for handling database operations with SQLite."""

    def __init__(self, db_name: str = "snippets.db"):
        # Определяем путь к базе данных
        # Если запускаем из корня проекта, создаем в папке src
        # Если запускаем из папки src, создаем там же
        current_dir = Path(os.getcwd())
        if current_dir.name == "src" or (current_dir / "src").exists():
            # Уже в папке src или есть папка src
            if current_dir.name == "src":
                db_path = current_dir / db_name
            else:
                db_path = current_dir / "src" / db_name
        else:
            # В корне проекта, создаем в src
            db_path = current_dir / "src" / db_name

        # Создаем директорию если нужно
        db_path.parent.mkdir(exist_ok=True)

        self.db_name = str(db_path)
        print(f"DEBUG: Database path: {self.db_name}")

        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
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
        print(f"DEBUG: Database.add_snippet called - title: {title}, language: {language}")
        print(f"DEBUG: Number of cells to add: {len(cells)}")
        for i, cell in enumerate(cells):
            print(f"DEBUG: Cell {i}: {cell.get('type', 'unknown')} - {len(cell.get('content', ''))} chars")

        try:
            # Convert cells list to YAML
            import yaml
            yaml_content = yaml.dump(cells, allow_unicode=True)
            print(f"DEBUG: YAML content length: {len(yaml_content)}")

            self.cursor.execute(
                "INSERT INTO snippets (title, language, rich_content, tags) VALUES (?, ?, ?, ?)",
                (title, language, yaml_content, tags)
            )
            self.conn.commit()
            result = self.cursor.lastrowid
            print(f"DEBUG: Snippet added successfully, ID: {result}")
            return result
        except Exception as e:
            print(f"DEBUG: Error in add_snippet: {e}")
            import traceback
            traceback.print_exc()
            raise

    def get_snippets(self, search_query: str = "") -> List[Tuple]:
        """Get all snippets, optionally filtered by search query."""
        print(f"DEBUG: Database.get_snippets called with query: '{search_query}'")
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
        print(f"DEBUG: Retrieved {len(rows)} rows from database")
        snippets = []
        for row in rows:
            try:
                cells = yaml.safe_load(row[3]) if row[3] else []
                print(f"DEBUG: Loaded {len(cells)} cells for snippet ID {row[0]}")
                snippets.append((row[0], row[1], row[2], cells, row[4]))
            except yaml.YAMLError:
                print(f"DEBUG: YAML parsing error for snippet ID {row[0]}, using fallback")
                # Fallback: create a simple code cell
                cells = [{"type": "code", "language": row[2], "content": row[3]}]
                snippets.append((row[0], row[1], row[2], cells, row[4]))

        print(f"DEBUG: Returning {len(snippets)} snippets")
        return snippets

    def get_snippet_by_id(self, snippet_id: int) -> Optional[Tuple]:
        """Get a specific snippet by its ID."""
        print(f"DEBUG: Database.get_snippet_by_id called for ID: {snippet_id}")
        self.cursor.execute(
            "SELECT id, title, language, rich_content, tags FROM snippets WHERE id = ?",
            (snippet_id,)
        )
        row = self.cursor.fetchone()
        if row:
            try:
                cells = yaml.safe_load(row[3]) if row[3] else []
                print(f"DEBUG: Loaded snippet {snippet_id} with {len(cells)} cells")
                return (row[0], row[1], row[2], cells, row[4])
            except yaml.YAMLError:
                print(f"DEBUG: YAML parsing error for snippet ID {snippet_id}, using fallback")
                cells = [{"type": "code", "language": row[2], "content": row[3]}]
                return (row[0], row[1], row[2], cells, row[4])
        print(f"DEBUG: Snippet with ID {snippet_id} not found")
        return None

    def update_snippet(self, snippet_id: int, title: str, language: str, cells: list, tags: str = ""):
        """Update an existing snippet."""
        print(f"DEBUG: Database.update_snippet called for ID: {snippet_id}")
        print(f"DEBUG: Updating with title: {title}, language: {language}")
        print(f"DEBUG: Number of cells to update: {len(cells)}")
        for i, cell in enumerate(cells):
            print(f"DEBUG: Cell {i}: {cell.get('type', 'unknown')} - {len(cell.get('content', ''))} chars")
            
        yaml_content = yaml.dump(cells, allow_unicode=True)
        print(f"DEBUG: YAML content length: {len(yaml_content)}")
        self.cursor.execute(
            "UPDATE snippets SET title = ?, language = ?, rich_content = ?, tags = ? WHERE id = ?",
            (title, language, yaml_content, tags, snippet_id)
        )
        self.conn.commit()
        print(f"DEBUG: Snippet {snippet_id} updated successfully")

    def delete_snippet(self, snippet_id: int):
        """Delete a snippet from the database."""
        print(f"DEBUG: Database.delete_snippet called for ID: {snippet_id}")
        self.cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
        self.conn.commit()
        print(f"DEBUG: Snippet {snippet_id} deleted successfully")

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()