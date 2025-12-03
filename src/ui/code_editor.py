import flet as ft
from typing import Callable, Optional


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
    
    @property
    def content(self):
        """Получение текущего содержимого"""
        return self.text_field.value if self.text_field.value else ""


class MultiCellEditor:
    """
    Редактор для нескольких ячеек сниппета
    """
    
    def __init__(self, cells: list = None, on_change: Optional[Callable[[list], None]] = None):
        self.cells = cells or []
        self.on_change = on_change
        self.editors = []
        
        # Кнопка добавления новой ячейки
        self.add_cell_button = ft.ElevatedButton(
            "Добавить ячейку",
            icon=ft.icons.ADD_OUTLINED,
            on_click=self._add_cell
        )
        
        # Контейнер для ячеек
        self.cells_container = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        # Инициализация существующих ячеек
        self._init_cells()
    
    def _init_cells(self):
        """Инициализация существующих ячеек"""
        self.cells_container.controls.clear()
        self.editors.clear()
        
        for i, cell in enumerate(self.cells):
            cell_editor = self._create_cell_editor(i, cell)
            self.cells_container.controls.append(cell_editor)
            self.editors.append(cell_editor)
    
    def _create_cell_editor(self, index: int, cell: dict):
        """Создание редактора для одной ячейки"""
        cell_type = cell.get("type", "code")
        content = cell.get("content", "")
        language = cell.get("language", "python")
        
        # Выбор типа ячейки
        type_dropdown = ft.Dropdown(
            label="Тип ячейки",
            width=200,
            options=[
                ft.dropdown.Option("text", "Текст"),
                ft.dropdown.Option("code", "Код")
            ],
            value=cell_type,
            on_change=lambda e: self._update_cell_type(index, e.control.value)
        )
        
        # Язык программирования (для кода)
        lang_dropdown = ft.Dropdown(
            label="Язык",
            width=200,
            options=[
                ft.dropdown.Option("python", "Python"),
                ft.dropdown.Option("javascript", "JavaScript"),
                ft.dropdown.Option("sql", "SQL"),
                ft.dropdown.Option("html", "HTML"),
                ft.dropdown.Option("css", "CSS"),
                ft.dropdown.Option("c++", "C++"),
                ft.dropdown.Option("java", "Java"),
                ft.dropdown.Option("go", "Go"),
                ft.dropdown.Option("rust", "Rust"),
                ft.dropdown.Option("bash", "Bash"),
                ft.dropdown.Option("markdown", "Markdown"),
                ft.dropdown.Option("json", "JSON"),
                ft.dropdown.Option("yaml", "YAML"),
                ft.dropdown.Option("xml", "XML"),
            ],
            value=language,
            visible=(cell_type == "code"),
            on_change=lambda e: self._update_cell_language(index, e.control.value)
        )
        
        # Редактор содержимого
        code_editor = CodeEditor(
            label="Содержимое",
            value=content,
            language=language if cell_type == "code" else "markdown",
            on_change=lambda value: self._update_cell_content(index, value)
        )
        
        # Кнопка удаления ячейки
        delete_button = ft.IconButton(
            icon=ft.icons.DELETE_OUTLINE,
            tooltip="Удалить ячейку",
            on_click=lambda e: self._remove_cell(index),
            icon_color=ft.colors.RED
        )
        
        def toggle_lang_visibility(e):
            """Переключение видимости выпадающего списка языка"""
            lang_dropdown.visible = type_dropdown.value == "code"
            # Обновление страницы, если возможно
            if hasattr(e, 'page'):
                e.page.update()
        
        type_dropdown.on_change = toggle_lang_visibility
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([type_dropdown, lang_dropdown, delete_button]),
                    code_editor.build()
                ]),
                padding=10
            ),
            elevation=2
        )
    
    def _add_cell(self, e):
        """Добавление новой ячейки"""
        new_cell = {
            "type": "code",
            "language": "python",
            "content": ""
        }
        self.cells.append(new_cell)
        
        cell_editor = self._create_cell_editor(len(self.cells) - 1, new_cell)
        self.cells_container.controls.append(cell_editor)
        self.editors.append(cell_editor)
        
        if self.on_change:
            self.on_change(self.cells)
        
        # Обновление страницы, если возможно
        if hasattr(e, 'page'):
            e.page.update()
    
    def _remove_cell(self, index: int):
        """Удаление ячейки"""
        if 0 <= index < len(self.cells):
            self.cells.pop(index)
            self.cells_container.controls.pop(index)
            self.editors.pop(index)
            
            # Переиндексация оставшихся редакторов
            for i, editor in enumerate(self.editors):
                # Нужно пересоздать редакторы с правильными индексами
                pass
            
            if self.on_change:
                self.on_change(self.cells)
            
            # Обновление страницы, если возможно
            if hasattr(self, 'page'):
                self.page.update()
    
    def _update_cell_type(self, index: int, cell_type: str):
        """Обновление типа ячейки"""
        if 0 <= index < len(self.cells):
            self.cells[index]["type"] = cell_type
            if self.on_change:
                self.on_change(self.cells)
    
    def _update_cell_language(self, index: int, language: str):
        """Обновление языка ячейки"""
        if 0 <= index < len(self.cells):
            self.cells[index]["language"] = language
            if self.on_change:
                self.on_change(self.cells)
    
    def _update_cell_content(self, index: int, content: str):
        """Обновление содержимого ячейки"""
        if 0 <= index < len(self.cells):
            self.cells[index]["content"] = content
            if self.on_change:
                self.on_change(self.cells)
    
    def build(self):
        """Создание UI компонента"""
        return ft.Column([
            ft.Row([self.add_cell_button], alignment=ft.MainAxisAlignment.END),
            self.cells_container
        ], expand=True)
    
    def update_cells(self, cells: list):
        """Обновление всех ячеек"""
        self.cells = cells or []
        self._init_cells()
        # Обновление страницы, если возможно
        if hasattr(self, 'page'):
            self.page.update()