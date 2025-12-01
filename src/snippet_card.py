import flet as ft
from typing import Callable, Optional


class SnippetCard(ft.Container):
    """A card component to display a code snippet with syntax highlighting."""
    
    def __init__(
        self,
        snippet_id: int,
        title: str,
        language: str,
        code: str,
        on_copy: Optional[Callable[[str], None]] = None,
        on_delete: Optional[Callable[[int], None]] = None,
        on_edit: Optional[Callable[[int, str, str, str], None]] = None,
        expand: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)
        
        self.snippet_id = snippet_id
        self.title = title
        self.language = language
        self.code = code
        self.on_copy = on_copy
        self.on_delete = on_delete
        self.on_edit = on_edit
        
        # Create the card content
        self.content = self._build_content()
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.padding = 15
        self.border_radius = 10
        self.animate_scale = ft.animation.Animation(300, ft.AnimationCurve.BOUNCE_OUT)
        self.expand = expand

    def _build_content(self) -> ft.Column:
        """Build the content of the snippet card."""
        # Format code for Markdown with syntax highlighting
        md_code = f"```{self.language}\n{self.code}\n```"

        return ft.Column(
            controls=[
                # Header with title and language tag
                ft.Row(
                    controls=[
                        ft.Icon(ft.icons.CODE, color=ft.colors.BLUE_400),
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
                            bgcolor=ft.colors.BLUE_GREY_700,
                            padding=5,
                            border_radius=5
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                
                ft.Divider(),
                
                # Code display area with scroll
                ft.Container(
                    content=ft.Markdown(
                        md_code,
                        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        code_theme="atom-one-dark",
                        selectable=True
                    ),
                    expand=True,
                    alignment=ft.alignment.top_left,
                    height=200  # Fixed height for consistent card sizing
                ),

                ft.Divider(),

                # Action buttons
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            tooltip="Редактировать",
                            on_click=lambda e: self._handle_edit()
                        ) if self.on_edit else ft.Container(),
                        ft.IconButton(
                            icon=ft.icons.COPY,
                            tooltip="Копировать код",
                            on_click=lambda e: self._handle_copy()
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            icon_color="red",
                            tooltip="Удалить",
                            on_click=lambda e: self._handle_delete()
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END
                ) if self.on_copy or self.on_delete or self.on_edit else ft.Container()
            ]
        )

    def _handle_copy(self):
        """Handle copy button click."""
        if self.on_copy:
            self.on_copy(self.code)

    def _handle_delete(self):
        """Handle delete button click."""
        if self.on_delete:
            self.on_delete(self.snippet_id)

    def _handle_edit(self):
        """Handle edit button click."""
        if self.on_edit:
            self.on_edit(self.snippet_id, self.title, self.language, self.code)

    def update_content(self, title: str, language: str, code: str):
        """Update the card content."""
        self.title = title
        self.language = language
        self.code = code
        
        # Rebuild content with new values
        self.content = self._build_content()