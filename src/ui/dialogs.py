import flet as ft
from typing import Callable
from src.ui.code_editor import MultiCellEditor  # Предполагаю, что code_editor.py с MultiCellEditor существует

class AddSnippetDialog:
    def __init__(self, on_submit: Callable[[str, str, list, str], None], on_cancel: Callable[[], None]):
        print("DEBUG: Инициализация AddSnippetDialog")
        self.on_submit = on_submit
        self.on_cancel = on_cancel

        self.title_field = ft.TextField(label="Название", width=400, autofocus=True)
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
        self.tags_field = ft.TextField(label="Теги (через запятую)", width=400)
        self.cells = [{"type": "code", "content": ""}]  # Default with one empty code cell
        self.cells_editor = MultiCellEditor()  # Create MultiCellEditor instance

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Новый сниппет"),
            content=ft.Column([
                self.title_field,
                self.lang_field,
                self.tags_field,
                ft.Divider(),
                ft.Text("Ячейки кода:", weight=ft.FontWeight.BOLD),
                ft.Container(content=self.cells_editor.build(), height=300, expand=True),
            ], scroll=ft.ScrollMode.AUTO, width=600, height=600),
            actions=[
                ft.TextButton("Отмена", on_click=self._handle_cancel),
                ft.ElevatedButton("Сохранить", on_click=self._handle_submit),
            ]
        )

    def _handle_submit(self, e):
        print("DEBUG: Обработка submit в диалоге добавления")
        if not self.title_field.value:
            snack_bar = ft.SnackBar(ft.Text("Пожалуйста, введите название!"))
            e.page.show_snack_bar(snack_bar)
            return
        # Get updated cells from the editor
        updated_cells = self.cells_editor.get_cells()
        self.on_submit(self.title_field.value, self.lang_field.value or "python", updated_cells, self.tags_field.value)

    def _handle_cancel(self, e):
        print("DEBUG: Обработка cancel в диалоге добавления")
        self.on_cancel()

class EditSnippetDialog:
    def __init__(self, on_submit: Callable[[int, str, str, list, str], None], on_full_edit: Callable[[], None], on_cancel: Callable[[], None]):
        print("DEBUG: Инициализация EditSnippetDialog")
        self.on_submit = on_submit
        self.on_full_edit = on_full_edit
        self.on_cancel = on_cancel
        self.snippet_id = None
        self.cells = []
        self.cells_editor = MultiCellEditor()  # Мини-редактор для cells

        self.title_field = ft.TextField(label="Название", width=400)
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
        self.tags_field = ft.TextField(label="Теги", width=400)

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Быстрое редактирование"),
            content=ft.Column([
                self.title_field,
                self.lang_field,
                self.tags_field,
                ft.Divider(),
                ft.Text("Ячейки кода:", weight=ft.FontWeight.BOLD),
                ft.Container(content=self.cells_editor.build(), height=350, expand=True),
            ], scroll=ft.ScrollMode.AUTO, width=600, height=650),
            actions=[
                ft.TextButton("Отмена", on_click=self._handle_cancel),
                ft.ElevatedButton("Сохранить", on_click=self._handle_quick_save),
                ft.ElevatedButton("Редактировать полностью", on_click=self._handle_full_edit),
            ]
        )

    def open(self, page: ft.Page, snippet_id: int, title: str, language: str, cells: list, tags: str):
        print(f"DEBUG: Открытие диалога редактирования с тегами '{tags}'")
        self.snippet_id = snippet_id
        self.title_field.value = title
        self.lang_field.value = language
        self.tags_field.value = tags
        self.cells = cells
        self.cells_editor.load_cells(cells)  # Загружаем cells в мини-редактор
        page.dialog = self.dialog
        self.dialog.open = True
        page.update()

    def _handle_quick_save(self, e):
        print("DEBUG: Обработка quick save в диалоге редактирования")
        if not self.title_field.value:
            snack_bar = ft.SnackBar(ft.Text("Пожалуйста, введите название!"))
            e.page.show_snack_bar(snack_bar)
            return
        new_cells = self.cells_editor.get_cells()  # Получаем обновлённые cells
        self.on_submit(self.snippet_id, self.title_field.value, self.lang_field.value or "python", new_cells, self.tags_field.value)

    def _handle_full_edit(self, e):
        print("DEBUG: Обработка full edit в диалоге редактирования")
        self.on_full_edit()

    def _handle_cancel(self, e):
        print("DEBUG: Обработка cancel в диалоге редактирования")
        self.on_cancel()