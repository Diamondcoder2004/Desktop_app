import flet as ft
from src.models.database import Database
from src.ui.code_editor import MultiCellEditor


class MainEditorView(ft.UserControl):
    def __init__(self, db: Database, page: ft.Page, on_back, initial_snippet=None):
        super().__init__()
        self.db = db
        self.page = page
        self.on_back = on_back
        self.initial_snippet = initial_snippet
        self.current_snippet = None
        self.cells_editor = None

        # Левая панель: список сниппетов
        self.snippets_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=10,
            auto_scroll=True
        )

        # Правая панель: редактор
        self.editor_container = ft.Container(
            expand=3,
            padding=20,
            content=ft.Column([
                ft.Text("Выберите сниппет для редактирования",
                        size=18,
                        color=ft.colors.GREY_700,
                        italic=True)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

        self._load_snippets()
        if self.initial_snippet:
            self._open_snippet(self.initial_snippet)

    # main_editor_view.py — замените build()
    def build(self):
        self.header = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: self.on_back()),
                ft.Text("Большой редактор", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.ElevatedButton("Новый сниппет", icon=ft.icons.ADD, on_click=self._handle_new_snippet)
            ],
            spacing=10,
            alignment=ft.MainAxisAlignment.START
        )

        # Левая панель: фиксированная ширина + прокрутка
        left_panel = ft.Container(
            content=ft.ListView(
                controls=self.snippets_list.controls,
                expand=True,
                spacing=10,
                padding=10,
                auto_scroll=False
            ),
            width=300,
            border=ft.border.only(right=ft.border.BorderSide(1, ft.colors.OUTLINE)),
            bgcolor=ft.colors.SURFACE_VARIANT,
            # Фиксируем высоту, чтобы не зависеть от правой панели
            height=self.page.window.height - 60  # ~высота header
        )

        # Правая панель: прокручиваемый редактор
        right_panel = ft.Column([
            ft.Container(content=self.header, padding=10),
            ft.Container(
                content=self.editor_container,
                expand=True,
                padding=10
            )
        ], expand=True)

        return ft.Row([left_panel, right_panel], expand=True)

    def _load_snippets(self):
        """Загружает список сниппетов в левую панель"""
        self.snippets_list.controls.clear()
        snippets = self.db.get_snippets()

        for snippet in snippets:
            card = ft.Container(
                content=ft.Column([
                    ft.Text(snippet["title"], weight=ft.FontWeight.BOLD),
                    ft.Text(
                        f"{snippet['language']} | {snippet['tags'] or 'без тегов'}",
                        size=12,
                        color=ft.colors.GREY_700
                    )
                ], spacing=2),
                padding=10,
                border_radius=5,
                bgcolor=ft.colors.SURFACE,
                on_click=lambda e, s=snippet: self._open_snippet(s),
                border=ft.border.all(1, ft.colors.OUTLINE),
                margin=ft.margin.only(bottom=5)
            )
            self.snippets_list.controls.append(card)

        if not snippets:
            self.snippets_list.controls.append(
                ft.Text("Нет сниппетов", color=ft.colors.GREY_700, italic=True)
            )
        self.update()

    def _open_snippet(self, snippet):
        """Открывает сниппет в редакторе"""
        self.current_snippet = snippet

        # Создаем поля для редактирования
        self.title_field = ft.TextField(
            label="Название",
            value=snippet["title"],
            width=500
        )
        self.lang_field = ft.Dropdown(
            label="Язык",
            value=snippet["language"],
            width=200,
            options=[ft.dropdown.Option(x) for x in [
                "python", "javascript", "bash", "yaml", "json", "sql", "markdown"
            ]]
        )
        self.tags_field = ft.TextField(
            label="Теги",
            value=snippet["tags"] or "",
            width=300
        )

        # Создаем редактор ячеек
        self.cells_editor = MultiCellEditor(self.page)
        self.cells_editor.load_cells(snippet["cells"])

        # Кнопки сохранения
        save_button = ft.ElevatedButton(
            "Сохранить",
            icon=ft.icons.SAVE,
            on_click=self._save_snippet
        )

        # Собираем редактор
        self.editor_container.content = ft.Column([
            ft.Row([self.title_field, self.lang_field, self.tags_field]),
            ft.Divider(),
            self.cells_editor,
            ft.Container(
                content=save_button,
                padding=20,
                alignment=ft.alignment.center
            )
        ], scroll=ft.ScrollMode.AUTO, expand=True)
        self.update()

    def _handle_new_snippet(self, e):
        """Создает новый пустой сниппет"""
        new_snippet = {
            "id": None,
            "title": "Новый сниппет",
            "language": "python",
            "tags": "",
            "cells": [{"type": "code", "content": ""}]
        }
        self._open_snippet(new_snippet)

    def _save_snippet(self, e):
        """Сохраняет текущий сниппет"""
        title = self.title_field.value.strip()
        language = self.lang_field.value
        tags = self.tags_field.value
        cells = self.cells_editor.get_cells()

        if not title:
            self.page.show_snack_bar(ft.SnackBar(
                ft.Text("Название не может быть пустым!"),
                bgcolor=ft.colors.ERROR
            ))
            return

        if self.current_snippet.get("id"):
            # Обновляем существующий
            self.db.update_snippet(
                self.current_snippet["id"],
                title,
                language,
                cells,
                tags
            )
            self.page.show_snack_bar(ft.SnackBar(ft.Text("✅ Сниппет обновлен!")))
        else:
            # Создаем новый
            new_id = self.db.add_snippet(title, language, cells, tags)
            self.current_snippet["id"] = new_id
            self.page.show_snack_bar(ft.SnackBar(ft.Text("✅ Сниппет создан!")))
            # Обновляем список
            self._load_snippets()