import flet as ft
from src.ui.code_editor import MultiCellEditor
from src.utils.constants import SUPPORTED_LANGUAGES


class AddSnippetDialog:
    def __init__(self, on_submit, on_cancel, page: ft.Page):
        self.page = page
        self.on_submit = on_submit
        self.on_cancel = on_cancel

        self.title = ft.TextField(label="Название", width=500, autofocus=True)
        self.lang = ft.Dropdown(
            label="Язык", value="python", width=500,
            options=[ft.dropdown.Option(lang) for lang in SUPPORTED_LANGUAGES ]
        )
        self.tags = ft.TextField(label="Теги (через запятую)", width=500)
        self.editor = MultiCellEditor(page)

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новый сниппет"),
            content=ft.Column([
                self.title, self.lang, self.tags, ft.Divider(), self.editor
            ], width=600, height=500, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Отмена", on_click=self._cancel),
                ft.ElevatedButton("Сохранить", on_click=self._save)
            ]
        )

    def _save(self, e):
        if not self.title.value.strip():
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Введите название!")))
            return
        self.on_submit(
            self.title.value.strip(),
            self.lang.value or "python",
            self.editor.get_cells(),
            self.tags.value or ""
        )
        self.close()

    def _cancel(self, e):
        self.on_cancel()
        self.close()

    def open(self):
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def close(self):
        self.dialog.open = False
        self.page.dialog = None
        self.page.update()

import flet as ft
from src.ui.code_editor import MultiCellEditor

class EditSnippetDialog:
    def __init__(self, on_submit, on_full_edit, page: ft.Page):
        self.page = page
        self.on_submit = on_submit
        self.on_full_edit = on_full_edit
        self.snippet_id = None

        # Поля без встроенных label
        self.title_field = ft.TextField(
            value="",  # будет установлено в open()
            width=480,
            height=50
        )
        self.lang_field = ft.Dropdown(
            value="python",
            width=180,
            height=50,
            options=[ft.dropdown.Option(lang) for lang in SUPPORTED_LANGUAGES]
        )
        self.tags_field = ft.TextField(
            value="",  # будет установлено в open()
            width=280,
            height=50
        )

        # Собираем поля с кастомными подписями сверху
        header_section = ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Название", size=12, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_700),
                    self.title_field
                ], spacing=5),
                ft.Column([
                    ft.Text("Язык", size=12, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_700),
                    self.lang_field
                ], spacing=5),
                ft.Column([
                    ft.Text("Теги", size=12, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_700),
                    self.tags_field
                ], spacing=5),
            ], spacing=20, wrap=True)
        ], spacing=10)

        self.cells_editor = MultiCellEditor(page)

        actions = [
            ft.TextButton("Отмена", on_click=lambda e: self._cancel()),
            ft.ElevatedButton("Сохранить", on_click=self._save),
            ft.ElevatedButton(
                "Большой редактор",
                icon=ft.icons.EDIT,
                on_click=lambda e: self._open_main_editor()
            )
        ]

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактировать сниппет"),
            content=ft.Column([
                header_section,
                ft.Divider(),
                self.cells_editor
            ], width=620, height=550, scroll=ft.ScrollMode.AUTO, spacing=10),
            actions=actions,
            actions_alignment=ft.MainAxisAlignment.END
        )

    def _save(self, e):
        if not self.title_field.value.strip():
            self.page.show_snack_bar(ft.SnackBar(ft.Text("Введите название!")))
            return
        self.on_submit(
            self.snippet_id,
            self.title_field.value.strip(),
            self.lang_field.value or "python",
            self.cells_editor.get_cells(),
            self.tags_field.value or ""
        )
        self.close()

    def _cancel(self):
        self.close()

    def _open_main_editor(self):
        """Открывает большой редактор с текущими данными"""
        current_snippet = {
            "id": self.snippet_id,
            "title": self.title_field.value.strip(),
            "language": self.lang_field.value or "python",
            "tags": self.tags_field.value or "",
            "cells": self.cells_editor.get_cells()
        }
        self.close()
        self.on_full_edit(current_snippet)

    # dialogs.py — замените метод open в EditSnippetDialog
    def open(self, snippet_id: int, title: str, language: str, cells: list, tags: str = ""):
        self.snippet_id = snippet_id
        self.title_field.value = title
        self.lang_field.value = language
        self.tags_field.value = tags

        # Сначала загружаем данные в редактор
        self.cells_editor.load_cells(cells)

        # Затем устанавливаем диалог и обновляем
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
        print(f"DEBUG: EditSnippetDialog открыт для сниппета ID={snippet_id}, ячеек={len(cells)}")


    def close(self):
        self.dialog.open = False
        self.page.dialog = None
        self.page.update()