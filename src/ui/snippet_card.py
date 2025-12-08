import flet as ft
from typing import Callable, Optional, List, Dict
import yaml


class SnippetCard(ft.Container):
    """A card component to display a code snippet with multi-cell content."""

    def __init__(
        self,
        snippet_id: int,
        title: str,
        language: str,
        cells: List[Dict[str, str]],
        tags: str = "",
        on_copy: Optional[Callable[[str], None]] = None,
        on_delete: Optional[Callable[[int], None]] = None,
        on_edit: Optional[Callable[[int, str, str, List[Dict[str, str]]], None]] = None,
        on_study: Optional[Callable[[int, str, str, List[Dict[str, str]], str], None]] = None,
        expand: bool = False,
        **kwargs
    ):
        self.snippet_id = snippet_id
        self.title = title
        self.language = language
        self.cells = cells
        self.tags = tags

        self.on_copy = on_copy
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.on_study = on_study

        # Build card content
        content = self._build_content()

        super().__init__(
            content=content,
            bgcolor="#1E1E1E",
            padding=15,
            border_radius=10,
            expand=expand,
            **kwargs
        )

    def _build_content(self) -> ft.Column:
        header = ft.Row(
            controls=[
                ft.Icon("code", color="#60A5FA"),
                ft.Text(self.title, weight="bold", size=16, expand=True, no_wrap=True),
                ft.Container(
                    content=ft.Text(self.language.upper(), size=10, color="white"),
                    bgcolor="#374151",
                    padding=5,
                    border_radius=5,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # Рендерим ячейки
        cells_controls = []
        for cell in self.cells:
            cell_type = cell.get("type", "code")
            content = cell.get("content", "")
            if cell_type in ("markdown", "text"):
                cells_controls.append(
                    ft.Container(
                        content=ft.Markdown(
                            content,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            selectable=True,
                        ),
                        padding=ft.padding.only(bottom=10),
                    )
                )
            elif cell_type == "code":
                code_block = f"```{self.language}\n{content}\n```"
                cells_controls.append(
                    ft.Container(
                        content=ft.Markdown(
                            code_block,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                            code_theme="atom-one-dark",
                            selectable=True,
                        ),
                        padding=ft.padding.only(bottom=10),
                        bgcolor="#00000020",
                        border_radius=5,
                    )
                )

        # === КЛЮЧЕВОЕ ИЗМЕНЕНИЕ: Контейнер с прокруткой + фиксированные кнопки снизу ===
        scrollable_content = ft.Container(
            content=ft.ListView(
                controls=cells_controls,
                expand=True,
                auto_scroll=False,
            ),
            expand=True,  # займёт всё доступное пространство между хедером и кнопками
            padding=ft.padding.only(bottom=10),
        )

        # Кнопки действий (всегда видны)
        action_buttons = []
        if self.on_edit:
            action_buttons.append(ft.IconButton(icon="edit", tooltip="Редактировать", on_click=self._handle_edit))
        if self.on_copy:
            action_buttons.append(
                ft.IconButton(icon="content_copy", tooltip="Копировать YAML", on_click=self._handle_copy))
        if self.on_delete:
            action_buttons.append(
                ft.IconButton(icon="delete_outline", icon_color="red", tooltip="Удалить", on_click=self._handle_delete))
        if self.on_study:
            action_buttons.append(
                ft.IconButton(icon=ft.icons.SCHOOL, tooltip="Изучить с AI", on_click=self._handle_study))

        actions = ft.Row(
            controls=action_buttons,
            alignment=ft.MainAxisAlignment.END,
        ) if action_buttons else ft.Container()

        return ft.Column(
            controls=[
                header,
                ft.Divider(),
                scrollable_content,  # ← прокручиваемая область
                ft.Divider(),
                actions,  # ← кнопки всегда снизу и видны
            ],
            spacing=10,
            expand=True  # ← карточка может растягиваться
        )

    def _handle_copy(self, e):
        if self.on_copy:
            yaml_content = yaml.dump(self.cells, allow_unicode=True)
            self.on_copy(yaml_content)

    def _handle_delete(self, e):
        if self.on_delete:
            self.on_delete(self.snippet_id)

    def _handle_edit(self, e):
        if self.on_edit:
            self.on_edit(self.snippet_id, self.title, self.language, self.cells)

    def _handle_study(self, e):
        if self.on_study:
            self.on_study(self.snippet_id, self.title, self.language, self.cells, self.tags)

    def update_content(self, title: str, language: str, cells: list):
        """Update card content and refresh UI."""
        self.title = title
        self.language = language
        self.cells = cells
        self.content = self._build_content()
        self.update()