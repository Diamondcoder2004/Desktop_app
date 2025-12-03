# test_db.py в папке src
import sys
import os

sys.path.insert(0, '.')

from models.database import Database


def test_database():
    db = Database()

    print("Тест 1: Получить существующие сниппеты")
    snippets = db.get_snippets()
    print(f"Найдено сниппетов: {len(snippets)}")

    print("\nТест 2: Добавить новый сниппет")
    test_cells = [
        {
            "type": "code",
            "language": "python",
            "content": "print('Hello World')"
        }
    ]

    try:
        snippet_id = db.add_snippet("Тестовый сниппет", "python", test_cells, "test")
        print(f"Сниппет добавлен с ID: {snippet_id}")
    except Exception as e:
        print(f"Ошибка при добавлении: {e}")

    print("\nТест 3: Проверить что сниппет добавился")
    snippets = db.get_snippets()
    print(f"Теперь сниппетов: {len(snippets)}")
    for s in snippets:
        print(f"ID: {s[0]}, Title: {s[1]}")

    db.close()


if __name__ == "__main__":
    test_database()