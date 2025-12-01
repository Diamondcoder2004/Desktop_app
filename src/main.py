import flet as ft
from src.database import Database
from src.snippet_card import SnippetCard
from src.dialogs import AddSnippetDialog, EditSnippetDialog
import pyperclip


def main(page: ft.Page):
    # Page setup
    page.title = "CodeSnippet Hub"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 800
    page.padding = 20

    # Initialize database
    db = Database()

    # Search field
    search_field = ft.TextField(
        label="Поиск по названию или языку",
        prefix_icon=ft.icons.SEARCH,
        expand=True
    )

    # Snippets grid
    snippets_grid = ft.GridView(
        expand=1,
        runs_count=2,
        max_extent=500,
        child_aspect_ratio=1.5,
        spacing=20,
        run_spacing=20,
    )

    # Functions
    def load_snippets(search_query: str = ""):
        """Load snippets from database."""
        snippets_grid.controls.clear()

        snippets = db.get_snippets(search_query)
        for snippet in snippets:
            snippet_id, title, language, code = snippet
            card = SnippetCard(
                snippet_id=snippet_id,
                title=title,
                language=language,
                code=code,
                on_copy=handle_copy,
                on_delete=handle_delete,
                on_edit=handle_edit
            )
            snippets_grid.controls.append(card)

        page.update()

    def handle_search(e):
        """Handle search field changes."""
        load_snippets(search_field.value)

    def handle_add_snippet(e):
        """Handle add snippet button click."""

        def on_submit(title: str, language: str, code: str):
            db.add_snippet(title, language, code)
            dialog.close(page)
            load_snippets(search_field.value)

        def on_cancel():
            dialog.close(page)

        dialog = AddSnippetDialog(on_submit=on_submit, on_cancel=on_cancel)
        dialog.open(page)

    def handle_copy(code: str):
        """Handle copy button click."""
        pyperclip.copy(code)
        page.snack_bar = ft.SnackBar(ft.Text("Код скопирован в буфер обмена!"))
        page.snack_bar.open = True
        page.update()

    def handle_delete(snippet_id: int):
        """Handle delete button click."""

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
                ft.TextButton("Удалить", on_click=lambda e: on_confirm(), style=ft.ButtonStyle(color="red")),
            ],
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    def handle_edit(snippet_id: int, title: str, language: str, code: str):
        """Handle edit button click."""

        def on_submit(s_id: int, new_title: str, new_language: str, new_code: str):
            db.update_snippet(s_id, new_title, new_language, new_code)
            dialog.close(page)
            load_snippets(search_field.value)

        def on_cancel():
            dialog.close(page)

        dialog = EditSnippetDialog(on_submit=on_submit, on_cancel=on_cancel)
        dialog.open(page, snippet_id, title, language, code)

    # Connect search field
    search_field.on_change = handle_search

    # Create layout
    page.add(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        search_field,
                        ft.ElevatedButton(
                            "Добавить сниппет",
                            icon=ft.icons.ADD,
                            on_click=handle_add_snippet
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


if __name__ == "__main__":
    ft.app(target=main)