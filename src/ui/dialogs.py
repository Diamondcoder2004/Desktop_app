import flet as ft
from typing import Callable, Optional
import yaml


class AddSnippetDialog:
    """Dialog for adding a new multi-cell snippet."""

    def __init__(self, on_submit: Callable[[str, str, list], None], on_cancel: Callable[[], None]):
        self.on_submit = on_submit
        self.on_cancel = on_cancel

        # Cell type selector
        self.cell_type = ft.Dropdown(
            label="Тип ячейки",
            width=200,
            options=[
                ft.dropdown.Option("text"),
                ft.dropdown.Option("code"),
            ],
            value="code"
        )

        # Create form fields
        self.title_field = ft.TextField(
            label="Название сниппета",
            width=400,
            autofocus=True
        )
        self.lang_field = ft.Dropdown(
            label="Основной язык",
            width=400,
            options=[
                ft.dropdown.Option("python"),
                ft.dropdown.Option("javascript"),
                ft.dropdown.Option("sql"),
                ft.dropdown.Option("html"),
                ft.dropdown.Option("css"),
                ft.dropdown.Option("c++"),
                ft.dropdown.Option("java"),
                ft.dropdown.Option("go"),
                ft.dropdown.Option("rust"),
                ft.dropdown.Option("bash"),
                ft.dropdown.Option("markdown"),
                ft.dropdown.Option("json"),
                ft.dropdown.Option("yaml"),
                ft.dropdown.Option("xml"),
            ],
            value="python"
        )
        self.code_field = ft.TextField(
            label="Содержимое ячейки",
            multiline=True,
            min_lines=5,
            max_lines=15,
            width=400,
            text_style=ft.TextStyle(font_family="Consolas")
        )

        # Create dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новый сниппет (одна ячейка)"),
            content=ft.Column(
                [
                    self.title_field,
                    self.lang_field,
                    self.cell_type,
                    self.code_field
                ],
                height=450,
                width=400,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton("Отмена", on_click=self._handle_cancel),
                ft.ElevatedButton("Сохранить", on_click=self._handle_submit),
            ],
        )

    def _handle_submit(self, e):
        """Handle submit button click."""
        print(f"DEBUG: AddSnippetDialog._handle_submit called - title: {self.title_field.value}, code length: {len(self.code_field.value) if self.code_field.value else 0}")

        if not self.title_field.value or not self.code_field.value:
            print("DEBUG: Error - required fields are empty")
            # Show error notification
            if hasattr(self, 'dialog') and hasattr(self.dialog.page, 'snack_bar'):
                self.dialog.page.snack_bar = ft.SnackBar(ft.Text("Пожалуйста, заполните все обязательные поля!"))
                self.dialog.page.snack_bar.open = True
                self.dialog.page.update()
            return

        # Create a cell based on selected type
        cell_type = self.cell_type.value or "code"
        if cell_type == "text":
            cell = {
                "type": "text",
                "content": self.code_field.value
            }
        else:  # code
            cell = {
                "type": "code",
                "language": self.lang_field.value or "python",
                "content": self.code_field.value
            }

        cells = [cell]
        print(f"DEBUG: Created cell of type '{cell_type}' with {len(cells)} cells")
        self.on_submit(self.title_field.value, self.lang_field.value or "python", cells)
        print("DEBUG: on_submit callback called successfully")

    def _handle_cancel(self, e):
        """Handle cancel button click."""
        self.on_cancel()

    def open(self, page: ft.Page):
        """Open the dialog."""
        print("DEBUG: AddSnippetDialog.open called")
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()
        print("DEBUG: AddSnippetDialog opened successfully")

    def close(self, page: ft.Page):
        """Close the dialog."""
        print("DEBUG: AddSnippetDialog.close called")
        self.dialog.open = False
        page.dialog = None
        page.update()
        print("DEBUG: AddSnippetDialog closed successfully")

    def clear_fields(self):
        """Clear all form fields."""
        self.title_field.value = ""
        self.code_field.value = ""
        self.lang_field.value = "python"
        self.cell_type.value = "code"


class EditSnippetDialog:
    """Dialog for editing an existing snippet."""

    def __init__(self, on_submit: Callable[[int, str, str, list], None], on_cancel: Callable[[], None]):
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.snippet_id = None

        # Cell type selector
        self.cell_type = ft.Dropdown(
            label="Тип ячейки",
            width=200,
            options=[
                ft.dropdown.Option("text"),
                ft.dropdown.Option("code"),
            ],
            value="code"
        )

        # Create form fields
        self.title_field = ft.TextField(
            label="Название сниппета",
            width=400,
            autofocus=True
        )
        self.lang_field = ft.Dropdown(
            label="Основной язык",
            width=400,
            options=[
                ft.dropdown.Option("python"),
                ft.dropdown.Option("javascript"),
                ft.dropdown.Option("sql"),
                ft.dropdown.Option("html"),
                ft.dropdown.Option("css"),
                ft.dropdown.Option("c++"),
                ft.dropdown.Option("java"),
                ft.dropdown.Option("go"),
                ft.dropdown.Option("rust"),
                ft.dropdown.Option("bash"),
                ft.dropdown.Option("markdown"),
                ft.dropdown.Option("json"),
                ft.dropdown.Option("yaml"),
                ft.dropdown.Option("xml"),
            ],
            value="python"
        )
        self.code_field = ft.TextField(
            label="Содержимое ячейки",
            multiline=True,
            min_lines=5,
            max_lines=15,
            width=400,
            text_style=ft.TextStyle(font_family="Consolas")
        )

        # Create dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактировать сниппет"),
            content=ft.Column(
                [
                    self.title_field,
                    self.lang_field,
                    self.cell_type,
                    self.code_field
                ],
                height=450,
                width=400,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[
                ft.TextButton("Отмена", on_click=self._handle_cancel),
                ft.ElevatedButton("Сохранить", on_click=self._handle_submit),
            ],
        )

    def _handle_submit(self, e):
        """Handle submit button click."""
        print(f"DEBUG: EditSnippetDialog._handle_submit called - title: {self.title_field.value}, code length: {len(self.code_field.value) if self.code_field.value else 0}")

        if not self.title_field.value or not self.code_field.value:
            print("DEBUG: Error - required fields are empty")
            # Show error notification
            if hasattr(self, 'dialog') and hasattr(self.dialog.page, 'snack_bar'):
                self.dialog.page.snack_bar = ft.SnackBar(ft.Text("Пожалуйста, заполните все обязательные поля!"))
                self.dialog.page.snack_bar.open = True
                self.dialog.page.update()
            return

        # Create a cell based on selected type
        cell_type = self.cell_type.value or "code"
        if cell_type == "text":
            cell = {
                "type": "text",
                "content": self.code_field.value
            }
        else:  # code
            cell = {
                "type": "code",
                "language": self.lang_field.value or "python",
                "content": self.code_field.value
            }

        cells = [cell]
        print(f"DEBUG: Created cell of type '{cell_type}' with {len(cells)} cells")
        if self.snippet_id is not None:
            print(f"DEBUG: Calling on_submit with snippet_id {self.snippet_id}")
            self.on_submit(self.snippet_id, self.title_field.value, self.lang_field.value or "python", cells)
            print("DEBUG: on_submit callback called successfully")
        else:
            print("DEBUG: Cannot submit - snippet_id is None")

    def _handle_cancel(self, e):
        """Handle cancel button click."""
        self.on_cancel()

    def open(self, page: ft.Page, snippet_id: int, title: str, language: str, cells: list):
        """Open the dialog with existing snippet data."""
        print(f"DEBUG: EditSnippetDialog.open called for snippet {snippet_id}")
        self.snippet_id = snippet_id
        self.title_field.value = title
        self.lang_field.value = language

        # Show first cell (simplified editing)
        if cells:
            first_cell = cells[0]
            self.cell_type.value = first_cell.get("type", "code")
            self.code_field.value = first_cell.get("content", "")
            print(f"DEBUG: Loaded first cell of type '{first_cell.get('type', 'code')}' with {len(first_cell.get('content', ''))} chars")

        page.dialog = self.dialog
        self.dialog.open = True
        page.update()
        print("DEBUG: EditSnippetDialog opened successfully")

    def close(self, page: ft.Page):
        """Close the dialog."""
        print("DEBUG: EditSnippetDialog.close called")
        self.dialog.open = False
        page.dialog = None
        page.update()
        print("DEBUG: EditSnippetDialog closed successfully")

    def clear_fields(self):
        """Clear all form fields."""
        self.title_field.value = ""
        self.code_field.value = ""
        self.lang_field.value = "python"
        self.cell_type.value = "code"
        self.snippet_id = None