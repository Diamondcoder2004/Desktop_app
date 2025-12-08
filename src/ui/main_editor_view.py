import flet as ft
from src.models.database import Database
from src.ui.code_editor import MultiCellEditor
from src.utils.constants import SUPPORTED_LANGUAGES


class MainEditorView(ft.UserControl):
    def __init__(self, db: Database, page: ft.Page, on_back, initial_snippet=None):
        super().__init__()
        self.db = db
        self.page = page
        self.on_back = on_back
        self.initial_snippet = initial_snippet
        self.current_snippet = None
        self.cells_editor = None

        # Создаём виджеты, но НЕ загружаем данные
        self.snippets_list_view = ft.ListView(
            spacing=10,
            padding=10,
            auto_scroll=False,
            # expand=True  # не нужно здесь — задаётся в build
        )
        self.editor_container = ft.Container(
            padding=20,
            content=ft.Column([
                ft.Text("Выберите сниппет для редактирования",
                        size=18,
                        color=ft.colors.GREY_700,
                        italic=True)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def did_mount(self):
        """Вызывается после добавления виджета на страницу — безопасно обновлять."""
        print("DEBUG: MainEditorView.did_mount вызван")
        self._load_snippets()
        if self.initial_snippet:
            self._open_snippet(self.initial_snippet)

    def build(self):
        header = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: self.on_back()),
                ft.Text("Большой редактор", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.ElevatedButton("Новый сниппет", icon=ft.icons.ADD, on_click=self._handle_new_snippet)
            ],
            spacing=10
        )

        # Оборачиваем существующий ListView в контейнер с фиксированной высотой
        left_panel = ft.Container(
            content=self.snippets_list_view,  # ← используем тот же объект, что и в _load_snippets
            width=300,
            height=self.page.window.height - 70,
            border=ft.border.only(right=ft.border.BorderSide(1, ft.colors.OUTLINE)),
            bgcolor=ft.colors.SURFACE_VARIANT,
            alignment=ft.alignment.top_left,
            clip_behavior=ft.ClipBehavior.HARD_EDGE  # чтобы прокрутка не вылезала
        )

        right_panel = ft.Column([
            ft.Container(content=header, padding=10),
            ft.Container(
                content=self.editor_container,
                expand=True,
                padding=10,
                # Дополнительно: гарантируем, что контейнер прокручивается
                height=self.page.window.height - 100  # header + padding
            )
        ], expand=True)
        

        return ft.Row(
            [left_panel, ft.VerticalDivider(width=1), right_panel],
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

    def _load_snippets(self):
        print("DEBUG: MainEditorView._load_snippets вызван")
        self.snippets_list_view.controls.clear()
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
            self.snippets_list_view.controls.append(card)

        if not snippets:
            self.snippets_list_view.controls.append(
                ft.Text("Нет сниппетов", color=ft.colors.GREY_700, italic=True)
            )
        # Теперь безопасно — виджет уже на странице
        self.snippets_list_view.update()

    def _open_snippet(self, snippet):
        self.current_snippet = snippet
        print(f"DEBUG: Открываем сниппет: {snippet.get('title')} (ID={snippet.get('id')})")


        self.title_field = ft.TextField(label="Название", value=snippet["title"], width=500)

        self.lang_field = ft.Dropdown(
            label="Язык", value=snippet["language"], width=200,
            options=[ft.dropdown.Option(lang) for lang in SUPPORTED_LANGUAGES]
        )
        self.tags_field = ft.TextField(label="Теги", value=snippet["tags"] or "", width=300)

        self.cells_editor = MultiCellEditor(self.page)
        self.cells_editor.load_cells(snippet["cells"])

        save_button = ft.ElevatedButton("Сохранить", icon=ft.icons.SAVE, on_click=self._save_snippet)
        delete_button = ft.ElevatedButton(
            "Удалить",
            icon=ft.icons.DELETE,
            color=ft.colors.RED,
            on_click=self._delete_snippet
        )
        # Замените строку с ft.Row на следующее:
        header_fields = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Column([ft.Text("", size=12, color=ft.colors.GREY_700), self.title_field], spacing=5),
                    ft.Column([ft.Text("", size=12, color=ft.colors.GREY_700), self.lang_field], spacing=5),
                    ft.Column([ft.Text("", size=12, color=ft.colors.GREY_700), self.tags_field], spacing=5),
                ],
                spacing=20,
                vertical_alignment=ft.CrossAxisAlignment.START
            ),
            padding=ft.padding.only(bottom=10)
        )

        # === ВАЖНО: оберните всё в ListView для прокрутки ===
        scrollable_editor = ft.ListView(
            controls=[
                header_fields,  # ← замените Row на header_fields
                ft.Divider(),
                self.cells_editor,
                ft.Row([  # ← кнопки в одном ряду
                    save_button,
                    delete_button
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
            ],
            expand=True,
            auto_scroll=False
        )

        self.editor_container.content = scrollable_editor
        self.editor_container.update()

    def _handle_new_snippet(self, e):
        new_snippet = {
            "id": None,
            "title": "Новый сниппет",
            "language": "python",
            "tags": "",
            "cells": [{"type": "code", "content": ""}]
        }
        self._open_snippet(new_snippet)

    def _save_snippet(self, e):
        title = self.title_field.value.strip()
        language = self.lang_field.value
        tags = self.tags_field.value
        cells = self.cells_editor.get_cells()

        if not title:
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Название не может быть пустым!")))
            return

        if self.current_snippet.get("id"):
            self.db.update_snippet(self.current_snippet["id"], title, language, cells, tags)
            self.page.show_snack_bar(ft.SnackBar(ft.Text("✅ Сниппет обновлен!")))
        else:
            new_id = self.db.add_snippet(title, language, cells, tags)
            self.current_snippet["id"] = new_id
            self.page.show_snack_bar(ft.SnackBar(ft.Text("✅ Сниппет создан!")))
            self._load_snippets()  # Обновляем список слева\

    def _delete_snippet(self, e):
        if not self.current_snippet or not self.current_snippet.get("id"):
            return

        def confirm_delete():
            self.db.delete_snippet(self.current_snippet["id"])
            self.page.snack_bar = ft.SnackBar(ft.Text("Сниппет удалён"), bgcolor=ft.colors.ERROR)
            self.page.snack_bar.open = True
            self.page.update()
            # Обновить список слева
            self._load_snippets()
            # Очистить редактор
            self.editor_container.content = ft.Column([
                ft.Text("Выберите сниппет для редактирования", size=18, color=ft.colors.GREY_700, italic=True)
            ], alignment=ft.MainAxisAlignment.CENTER)
            self.editor_container.update()

        # Показать подтверждение
        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтвердите удаление"),
            content=ft.Text(f"Удалить сниппет «{self.current_snippet['title']}»?"),
            actions=[
                ft.TextButton("Отмена", on_click=lambda _: self.page.close_dialog()),
                ft.ElevatedButton("Удалить", color=ft.colors.RED, on_click=lambda _: confirm_delete())
            ]
        )
        self.page.dialog = confirm_dialog
        confirm_dialog.open = True
        self.page.update()