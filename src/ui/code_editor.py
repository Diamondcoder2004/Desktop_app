import flet as ft
from typing import List, Dict, Optional


class MultiCellEditor(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.cells: List[ft.Container] = []
        self.cells_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.add_button = ft.ElevatedButton("Добавить ячейку", on_click=self.add_cell)
        self._pending_cells = None  # Отложенные данные

    def build(self):
        container = ft.Container(
            content=ft.Column([
                ft.Text("Ячейки:", weight=ft.FontWeight.BOLD),
                self.cells_column,
                self.add_button
            ]),
            padding=10,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=10,
            expand=True
        )

        # Загружаем отложенные данные при построении UI
        if self._pending_cells is not None:
            self._load_cells_internal(self._pending_cells)
            self._pending_cells = None
        elif not self.cells:
            self._add_cell_internal()

        return container

    def _add_cell_internal(self):
        cell_container = ft.Container(
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=5,
            margin=ft.margin.only(bottom=10)
        )

        dropdown = ft.Dropdown(
            value="code",
            options=[
                ft.dropdown.Option("code"),
                ft.dropdown.Option("text"),
                ft.dropdown.Option("markdown"),
            ],
            width=120
        )
        text_field = ft.TextField(
            label="Код / Текст",
            multiline=True,
            min_lines=3,
            expand=True
        )
        delete_button = ft.IconButton(
            icon=ft.icons.DELETE,
            icon_color="red",
            on_click=lambda _, c=cell_container: self.remove_cell(c)
        )

        cell_container.content = ft.Column([ft.Row([dropdown, text_field, delete_button])])
        self.cells.append(cell_container)
        self.cells_column.controls.append(cell_container)

    def add_cell(self, e):
        self._add_cell_internal()
        self.cells_column.update()

    def remove_cell(self, cell_container):
        if len(self.cells) > 1:
            self.cells.remove(cell_container)
            self.cells_column.controls.remove(cell_container)
            self.cells_column.update()

    def get_cells(self) -> List[Dict]:
        result = []
        for container in self.cells:
            row = container.content.controls[0]
            dropdown = row.controls[0]
            textfield = row.controls[1]
            result.append({
                "type": dropdown.value,
                "content": textfield.value or ""
            })
        return result

    def _load_cells_internal(self, cells: List[Dict]):
        self.cells_column.controls.clear()
        self.cells.clear()

        if not cells:
            self._add_cell_internal()
        else:
            for cell in cells:
                cell_type = cell.get("type", "code")
                content = cell.get("content", "")

                cell_container = ft.Container(
                    padding=10,
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=5,
                    margin=ft.margin.only(bottom=10)
                )

                dropdown = ft.Dropdown(
                    value=cell_type,
                    options=[
                        ft.dropdown.Option("code"),
                        ft.dropdown.Option("text"),
                        ft.dropdown.Option("markdown"),
                    ],
                    width=120
                )
                text_field = ft.TextField(
                    value=content,
                    multiline=True,
                    min_lines=3,
                    expand=True
                )
                delete_button = ft.IconButton(
                    icon=ft.icons.DELETE,
                    icon_color="red",
                    on_click=lambda _, c=cell_container: self.remove_cell(c)
                )

                cell_container.content = ft.Column([ft.Row([dropdown, text_field, delete_button])])
                self.cells.append(cell_container)
                self.cells_column.controls.append(cell_container)

    # code_editor.py — улучшите load_cells
    def load_cells(self, cells: List[Dict]):
        """Загружает ячейки. Если UI уже построен — обновляет немедленно."""
        self._pending_cells = cells
        # Всегда вызываем update — Flet корректно обработает,
        # даже если элемент ещё не добавлен на страницу.
        self.update()
        print(f"DEBUG: MultiCellEditor.load_cells вызван, ячеек={len(cells)}")