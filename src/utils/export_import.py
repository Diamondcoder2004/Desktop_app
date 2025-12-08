# src/utils/export_import.py
import json
from datetime import datetime

from src.models.database import Database


def export_snippets(db: Database) -> str:
    """Экспортирует ВСЕ сниппеты в JSON"""
    snippets = db.get_all_snippets()
    export_data = {
        "version": "1.0",
        "exported_at": datetime.now().isoformat(),
        "snippets": []
    }

    for s in snippets:
        export_data["snippets"].append({
            "id": s["id"],
            "title": s["title"],
            "language": s["language"],
            "tags": s["tags"].split(",") if s["tags"] else [],
            "cells": json.loads(s["cells"]),  # ваш текущий формат
            "created_at": s["created_at"],
            "updated_at": s["updated_at"]
        })

    return json.dumps(export_data, indent=2, ensure_ascii=False)


def import_snippets(db: Database, json_data: str):
    """Импортирует сниппеты из JSON"""
    data = json.loads(json_data)

    for snippet in data["snippets"]:
        # Проверяем, нет ли такого сниппета
        existing = db.get_snippet_by_title(snippet["title"])
        if existing:
            continue  # или обновляем

        db.add_snippet(
            title=snippet["title"],
            language=snippet["language"],
            cells=snippet["cells"],
            tags=",".join(snippet["tags"])
        )