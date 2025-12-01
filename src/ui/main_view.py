import flet as ft
from src.models.database import Database
from src.snippet_card import SnippetCard
from src.dialogs import AddSnippetDialog, EditSnippetDialog
import pyperclip


class MainView(ft.Column):
    """Main view of the application."""

    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.expand = True

        # Search field
        self.search_field = ft.TextField(
            label="Поиск по названию или языку",
            prefix_icon=ft.icons.SEARCH,
            on_change=self._handle_search,
            expand=True
        )

        # Snippets grid
        self.snippets_grid = ft.GridView(
            expand=1,
            runs_count=2,
            max_extent=500,
            child_aspect_ratio=1.5,
            spacing=20,
            run_spacing=20,
        )

        # Build the UI
        self._build_ui()

        # Load snippets
        self._load_snippets()

    def _build_ui(self):
        """Build the user interface."""
        self.controls = [
            ft.Row(
                controls=[
                    self.search_field,
                    ft.ElevatedButton(
                        "Добавить сниппет",
                        icon=ft.icons.ADD,
                        on_click=self._handle_add_snippet
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            ft.Divider(),
            ft.Container(
                content=self.snippets_grid,
                expand=True
            )
        ]

    def _load_snippets(self, search_query: str = ""):
        """Load snippets from database."""
        self.snippets_grid.controls.clear()

        snippets = self.db.get_snippets(search_query)
        for snippet in snippets:
            snippet_id, title, language, code = snippet
            card = SnippetCard(
                snippet_id=snippet_id,
                title=title,
                language=language,
                code=code,
                on_copy=self._handle_copy,
                on_delete=self._handle_delete,
                on_edit=self._handle_edit
            )
            self.snippets_grid.controls.append(card)

        self.update()

    def _handle_search(self, e):
        """Handle search field changes."""
        self._load_snippets(e.control.value)

    def _handle_add_snippet(self, e):
        """Handle add snippet button click."""

        def on_submit(title: str, language: str, code: str):
            self.db.add_snippet(title, language, code)
            dialog.close(self.page)
            self._load_snippets()

        def on_cancel():
            dialog.close(self.page)

        dialog = AddSnippetDialog(on_submit=on_submit, on_cancel=on_cancel)
        dialog.open(self.page)

    def _handle_copy(self, code: str):
        """Handle copy button click."""
        pyperclip.copy(code)
        self.page.snack_bar = ft.SnackBar(ft.Text("Код скопирован в буфер обмена!"))
        self.page.snack_bar.open = True
        self.page.update()

    def _handle_delete(self, snippet_id: int):
        """Handle delete button click."""

        def on_confirm():
            self.db.delete_snippet(snippet_id)
            dialog.open = False
            self.page.dialog = None
            self.page.update()
            self._load_snippets(self.search_field.value)

        def on_cancel():
            dialog.open = False
            self.page.dialog = None
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Удалить сниппет?"),
            content=ft.Text("Вы уверены, что хотите удалить этот сниппет? Это действие нельзя отменить."),
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: on_cancel()),
                ft.TextButton("Удалить", on_click=lambda e: on_confirm(), style=ft.ButtonStyle(color="red")),
            ],
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _handle_edit(self, snippet_id: int, title: str, language: str, code: str):
        """Handle edit button click."""

        def on_submit(s_id: int, new_title: str, new_language: str, new_code: str):
            self.db.update_snippet(s_id, new_title, new_language, new_code)
            dialog.close(self.page)
            self._load_snippets(self.search_field.value)

        def on_cancel():
            dialog.close(self.page)

        dialog = EditSnippetDialog(on_submit=on_submit, on_cancel=on_cancel)
        dialog.open(self.page, snippet_id, title, language, code)