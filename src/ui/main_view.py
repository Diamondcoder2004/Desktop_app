import flet as ft
from src.models.database import Database
from src.ui.snippet_card import SnippetCard
from src.ui.dialogs import AddSnippetDialog, EditSnippetDialog
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

        self._build_ui()
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
            card = SnippetCard(
                snippet_id=snippet["id"],
                title=snippet["title"],
                language=snippet["language"],
                cells=snippet["cells"],
                on_copy=self._handle_copy,
                on_delete=self._handle_delete,
                on_edit=self._handle_edit
            )
            self.snippets_grid.controls.append(card)
        self.update()

    def _handle_search(self, e):
        self._load_snippets(e.control.value)

    def _handle_add_snippet(self, e):
        """Open dialog to add a new snippet."""

        def on_submit(title: str, language: str, cells: list, tags: str):
            self.db.add_snippet(title, language, cells, tags)
            dialog.close()
            self._load_snippets()

        def on_cancel():
            dialog.close()

        # Передаём page в диалог
        dialog = AddSnippetDialog(
            on_submit=on_submit,
            on_cancel=on_cancel,
            page=self.page
        )
        dialog.open()  # page уже внутри dialog

    def _handle_copy(self, code: str):
        pyperclip.copy(code)
        self.page.snack_bar = ft.SnackBar(ft.Text("Код скопирован в буфер обмена!"))
        self.page.snack_bar.open = True
        self.page.update()

    def _handle_delete(self, snippet_id: int):
        def on_confirm():
            self.db.delete_snippet(snippet_id)
            self.page.dialog = None
            self.page.update()
            self._load_snippets(self.search_field.value)

        def on_cancel():
            self.page.dialog = None
            self.page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Удалить сниппет?"),
            content=ft.Text("Вы уверены, что хотите удалить этот сниппет? Это действие нельзя отменить."),
            actions=[
                ft.TextButton("Отмена", on_click=lambda _: on_cancel()),
                ft.TextButton("Удалить", on_click=lambda _: on_confirm(), style=ft.ButtonStyle(color=ft.colors.RED)),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _handle_edit(self, snippet_id: int, title: str, language: str, cells: list):
        """Open dialog to edit an existing snippet."""

        def on_submit(s_id: int, new_title: str, new_language: str, new_cells: list, tags: str):
            self.db.update_snippet(s_id, new_title, new_language, new_cells, tags)
            dialog.close()
            self._load_snippets(self.search_field.value)

        def on_cancel():
            dialog.close()

        dialog = EditSnippetDialog(
            on_submit=on_submit,
            on_cancel=on_cancel,
            page=self.page
        )
        dialog.open(snippet_id, title, language, cells)  # page уже внутри