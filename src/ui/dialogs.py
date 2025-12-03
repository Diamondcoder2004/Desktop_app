import flet as ft
from typing import Callable, Optional
import yaml
from .code_editor import MultiCellEditor


class AddSnippetDialog:
    """Dialog for adding a new multi-cell snippet."""

    def __init__(self, on_submit: Callable[[str, str, list], None], on_cancel: Callable[[], None]):
        self.on_submit = on_submit
        self.on_cancel = on_cancel

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

        # Create multi-cell editor
        self.cells_editor = MultiCellEditor(
            cells=[{
                "type": "code",
                "content": ""
            }],
            on_change=self._on_cells_change
        )

        # Create dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новый сниппет (многоячейковый)"),
            content=ft.Container(
                content=ft.Column(
                    [
                        self.title_field,
                        self.lang_field,
                        self.cells_editor
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10
                ),
                width=800,
                height=600,
                padding=20
            ),
            actions=[
                ft.TextButton("Отмена", on_click=self._handle_cancel),
                ft.ElevatedButton("Сохранить", on_click=self._handle_submit),
            ],
        )

    def _on_cells_change(self, cells: list):
        """Handle changes in cells editor."""
        pass

    def _handle_submit(self, e):
        """Handle submit button click."""
        print(f"DEBUG: AddSnippetDialog._handle_submit called - title: {self.title_field.value}")

        if not self.title_field.value:
            print("DEBUG: Error - title is empty")
            # Show error notification
            if hasattr(e, 'page'):
                snack_bar = ft.SnackBar(ft.Text("Пожалуйста, введите название сниппета!"))
                e.page.overlay.append(snack_bar)
                snack_bar.open = True
                e.page.update()
            return

        cells = self.cells_editor.get_cells()
        if not cells:
            cells = [{"type": "code", "content": ""}]

        print(f"DEBUG: Created snippet with {len(cells)} cells")
        self.on_submit(self.title_field.value, self.lang_field.value or "python", cells)

    def _handle_cancel(self, e):
        """Handle cancel button click."""
        self.on_cancel()

    def open(self, page: ft.Page):
        """Open the dialog."""
        print("DEBUG: AddSnippetDialog.open called")
        page.overlay.append(self.dialog)
        self.dialog.open = True
        page.update()
        print("DEBUG: AddSnippetDialog opened successfully")

    def close(self, page: ft.Page):
        """Close the dialog."""
        print("DEBUG: AddSnippetDialog.close called")
        self.dialog.open = False
        page.overlay.remove(self.dialog)
        page.update()
        print("DEBUG: AddSnippetDialog closed successfully")

    def clear_fields(self):
        """Clear all form fields."""
        self.title_field.value = ""
        self.lang_field.value = "python"
        self.cells_editor.load_cells([{"type": "code", "content": ""}])


class EditSnippetDialog:
    """Dialog for editing an existing snippet."""

    def __init__(self, on_submit: Callable[[int, str, str, list], None], on_cancel: Callable[[], None]):
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.snippet_id = None

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

        # Create multi-cell editor
        self.cells_editor = MultiCellEditor(
            cells=[],
            on_change=self._on_cells_change
        )

        # Create dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактировать сниппет"),
            content=ft.Container(
                content=ft.Column(
                    [
                        self.title_field,
                        self.lang_field,
                        self.cells_editor
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    spacing=10
                ),
                width=800,
                height=600,
                padding=20
            ),
            actions=[
                ft.TextButton("Отмена", on_click=self._handle_cancel),
                ft.ElevatedButton("Сохранить", on_click=self._handle_submit),
            ],
        )

    def _on_cells_change(self, cells: list):
        """Handle changes in cells editor."""
        pass

    def _handle_submit(self, e):
        """Handle submit button click."""
        print(f"DEBUG: EditSnippetDialog._handle_submit called - title: {self.title_field.value}")

        if not self.title_field.value:
            print("DEBUG: Error - title is empty")
            if hasattr(e, 'page'):
                snack_bar = ft.SnackBar(ft.Text("Пожалуйста, введите название сниппета!"))
                e.page.overlay.append(snack_bar)
                snack_bar.open = True
                e.page.update()
            return

        cells = self.cells_editor.get_cells()
        if not cells:
            cells = [{"type": "code", "content": ""}]

        if self.snippet_id is not None:
            print(f"DEBUG: Calling on_submit with snippet_id {self.snippet_id}")
            self.on_submit(self.snippet_id, self.title_field.value, self.lang_field.value or "python", cells)

    def _handle_cancel(self, e):
        """Handle cancel button click."""
        self.on_cancel()

    def open(self, page: ft.Page, snippet_id: int, title: str, language: str, cells: list):
        """Open the dialog with existing snippet data."""
        print(f"DEBUG: EditSnippetDialog.open called for snippet {snippet_id}")
        self.snippet_id = snippet_id
        self.title_field.value = title
        self.lang_field.value = language

        # Load all cells into the editor
        self.cells_editor.load_cells(cells)  # Убедитесь, что это есть!
        print(f"DEBUG: Loaded {len(cells)} cells into editor")

        page.overlay.append(self.dialog)  # ВАЖНО: page.overlay.append, а не page.dialog
        self.dialog.open = True
        page.update()
        print("DEBUG: EditSnippetDialog opened successfully")

    def close(self, page: ft.Page):
        """Close the dialog."""
        print("DEBUG: EditSnippetDialog.close called")
        self.dialog.open = False
        page.overlay.remove(self.dialog)  # ВАЖНО: page.overlay.remove
        page.update()
        print("DEBUG: EditSnippetDialog closed successfully")

    def clear_fields(self):
        """Clear all form fields."""
        self.title_field.value = ""
        self.lang_field.value = "python"
        self.cells_editor.load_cells([])
        self.snippet_id = None