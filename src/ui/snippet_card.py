# snippet_card.py
import flet as ft
from typing import Callable, Optional
import yaml


class SnippetCard(ft.Container):
    """A card component to display a code snippet with multi-cell content."""

    def __init__(
            self,
            snippet_id: int,
            title: str,
            language: str,
            cells: list,
            on_copy: Optional[Callable[[str], None]] = None,
            on_delete: Optional[Callable[[int], None]] = None,
            on_edit: Optional[Callable[[int, str, str, list], None]] = None,
            expand: bool = True,
            **kwargs
    ):
        super().__init__(**kwargs)

        self.snippet_id = snippet_id
        self.title = title
        self.language = language
        self.cells = cells
        self.on_copy = on_copy
        self.on_delete = on_delete
        self.on_edit = on_edit

        # Create the card content
        self.content = self._build_content()
        self.bgcolor = "#1E1E1E"  # Используем hex цвета вместо ft.colors
        self.padding = 15
        self.border_radius = 10
        self.expand = expand  # Убрали анимацию, чтобы избежать ошибок

    def _build_content(self) -> ft.Column:
        """Build the content of the snippet card with multiple cells."""
        # Header with title and language tag
        header = ft.Row(
            controls=[
                ft.Icon("code", color="#60A5FA"),  # Синий цвет в hex
                ft.Text(
                    self.title,
                    weight="bold",
                    size=16,
                    expand=True,
                    no_wrap=True
                ),
                ft.Container(
                    content=ft.Text(
                        self.language.upper(),
                        size=10,
                        color="white"
                    ),
                    bgcolor="#374151",  # Темно-серый в hex
                    padding=5,
                    border_radius=5
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Build cells content
        cells_controls = []

        for cell in self.cells:
            cell_type = cell.get("type", "code")

            if cell_type == "text":
                # Markdown text cell
                cells_controls.append(
                    ft.Container(
                        content=ft.Markdown(
                            cell.get("content", ""),
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            selectable=True
                        ),
                        padding=ft.padding.only(bottom=10)
                    )
                )
            elif cell_type == "code":
                # Code cell with syntax highlighting
                code_lang = cell.get("language", self.language)
                code_content = cell.get("content", "")
                md_code = f"```{code_lang}\n{code_content}\n```"

                cells_controls.append(
                    ft.Container(
                        content=ft.Markdown(
                            md_code,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            code_theme="atom-one-dark",
                            selectable=True
                        ),
                        padding=ft.padding.only(bottom=10),
                        bgcolor="#00000020",  # Полупрозрачный черный
                        border_radius=5
                    )
                )

        # Action buttons
        actions = ft.Row(
            controls=[
                ft.IconButton(
                    icon="edit",
                    tooltip="Редактировать",
                    on_click=lambda e: self._handle_edit()
                ) if self.on_edit else ft.Container(),
                ft.IconButton(
                    icon="content_copy",
                    tooltip="Копировать YAML",
                    on_click=lambda e: self._handle_copy()
                ),
                ft.IconButton(
                    icon="delete_outline",
                    icon_color="red",
                    tooltip="Удалить",
                    on_click=lambda e: self._handle_delete()
                )
            ],
            alignment=ft.MainAxisAlignment.END
        ) if self.on_copy or self.on_delete or self.on_edit else ft.Container()

        # Combine all controls
        return ft.Column(
            controls=[
                header,
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                        controls=cells_controls,
                        scroll=ft.ScrollMode.AUTO
                    ),
                    height=250,
                    expand=True
                ),
                ft.Divider(),
                actions
            ],
            spacing=10
        )

    def _handle_copy(self):
        """Handle copy button click - copy YAML content."""
        print(f"DEBUG: SnippetCard._handle_copy called for snippet {self.snippet_id}")
        if self.on_copy:
            print(f"DEBUG: Creating YAML content from {len(self.cells)} cells")
            yaml_content = yaml.dump(self.cells, allow_unicode=True)
            print(f"DEBUG: YAML content length: {len(yaml_content)}")
            self.on_copy(yaml_content)
        else:
            print(f"DEBUG: No on_copy callback defined for snippet {self.snippet_id}")

    def _handle_delete(self):
        """Handle delete button click."""
        print(f"DEBUG: SnippetCard._handle_delete called for snippet {self.snippet_id}")
        if self.on_delete:
            print(f"DEBUG: Calling delete callback for snippet {self.snippet_id}")
            self.on_delete(self.snippet_id)
        else:
            print(f"DEBUG: No on_delete callback defined for snippet {self.snippet_id}")

    def _handle_edit(self):
        """Handle edit button click."""
        print(f"DEBUG: SnippetCard._handle_edit called for snippet {self.snippet_id}")
        if self.on_edit:
            print(f"DEBUG: Calling edit callback for snippet {self.snippet_id}")
            self.on_edit(self.snippet_id, self.title, self.language, self.cells)
        else:
            print(f"DEBUG: No on_edit callback defined for snippet {self.snippet_id}")

    def update_content(self, title: str, language: str, cells: list):
        """Update the card content."""
        self.title = title
        self.language = language
        self.cells = cells

        # Rebuild content with new values
        self.content = self._build_content()
        self.update()