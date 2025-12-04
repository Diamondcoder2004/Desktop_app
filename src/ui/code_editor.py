import flet as ft
from typing import List, Dict, Callable, Optional

class CodeEditor:
    """
    Улучшенный редактор кода с подсветкой синтаксиса
    """

    def __init__(
        self,
        label: str = "Содержимое ячейки",
        value: str = "",
        language: str = "python",
        on_change: Optional[Callable[[str], None]] = None
    ):
        self.label = label
        self.value = value
        self.language = language
        self.on_change = on_change
        self._multiline = True
        self._min_lines = 10
        self._max_lines = 20

        # Создаем текстовое поле для ввода
        self.text_field = ft.TextField(
            label=label,
            value=value,
            multiline=self._multiline,
            min_lines=self._min_lines,
            max_lines=self._max_lines,
            expand=True,
            text_style=ft.TextStyle(font_family="Consolas"),
            on_change=self._handle_text_change
        )

        # Создаем Text элемент для просмотра (без подсветки синтаксиса)
        self.code_view = ft.Text(
            value=value,
            selectable=True,
            font_family="Consolas",
            style=ft.TextStyle(font_family="Consolas")
        )

        # Переключатель между редактором и просмотров
        self.view_mode = "edit"  # "edit" или "preview"

    def _handle_text_change(self, e):
        """Обработка изменения текста"""
        self.value = e.control.value
        if self.on_change:
            self.on_change(self.value)

    def build(self):
        """Создание UI компонента"""
        # Кнопки переключения режима
        self.toggle_button = ft.IconButton(
            icon=ft.icons.CODE_OUTLINED,
            tooltip="Режим редактирования",
            on_click=self._toggle_view_mode
        )

        # Основной контейнер
        self.editor_container = ft.Container(
            content=self.text_field,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=5,
            expand=True
        )

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(self.label, style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
                        self.toggle_button
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                self.editor_container
            ],
            expand=True
        )

    def _toggle_view_mode(self, e):
        """Переключение между режимами редактирования и просмотра"""
        if self.view_mode == "edit":
            # Переключаемся в режим просмотра
            self.code_view.value = self.text_field.value
            self.editor_container.content = self.code_view
            self.toggle_button.icon = ft.icons.EDIT_OUTLINED
            self.toggle_button.tooltip = "Режим редактирования"
            self.view_mode = "preview"
        else:
            # Переключаемся в режим редактирования
            self.editor_container.content = self.text_field
            self.toggle_button.icon = ft.icons.CODE_OUTLINED
            self.toggle_button.tooltip = "Режим просмотра"
            self.view_mode = "edit"

        # Обновление страницы, если возможно
        if hasattr(e, 'page'):
            e.page.update()

    def update_content(self, content: str, language: str = None):
        """Обновление содержимого редактора"""
        self.text_field.value = content
        self.value = content
        if language:
            self.language = language
        # Обновление страницы, если возможно
        if hasattr(self, 'page'):
            self.page.update()

    def get_cells(self) -> List[Dict]:
        """Возвращает список ячеек."""
        print("Ошибка в get_cells 100%")
        return self.cells

    @property
    def content(self):
        """Получение текущего содержимого"""
        return self.text_field.value if self.text_field.value else ""


from typing import List, Dict, Callable, Optional


class MultiCellEditor:
    """Редактор для нескольких ячеек кода."""

    def __init__(self, cells: Optional[List[Dict]] = None, on_change: Optional[Callable] = None):
        self.cells = cells or []
        self.on_change = on_change
        self.cell_widgets = []
        self.column = None  # Will be initialized in build()

    def build(self):
        """Build the control."""
        self.column = ft.Column()

        # Инициализация колонки с ячейками
        self.column.controls = []
        for cell in self.cells:
            self._add_cell_to_column(cell)

        # Кнопка добавления новой ячейки
        self.column.controls.append(
            ft.ElevatedButton(
                "Добавить ячейку",
                icon=ft.icons.ADD_OUTLINED,
                on_click=self._add_cell,
            )
        )

        return self.column

    def _add_cell_to_column(self, cell: Dict):
        """Добавляет ячейку в колонку."""
        cell_type = cell.get('type', 'code')
        content = cell.get('content', '')

        # Создаем виджет ячейки
        text_field = ft.TextField(
            value=content,
            multiline=True,
            min_lines=3,
            max_lines=10,
            expand=True,
        )

        # Сохраняем ссылку на поле ввода для обновления
        def on_text_change(e):
            idx = next(i for i, c in enumerate(self.cell_widgets) if c['text_field'] == e.control)
            if 0 <= idx < len(self.cells):
                self.cells[idx]['content'] = e.control.value
                if self.on_change:
                    self.on_change(self.cells)

        text_field.on_change = on_text_change

        cell_widget = ft.Container(
            content=ft.Column([
                ft.Text("Код:" if cell_type == 'code' else "Markdown:",
                        size=14, weight=ft.FontWeight.BOLD),
                text_field
            ]),
            padding=10,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            margin=ft.margin.only(bottom=10),
        )

        # Кнопка удаления ячейки
        delete_button = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            icon_color=ft.colors.ERROR,
            tooltip="Удалить ячейку",
        )

        def on_delete_click(e, idx=len(self.cell_widgets)):
            self._remove_cell(idx)

        delete_button.on_click = on_delete_click

        cell_container = ft.Row(
            controls=[
                ft.Container(content=cell_widget, expand=True),
                delete_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        # Вставляем перед кнопкой "Добавить ячейку"
        self.column.controls.insert(len(self.column.controls) - 1, cell_container)
        self.cell_widgets.append({
            'container': cell_container,
            'text_field': text_field,
            'type': cell_type,
            'content': content
        })

    def _add_cell(self, e):
        """Добавляет новую ячейку."""
        new_cell = {'type': 'code', 'content': ''}
        self.cells.append(new_cell)
        self._add_cell_to_column(new_cell)

        if self.on_change:
            self.on_change(self.cells)

    def _remove_cell(self, index: int):
        """Удаляет ячейку по индексу."""
        if 0 <= index < len(self.cells):
            # Удаляем из списков
            self.cells.pop(index)

            # Удаляем виджет из column.controls
            # (минус 1 для учета кнопки добавления в конце)
            if index < len(self.column.controls) - 1:
                self.column.controls.pop(index)

            # Обновляем cell_widgets
            self.cell_widgets.pop(index)

            # Обновляем индексы для оставшихся кнопок удаления
            for i, cell_data in enumerate(self.cell_widgets):
                # Создаем новую функцию с правильным индексом
                def make_delete_handler(idx):
                    return lambda e: self._remove_cell(idx)

                # Находим кнопку удаления в контейнере
                delete_btn = cell_data['container'].controls[1]  # 0 - content, 1 - delete button
                delete_btn.on_click = make_delete_handler(i)

            if self.on_change:
                self.on_change(self.cells)

    def get_cells(self) -> List[Dict]:
        """Возвращает список ячеек."""
        return self.cells

    def load_cells(self, cells: List[Dict]):
        """Загружает ячейки в редактор."""
        self.cells = cells.copy()  # Создаем копию
        self.cell_widgets = []

        # Очищаем текущие контролы
        if self.column:
            self.column.controls.clear()

        # Добавляем все ячейки
        for cell in self.cells:
            self._add_cell_to_column(cell)

        # Добавляем кнопку добавления
        if self.column:
            self.column.controls.append(
                ft.ElevatedButton(
                    "Добавить ячейку",
                    icon=ft.icons.ADD_OUTLINED,
                    on_click=self._add_cell,
                )
            )