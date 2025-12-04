import sqlite3
import os
from pathlib import Path
from typing import List, Dict, Optional
import yaml
import traceback

class Database:
    """Класс для работы с операциями базы данных SQLite."""

    def __init__(self, db_name: str = "snippets.db"):
        print("DEBUG: Инициализация Database")
        # Определяем путь к базе данных
        current_dir = Path(os.getcwd())
        src_dir = current_dir / "src" if current_dir.name != "src" else current_dir
        db_path = src_dir / db_name

        # Создаем директорию если нужно
        db_path.parent.mkdir(exist_ok=True)

        self.db_name = str(db_path)
        print(f"DEBUG: Путь к базе данных: {self.db_name}")

        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Создание таблицы snippets с rich_content для многоячеечных сниппетов."""
        print("DEBUG: Создание таблицы если не существует")
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
        print("DEBUG: Таблица создана или уже существует")

    def add_snippet(self, title: str, language: str, cells: list, tags: str = "") -> int:
        """Добавление нового сниппета с многоячеечным содержимым."""
        print(f"DEBUG: Вызов add_snippet - title: {title}, language: {language}, tags: {tags}")
        print(f"DEBUG: Количество ячеек для добавления: {len(cells)}")
        for i, cell in enumerate(cells):
            print(f"DEBUG: Ячейка {i}: {cell.get('type', 'unknown')} - {len(cell.get('content', ''))} символов")

        try:
            yaml_content = yaml.dump(cells, allow_unicode=True)
            print(f"DEBUG: Длина YAML-контента: {len(yaml_content)}")

            self.cursor.execute(
                "INSERT INTO snippets (title, language, rich_content, tags) VALUES (?, ?, ?, ?)",
                (title, language, yaml_content, tags)
            )
            self.conn.commit()
            result = self.cursor.lastrowid
            print(f"DEBUG: Сниппет добавлен успешно, ID: {result}")
            return result
        except Exception as e:
            print(f"DEBUG: Ошибка в add_snippet: {e}")
            traceback.print_exc()
            raise

    def get_snippets(self, search_query: str = "") -> List[Dict]:
        """Получение всех сниппетов, опционально с фильтром по поисковому запросу."""
        print(f"DEBUG: Вызов get_snippets с запросом: '{search_query}'")
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
        print(f"DEBUG: Получено {len(rows)} строк из базы данных")
        snippets = []
        for row in rows:
            try:
                cells = yaml.safe_load(row[3]) if row[3] else []
                print(f"DEBUG: Загружено {len(cells)} ячеек для сниппета ID {row[0]}")
            except yaml.YAMLError as yaml_err:
                print(f"DEBUG: Ошибка парсинга YAML для сниппета ID {row[0]}: {yaml_err}, использование fallback")
                cells = [{"type": "code", "language": row[2], "content": row[3]}]
            snippets.append({
                "id": row[0],
                "title": row[1],
                "language": row[2],
                "cells": cells,
                "tags": row[4]
            })

        print(f"DEBUG: Возвращаю {len(snippets)} сниппетов")
        return snippets

    def get_snippet_by_id(self, snippet_id: int) -> Optional[Dict]:
        """Получение конкретного сниппета по ID."""
        print(f"DEBUG: Вызов get_snippet_by_id для ID: {snippet_id}")
        self.cursor.execute(
            "SELECT id, title, language, rich_content, tags FROM snippets WHERE id = ?",
            (snippet_id,)
        )
        row = self.cursor.fetchone()
        if row:
            try:
                cells = yaml.safe_load(row[3]) if row[3] else []
                print(f"DEBUG: Загружен сниппет {snippet_id} с {len(cells)} ячейками")
            except yaml.YAMLError as yaml_err:
                print(f"DEBUG: Ошибка парсинга YAML для сниппета ID {snippet_id}: {yaml_err}, использование fallback")
                cells = [{"type": "code", "language": row[2], "content": row[3]}]
            return {
                "id": row[0],
                "title": row[1],
                "language": row[2],
                "cells": cells,
                "tags": row[4]
            }
        print(f"DEBUG: Сниппет с ID {snippet_id} не найден")
        return None

    def update_snippet(self, snippet_id: int, title: str, language: str, cells: list, tags: str = ""):
        """Обновление существующего сниппета."""
        print(f"DEBUG: Вызов update_snippet для ID: {snippet_id}")
        print(f"DEBUG: Обновление с title: {title}, language: {language}, tags: {tags}")
        print(f"DEBUG: Количество ячеек для обновления: {len(cells)}")
        for i, cell in enumerate(cells):
            print(f"DEBUG: Ячейка {i}: {cell.get('type', 'unknown')} - {len(cell.get('content', ''))} символов")

        yaml_content = yaml.dump(cells, allow_unicode=True)
        print(f"DEBUG: Длина YAML-контента: {len(yaml_content)}")
        self.cursor.execute(
            "UPDATE snippets SET title = ?, language = ?, rich_content = ?, tags = ? WHERE id = ?",
            (title, language, yaml_content, tags, snippet_id)
        )
        self.conn.commit()
        print(f"DEBUG: Сниппет {snippet_id} обновлён успешно")

    def delete_snippet(self, snippet_id: int):
        """Удаление сниппета из базы данных."""
        print(f"DEBUG: Вызов delete_snippet для ID: {snippet_id}")
        self.cursor.execute("DELETE FROM snippets WHERE id = ?", (snippet_id,))
        self.conn.commit()
        print(f"DEBUG: Сниппет {snippet_id} удалён успешно")

    def close(self):
        """Закрытие соединения с базой данных."""
        print("DEBUG: Закрытие соединения с базой данных")
        if self.conn:
            self.conn.close()