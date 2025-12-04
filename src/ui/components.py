import flet as ft
from flet import icons  # Импорт icons для исправления NameError
from typing import List, Dict, Any, Callable

class CellEditor(ft.UserControl):
    def __init__(self, cell_data: Dict[str, Any] = None, on_delete: Callable = None, on_change: Callable = None):
        super().__init__()
        self.cell_data = cell_data or {'type': 'text', 'content': ''}
        self.on_delete = on_delete
        self.on_change = on_change
        self.preview = ft.Container()
        self._build_components()

    def _build_components(self):
        self.type_dropdown = ft.Dropdown(
            value=self.cell_data['type'],
            options=[
                ft.dropdown.Option("text", "Текст"),
                ft.dropdown.Option("code", "Код"),
                ft.dropdown.Option("markdown", "Markdown"),
                ft.dropdown.Option("image", "Изображение"),
            ],
            on_change=self._on_type_change,
            width=120
        )

        if self.cell_data['type'] == 'code':
            self.language_dropdown = ft.Dropdown(
                value=self.cell_data.get('language', 'python'),
                options=[
                    ft.dropdown.Option("python", "Python"),
                    ft.dropdown.Option("javascript", "JavaScript"),
                    ft.dropdown.Option("html", "HTML"),
                    ft.dropdown.Option("css", "CSS"),
                    ft.dropdown.Option("sql", "SQL"),
                    ft.dropdown.Option("bash", "Bash"),
                    ft.dropdown.Option("dockerfile", "Dockerfile"),
                    ft.dropdown.Option("yaml", "YAML"),
                    ft.dropdown.Option("json", "JSON"),
                    ft.dropdown.Option("c++", "C++"),
                    ft.dropdown.Option("java", "Java"),
                ],
                width=150,
                on_change=self._update_preview
            )
            self.content_field = ft.TextField(
                value=self.cell_data['content'],
                multiline=True,
                min_lines=3,
                max_lines=10,
                expand=True,
                label="Код",
                on_change=self._update_preview
            )
        elif self.cell_data['type'] == 'markdown':
            self.content_field = ft.TextField(
                value=self.cell_data['content'],
                multiline=True,
                min_lines=3,
                max_lines=10,
                expand=True,
                label="Markdown",
                on_change=self._update_preview
            )
            self.language_dropdown = None
        elif self.cell_data['type'] == 'image':
            self.content_field = ft.TextField(
                value=self.cell_data['content'],
                expand=True,
                label="URL или путь к изображению",
                on_change=self._update_preview
            )
            self.language_dropdown = None
        else:
            self.content_field = ft.TextField(
                value=self.cell_data['content'],
                multiline=True,
                min_lines=2,
                max_lines=5,
                expand=True,
                label="Текст",
                on_change=self._update_preview
            )
            self.language_dropdown = None

        delete_btn = ft.IconButton(icons.DELETE, tooltip="Удалить ячейку", on_click=lambda e: self.on_delete(self))

        self.preview = self._build_preview()

        self.content = ft.Column([
            ft.Row([
                self.type_dropdown,
                self.language_dropdown if self.language_dropdown else ft.Container(),
                self.content_field,
                delete_btn
            ]),
            ft.Divider(),
            self.preview
        ])

    def _build_preview(self) -> ft.Container:
        ctype = self.cell_data['type']
        content = self.content_field.value if self.content_field else ""
        if ctype == 'code':
            lang = self.language_dropdown.value if self.language_dropdown else "python"
            md_code = f"```{lang}\n{content}\n```"
            return ft.Markdown(md_code, code_theme="atom-one-dark", selectable=True)
        elif ctype == 'markdown':
            return ft.Markdown(content, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB, selectable=True)
        elif ctype == 'image':
            return ft.Image(src=content, width=200, height=200, fit=ft.ImageFit.CONTAIN, error_content=ft.Text("Неверное изображение"))
        else:
            return ft.Text(content)
        return ft.Container()

    def _on_type_change(self, e):
        self.cell_data['type'] = e.control.value
        self._build_components()
        self.update()

    def _update_preview(self, e):
        self.preview = self._build_preview()
        if self.on_change:
            self.on_change()
        self.update()

    def get_cell_data(self) -> Dict[str, Any]:
        cell = {
            'type': self.type_dropdown.value,
            'content': self.content_field.value
        }
        if self.language_dropdown:
            cell['language'] = self.language_dropdown.value
        return cell

class SnippetEditor:
    def __init__(self, snippet: Dict = None, on_save: Callable = None, on_cancel: Callable = None):
        self.snippet = snippet or {'id': None, 'title': "", 'language': "python", 'cells': [], 'tags': ""}
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.cell_editors: List[CellEditor] = []
        self.cells_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self._build_components()

    def _build_components(self):
        print("DEBUG: Построение компонентов SnippetEditor")
        self.title_field = ft.TextField(value=self.snippet['title'], label="Название", width=400)
        self.language_dropdown = ft.Dropdown(
            value=self.snippet['language'],
            label="Основной язык",
            width=400,
            options=[
                ft.dropdown.Option("python", "Python"),
                ft.dropdown.Option("javascript", "JavaScript"),
                ft.dropdown.Option("html", "HTML"),
                ft.dropdown.Option("css", "CSS"),
                ft.dropdown.Option("sql", "SQL"),
                ft.dropdown.Option("bash", "Bash"),
                ft.dropdown.Option("dockerfile", "Dockerfile"),
                ft.dropdown.Option("yaml", "YAML"),
                ft.dropdown.Option("json", "JSON"),
                ft.dropdown.Option("c++", "C++"),
                ft.dropdown.Option("java", "Java"),
            ]
        )
        self.tags_field = ft.TextField(value=self.snippet['tags'], label="Теги (через запятую)", width=400)

        add_cell_btn = ft.ElevatedButton("Добавить ячейку", icon=icons.ADD, on_click=self._add_cell)

        save_btn = ft.ElevatedButton("Сохранить", on_click=self._on_save_click)
        cancel_btn = ft.TextButton("Назад", on_click=self._on_cancel_click)

        for cell in self.snippet['cells']:
            self._add_cell_editor(cell)

        self.content = ft.Column([
            ft.Text("Редактирование сниппета", size=20, weight=ft.FontWeight.BOLD),
            self.title_field,
            self.language_dropdown,
            self.tags_field,
            ft.Divider(),
            ft.Text("Ячейки содержимого:"),
            self.cells_list,
            ft.Row([add_cell_btn, save_btn, cancel_btn])
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    def _add_cell(self, e):
        print("DEBUG: Добавление новой ячейки")
        self._add_cell_editor({'type': 'text', 'content': ''})

    def _add_cell_editor(self, cell_data: Dict):
        print("DEBUG: Добавление редактора ячейки")
        editor = CellEditor(cell_data=cell_data, on_delete=self._remove_cell_editor, on_change=lambda: None)
        self.cell_editors.append(editor)
        self.cells_list.controls.append(editor)
        # Note: We can't call self.update() here since we're not a UserControl anymore
        # The caller will need to update the page

    def _remove_cell_editor(self, editor: 'CellEditor'):
        print("DEBUG: Удаление редактора ячейки")
        if editor in self.cell_editors:
            self.cell_editors.remove(editor)
            self.cells_list.controls.remove(editor)
            # Note: We can't call self.update() here since we're not a UserControl anymore
            # The caller will need to update the page

    def _on_save_click(self, e):
        print("DEBUG: Обработка сохранения в SnippetEditor")
        if self.on_save:
            self.on_save(self.get_snippet_data())

    def _on_cancel_click(self, e):
        print("DEBUG: Обработка отмены в SnippetEditor")
        if self.on_cancel:
            self.on_cancel()

    def get_snippet_data(self) -> Dict:
        cells = [editor.get_cell_data() for editor in self.cell_editors]
        return {
            'id': self.snippet['id'],
            'title': self.title_field.value,
            'language': self.language_dropdown.value,
            'cells': cells,
            'tags': self.tags_field.value
        }
    
    def build(self):
        """Return the content of the editor for display."""
        return self.content