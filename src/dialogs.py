import flet as ft
from typing import Callable, Optional


class AddSnippetDialog:
    """Dialog for adding a new snippet."""
    
    def __init__(self, on_submit: Callable[[str, str, str], None], on_cancel: Callable[[], None]):
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        
        # Create form fields
        self.title_field = ft.TextField(
            label="Название (напр. Sort Array)", 
            width=400,
            autofocus=True
        )
        self.lang_field = ft.Dropdown(
            label="Язык", 
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
            label="Код", 
            multiline=True, 
            min_lines=5, 
            max_lines=15, 
            width=400, 
            text_style=ft.TextStyle(font_family="Consolas")
        )
        
        # Create dialog
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новый сниппет"),
            content=ft.Column(
                [self.title_field, self.lang_field, self.code_field], 
                height=400, 
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
        if not self.title_field.value or not self.code_field.value:
            # Show error message
            return
        self.on_submit(self.title_field.value, self.lang_field.value or "text", self.code_field.value)

    def _handle_cancel(self, e):
        """Handle cancel button click."""
        self.on_cancel()

    def open(self, page: ft.Page):
        """Open the dialog."""
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()

    def close(self, page: ft.Page):
        """Close the dialog."""
        self.dialog.open = False
        page.dialog = None
        page.update()

    def clear_fields(self):
        """Clear all form fields."""
        self.title_field.value = ""
        self.code_field.value = ""
        self.lang_field.value = "python"


class EditSnippetDialog:
    """Dialog for editing an existing snippet."""
    
    def __init__(self, on_submit: Callable[[int, str, str, str], None], on_cancel: Callable[[], None]):
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.snippet_id = None
        
        # Create form fields
        self.title_field = ft.TextField(
            label="Название (напр. Sort Array)", 
            width=400,
            autofocus=True
        )
        self.lang_field = ft.Dropdown(
            label="Язык", 
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
            label="Код", 
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
                [self.title_field, self.lang_field, self.code_field], 
                height=400, 
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
        if not self.title_field.value or not self.code_field.value:
            # Show error message
            return
        if self.snippet_id is not None:
            self.on_submit(self.snippet_id, self.title_field.value, self.lang_field.value or "text", self.code_field.value)

    def _handle_cancel(self, e):
        """Handle cancel button click."""
        self.on_cancel()

    def open(self, page: ft.Page, snippet_id: int, title: str, language: str, code: str):
        """Open the dialog with existing snippet data."""
        self.snippet_id = snippet_id
        self.title_field.value = title
        self.lang_field.value = language
        self.code_field.value = code
        
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()

    def close(self, page: ft.Page):
        """Close the dialog."""
        self.dialog.open = False
        page.dialog = None
        page.update()

    def clear_fields(self):
        """Clear all form fields."""
        self.title_field.value = ""
        self.code_field.value = ""
        self.lang_field.value = "python"
        self.snippet_id = None