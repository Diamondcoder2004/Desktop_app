import flet as ft
import pyperclip
from typing import List
from src.models.database import Database, Snippet
from src.ui.components import SnippetEditor


class MainView(ft.Control):
    """Main application view"""
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.snippets_grid = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=350,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
        )
        self.search_field = None
        self.edit_dialog = None

    def load_snippets(self, search_query: str = ""):
        """Load and display snippets from database"""
        self.snippets_grid.controls.clear()
        snippets = self.db.get_snippets(search_query)

        if not snippets:
            self.snippets_grid.controls.append(
                ft.Text("Сниппетов пока нет. Добавьте первый!", size=16, color=ft.colors.GREY_500)
            )
        else:
            for snippet in snippets:
                self.snippets_grid.controls.append(self._create_snippet_card(snippet))
        
        self.update()

    def _create_snippet_card(self, snippet: Snippet):
        """Create a card for a single snippet"""
        # Build content markdown from cells
        content_parts = []
        for cell in snippet.cells:
            if cell['type'] == 'code':
                lang = cell.get('language', 'text')
                content_parts.append(f"```{lang}\n{cell['content']}\n```")
            elif cell['type'] == 'text':
                content_parts.append(cell['content'])
            elif cell['type'] == 'image':
                content_parts.append(f"![Image]({cell['content']})")
        
        full_content = "\n".join(content_parts)
        
        # Create the card
        card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.CODE, color=ft.colors.BLUE_400),
                    ft.Text(snippet.title, weight="bold", size=16, expand=True, no_wrap=True),
                    ft.Container(
                        content=ft.Text(snippet.language.upper(), size=10, color="white"),
                        bgcolor=ft.colors.BLUE_GREY_700,
                        padding=5,
                        border_radius=5
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Divider(),
                
                # Content area with scrolling
                ft.Container(
                    content=ft.Markdown(
                        full_content,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        code_theme="atom-one-dark",
                        selectable=True,
                    ),
                    height=150,
                    alignment=ft.alignment.top_left,
                ),

                ft.Divider(),

                # Action buttons
                ft.Row([
                    ft.IconButton(
                        icon=ft.icons.EDIT,
                        tooltip="Редактировать",
                        on_click=lambda e, s=snippet: self._edit_snippet(s)
                    ),
                    ft.IconButton(
                        icon=ft.icons.COPY,
                        tooltip="Копировать код",
                        on_click=lambda e, s=snippet: self._copy_snippet_code(s)
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE_OUTLINE,
                        icon_color="red",
                        tooltip="Удалить",
                        on_click=lambda e, id=snippet.id: self._delete_snippet(id)
                    )
                ], alignment=ft.MainAxisAlignment.END)
            ]),
            bgcolor=ft.colors.SURFACE_VARIANT,
            padding=15,
            border_radius=10,
            animate_scale=ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT)
        )
        
        return card

    def _add_snippet(self, e):
        """Open dialog to add a new snippet"""
        snippet = Snippet(id=None, title="", language="python", cells=[])
        self._open_edit_dialog(snippet, is_new=True)

    def _edit_snippet(self, snippet: Snippet):
        """Open dialog to edit an existing snippet"""
        self._open_edit_dialog(snippet, is_new=False)

    def _open_edit_dialog(self, snippet: Snippet, is_new: bool):
        """Open the snippet editor dialog"""
        def save_snippet(updated_snippet: Snippet):
            if is_new:
                self.db.add_snippet(updated_snippet)
            else:
                self.db.update_snippet(updated_snippet)
            self.edit_dialog.open = False
            self.load_snippets(self.search_field.value)
            self.page.update()

        def cancel_edit():
            self.edit_dialog.open = False
            self.page.update()

        self.edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Редактирование сниппета"),
            content=SnippetEditor(snippet=snippet, on_save=save_snippet, on_cancel=cancel_edit),
            actions=[],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = self.edit_dialog
        self.edit_dialog.open = True
        self.page.update()

    def _copy_snippet_code(self, snippet: Snippet):
        """Copy all code cells from the snippet to clipboard"""
        code_parts = []
        for cell in snippet.cells:
            if cell['type'] == 'code':
                code_parts.append(cell['content'])
        
        if code_parts:
            full_code = "\n\n".join(code_parts)
            pyperclip.copy(full_code)
            self.page.snack_bar = ft.SnackBar(ft.Text("Код скопирован в буфер!"))
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("В сниппете нет кода для копирования"))
        
        self.page.snack_bar.open = True
        self.page.update()

    def _delete_snippet(self, snippet_id: int):
        """Delete a snippet after confirmation"""
        def confirm_delete(e):
            self.db.delete_snippet(snippet_id)
            delete_dialog.open = False
            self.load_snippets(self.search_field.value)
            self.page.update()

        def cancel_delete(e):
            delete_dialog.open = False
            self.page.update()

        delete_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтверждение удаления"),
            content=ft.Text("Вы уверены, что хотите удалить этот сниппет?"),
            actions=[
                ft.TextButton("Отмена", on_click=cancel_delete),
                ft.TextButton("Удалить", on_click=confirm_delete, style=ft.ButtonStyle(color="red")),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = delete_dialog
        delete_dialog.open = True
        self.page.update()

    def build(self):
        """Build the main UI"""
        self.search_field = ft.TextField(
            hint_text="Поиск по названию или тегам...",
            prefix_icon=ft.icons.SEARCH,
            on_change=lambda e: self.load_snippets(e.control.value),
            expand=True
        )
        
        header = ft.Row([
            ft.Icon(ft.icons.CODE, size=30, color="amber"),
            ft.Text("CodeSnippet Hub", size=24, weight="bold"),
            ft.VerticalDivider(width=20),
            self.search_field,
            ft.FloatingActionButton(
                icon=ft.icons.ADD, 
                text="Добавить", 
                on_click=self._add_snippet
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

        # Load initial snippets
        self.load_snippets()

        return ft.Column([
            header,
            ft.Divider(),
            self.snippets_grid
        ])