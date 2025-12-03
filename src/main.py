# main.py
import flet as ft
import sys
import os

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from models.database import Database
    from ui.snippet_card import SnippetCard
    from ui.dialogs import AddSnippetDialog, EditSnippetDialog
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback
    from database import Database
    from snippet_card import SnippetCard
    from dialogs import AddSnippetDialog, EditSnippetDialog

import pyperclip


def initialize_demo_data(db: Database):
    """Initialize the database with demo multi-cell snippets"""
    # Check if database is empty
    snippets = db.get_snippets()
    print(f"Инициализация: в базе {len(snippets)} сниппетов")

    if not snippets:
        print("Initializing demo multi-cell data...")

        # Python Data Science snippet with multiple cells
        python_ds_cells = [
            {
                "type": "text",
                "content": "### Основные библиотеки для Data Science на Python\n\n- **pandas** - работа с табличными данными\n- **numpy** - числовые вычисления\n- **scikit-learn** - машинное обучение\n- **pytorch** - глубокое обучение"
            },
            {
                "type": "code",
                "language": "python",
                "content": """import pandas as pd
import numpy as np

# Создание DataFrame
data = {
    'Имя': ['Анна', 'Борис', 'Клара'],
    'Возраст': [25, 30, 35],
    'Город': ['Москва', 'Санкт-Петербург', 'Казань']
}

df = pd.DataFrame(data)
print(df)"""
            },
            {
                "type": "code",
                "language": "python",
                "content": """# Пример работы с numpy
arr = np.array([[1, 2, 3], [4, 5, 6]])
print("Матрица 2x3:")
print(arr)
print(f"Сумма: {arr.sum()}")
print(f"Среднее: {arr.mean()}")"""
            }
        ]
        db.add_snippet("Python: Data Science", "python", python_ds_cells, "python, datascience, pandas")

        # Docker snippet with YAML
        docker_cells = [
            {
                "type": "text",
                "content": "### Docker основные команды\n\nУправление контейнерами и образами"
            },
            {
                "type": "code",
                "language": "bash",
                "content": """# Основные команды
docker ps              # Список запущенных контейнеров
docker images          # Список образов
docker build -t myapp . # Сборка образа
docker run -d -p 80:80 nginx # Запуск контейнера"""
            },
            {
                "type": "code",
                "language": "yaml",
                "content": """# docker-compose.yml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html

  db:
    image: postgres:13
    environment:
      POSTGRES_PASSWORD: example"""
            }
        ]
        db.add_snippet("Docker: Команды и Compose", "dockerfile", docker_cells, "docker, devops, container")

        print("Demo multi-cell data initialized!")


def main(page: ft.Page):
    # Page setup
    page.title = "CodeSnippet Hub - Multi-cell"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 800
    page.padding = 20

    print("=== ПРИЛОЖЕНИЕ ЗАПУЩЕНО ===")

    # Initialize database
    db = Database()

    # Initialize demo data
    initialize_demo_data(db)

    # Search field
    search_field = ft.TextField(
        label="Поиск по названию, языку или тегам",
        prefix_icon="search",
        expand=True,
        on_change=lambda e: print(f"Поиск изменился: {e.control.value}")
    )

    # Тестовая кнопка
    test_button = ft.ElevatedButton(
        "ТЕСТ: Добавить напрямую",
        on_click=lambda e: test_add_directly(e),
        bgcolor="green"
    )

    # Snippets grid
    snippets_grid = ft.GridView(
        expand=1,
        runs_count=2,
        max_extent=500,
        child_aspect_ratio=1.2,
        spacing=20,
        run_spacing=20,
    )

    # Functions
    def load_snippets(search_query: str = ""):
        """Load snippets from database."""
        print(f"Загрузка сниппетов, поиск: '{search_query}'")
        snippets_grid.controls.clear()

        snippets = db.get_snippets(search_query)
        print(f"Загружено {len(snippets)} сниппетов")

        for snippet in snippets:
            snippet_id, title, language, cells, tags = snippet
            print(f"  Создаю карточку: {title} (ID: {snippet_id})")

            card = SnippetCard(
                snippet_id=snippet_id,
                title=title,
                language=language,
                cells=cells,
                on_copy=handle_copy,
                on_delete=handle_delete,
                on_edit=handle_edit
            )
            snippets_grid.controls.append(card)

        page.update()

    def handle_search(e):
        """Handle search field changes."""
        print(f"Обработка поиска: {search_field.value}")
        load_snippets(search_field.value)

    def test_add_directly(e):
        """Прямое добавление для теста."""
        print("\n=== ТЕСТ: Прямое добавление ===")
        test_cells = [
            {
                "type": "code",
                "language": "python",
                "content": "# Тестовый сниппет\nprint('Test from button')"
            }
        ]
        try:
            snippet_id = db.add_snippet("Тест напрямую", "python", test_cells, "test")
            print(f"✓ Сниппет добавлен напрямую, ID: {snippet_id}")
            # Покажем уведомление
            page.snack_bar = ft.SnackBar(ft.Text("Тестовый сниппет добавлен напрямую!"))
            page.snack_bar.open = True
            load_snippets(search_field.value)
            page.update()
        except Exception as ex:
            print(f"✗ Ошибка при прямом добавлении: {ex}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {ex}"))
            page.snack_bar.open = True
            page.update()

    def handle_add_snippet(e):
        """Handle add snippet button click."""
        print("\n=== ОТКРЫТИЕ ДИАЛОГА ДОБАВЛЕНИЯ ===")

        def on_submit(title: str, language: str, cells: list):
            print(f"✓ Диалог: получены данные")
            print(f"  Title: {title}")
            print(f"  Language: {language}")
            print(f"  Cells: {cells}")

            try:
                snippet_id = db.add_snippet(title, language, cells, "")
                print(f"✓ Сниппет добавлен в БД, ID: {snippet_id}")

                # Закрываем диалог
                dialog.close(page)

                # Обновляем список
                load_snippets(search_field.value)

                # Показываем уведомление
                page.snack_bar = ft.SnackBar(ft.Text(f"Сниппет '{title}' добавлен!"))
                page.snack_bar.open = True
                page.update()

            except Exception as ex:
                print(f"✗ Ошибка при добавлении в БД: {ex}")
                page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка: {ex}"))
                page.snack_bar.open = True
                page.update()

        def on_cancel():
            print("✗ Диалог отменен")
            dialog.close(page)

        dialog = AddSnippetDialog(on_submit=on_submit, on_cancel=on_cancel)
        print("✓ Диалог создан, открываю...")
        dialog.open(page)

    def handle_copy(yaml_content: str):
        """Handle copy button click."""
        pyperclip.copy(yaml_content)
        page.snack_bar = ft.SnackBar(ft.Text("YAML содержимое скопировано в буфер!"))
        page.snack_bar.open = True
        page.update()

    def handle_delete(snippet_id: int):
        """Handle delete button click."""
        print(f"Удаление сниппета {snippet_id}")

        def on_confirm():
            db.delete_snippet(snippet_id)
            dialog.open = False
            page.dialog = None
            page.update()
            load_snippets(search_field.value)

        def on_cancel():
            dialog.open = False
            page.dialog = None
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Удалить сниппет?"),
            content=ft.Text("Вы уверены, что хотите удалить этот сниппет? Это действие нельзя отменить."),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: on_cancel()),
                ft.TextButton("Удалить", on_click=lambda e: on_confirm()),
            ],
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def handle_edit(snippet_id: int, title: str, language: str, cells: list):
        """Handle edit button click."""
        print(f"Редактирование сниппета {snippet_id}")

        def on_submit(s_id: int, new_title: str, new_language: str, new_cells: list):
            db.update_snippet(s_id, new_title, new_language, new_cells, "")
            dialog.close(page)
            load_snippets(search_field.value)

        def on_cancel():
            dialog.close(page)

        dialog = EditSnippetDialog(on_submit=on_submit, on_cancel=on_cancel)
        dialog.open(page, snippet_id, title, language, cells)

    # Connect search field
    search_field.on_change = handle_search

    # Create layout
    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        search_field,
                        test_button,
                        ft.ElevatedButton(
                            "Добавить сниппет",
                            icon="add",
                            on_click=handle_add_snippet,
                            bgcolor="blue"
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(),
                ft.Container(
                    content=snippets_grid,
                    expand=True
                )
            ],
            expand=True
        )
    )

    # Load initial snippets
    load_snippets()

    print("=== ИНТЕРФЕЙС СОЗДАН, ГОТОВ К РАБОТЕ ===")


if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)