import sqlite3
import yaml
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Snippet:
    """Represents a code snippet with multiple content cells"""
    id: Optional[int]
    title: str
    language: str
    cells: List[Dict[str, Any]]  # List of cells: [{'type': 'code', 'content': '...'}, {'type': 'text', 'content': '...'}, ...]
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class Database:
    def __init__(self, db_name="snippets.db"):
        self.db_path = Path(db_name)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Create the snippets table if it doesn't exist"""
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

    def add_snippet(self, snippet: Snippet) -> int:
        """Add a new snippet to the database"""
        # Serialize the cells to YAML string
        yaml_content = yaml.dump({
            'metadata': {
                'title': snippet.title,
                'language': snippet.language,
                'tags': snippet.tags or []
            },
            'cells': snippet.cells
        })
        
        # Convert tags list to comma-separated string
        tags_str = ','.join(snippet.tags) if snippet.tags else ''
        
        self.cursor.execute(
            "INSERT INTO snippets (title, language, rich_content, tags) VALUES (?, ?, ?, ?)",
            (snippet.title, snippet.language, yaml_content, tags_str)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_snippets(self, search_query: str = "") -> List[Snippet]:
        """Retrieve all snippets, optionally filtered by search query"""
        if search_query:
            # Search in title, language, and tags
            query = """
                SELECT id, title, language, rich_content, tags 
                FROM snippets 
                WHERE title LIKE ? OR language LIKE ? OR tags LIKE ?
                ORDER BY id DESC
            """
            search_pattern = f"%{search_query}%"
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern))
        else:
            self.cursor.execute("SELECT id, title, language, rich_content, tags FROM snippets ORDER BY id DESC")
        
        rows = self.cursor.fetchall()
        snippets = []
        
        for row in rows:
            snippet_id, title, language, yaml_content, tags_str = row
            
            # Parse the YAML content
            try:
                data = yaml.safe_load(yaml_content)
                cells = data.get('cells', [])
                metadata = data.get('metadata', {})
                
                # Parse tags from comma-separated string
                tags = tags_str.split(',') if tags_str else []
                tags = [tag.strip() for tag in tags if tag.strip()]
                
                snippet = Snippet(
                    id=snippet_id,
                    title=title,
                    language=language,
                    cells=cells,
                    tags=tags
                )
                snippets.append(snippet)
            except yaml.YAMLError:
                # If YAML parsing fails, create a basic snippet with the raw content
                snippet = Snippet(
                    id=snippet_id,
                    title=title,
                    language=language,
                    cells=[{'type': 'text', 'content': yaml_content}],
                    tags=[]
                )
                snippets.append(snippet)
        
        return snippets

    def get_snippet_by_id(self, snippet_id: int) -> Optional[Snippet]:
        """Retrieve a specific snippet by ID"""
        self.cursor.execute(
            "SELECT id, title, language, rich_content, tags FROM snippets WHERE id = ?",
            (snippet_id,)
        )
        row = self.cursor.fetchone()
        
        if not row:
            return None
            
        snippet_id, title, language, yaml_content, tags_str = row
        
        try:
            data = yaml.safe_load(yaml_content)
            cells = data.get('cells', [])
            metadata = data.get('metadata', {})
            
            # Parse tags from comma-separated string
            tags = tags_str.split(',') if tags_str else []
            tags = [tag.strip() for tag in tags if tag.strip()]
            
            return Snippet(
                id=snippet_id,
                title=title,
                language=language,
                cells=cells,
                tags=tags
            )
        except yaml.YAMLError:
            # If YAML parsing fails, return a basic snippet
            return Snippet(
                id=snippet_id,
                title=title,
                language=language,
                cells=[{'type': 'text', 'content': yaml_content}],
                tags=[]
            )

    def update_snippet(self, snippet: Snippet):
        """Update an existing snippet"""
        if snippet.id is None:
            raise ValueError("Snippet ID is required for update")
        
        # Serialize the cells to YAML string
        yaml_content = yaml.dump({
            'metadata': {
                'title': snippet.title,
                'language': snippet.language,
                'tags': snippet.tags or []
            },
            'cells': snippet.cells
        })
        
        # Convert tags list to comma-separated string
        tags_str = ','.join(snippet.tags) if snippet.tags else ''
        
        self.cursor.execute(
            "UPDATE snippets SET title = ?, language = ?, rich_content = ?, tags = ? WHERE id = ?",
            (snippet.title, snippet.language, yaml_content, tags_str, snippet.id)
        )
        self.conn.commit()

    def delete_snippet(self, snippet_id: int):
        """Delete a snippet by ID"""
        self.cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
        self.conn.commit()

    def close(self):
        """Close the database connection"""
        self.conn.close()