import flet as ft
from typing import List, Dict, Any, Callable
from src.models.database import Snippet


class CellEditor(ft.Control):
    """A component for editing a single content cell (code, text, or image)"""
    
    def __init__(self, cell_data: Dict[str, Any] = None, on_delete=None):
        super().__init__()
        self.cell_data = cell_data or {'type': 'text', 'content': ''}
        self.on_delete = on_delete
        self.content_field = None
        self.language_dropdown = None
        self.type_dropdown = None
        self._build_components()

    def _build_components(self):
        """Build the UI components for the cell editor"""
        # Type selection dropdown
        self.type_dropdown = ft.Dropdown(
            value=self.cell_data['type'],
            options=[
                ft.dropdown.Option("text", "Текст"),
                ft.dropdown.Option("code", "Код"),
                ft.dropdown.Option("image", "Изображение"),
            ],
            on_change=self._on_type_change,
            width=120
        )
        
        # Content field based on type
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
                width=150
            )
            self.content_field = ft.TextField(
                value=self.cell_data['content'],
                multiline=True,
                min_lines=3,
                max_lines=10,
                expand=True,
                label="Код"
            )
        elif self.cell_data['type'] == 'image':
            self.content_field = ft.TextField(
                value=self.cell_data['content'],
                expand=True,
                label="Ссылка на изображение или путь к файлу"
            )
        else:  # text
            self.content_field = ft.TextField(
                value=self.cell_data['content'],
                multiline=True,
                min_lines=2,
                max_lines=5,
                expand=True,
                label="Текст"
            )
        
        # Delete button
        delete_btn = ft.IconButton(
            icon=ft.icons.DELETE,
            tooltip="Удалить ячейку",
            on_click=self._on_delete_click
        )
        
        # Main row layout
        self.main_row = ft.Row([
            self.type_dropdown,
            ft.Container(width=10),  # Spacer
            self.language_dropdown if self.language_dropdown else ft.Container(width=0, height=0),
            ft.Container(width=10) if self.language_dropdown else ft.Container(width=0, height=0),
            self.content_field,
            ft.Container(width=10),  # Spacer
            delete_btn
        ], vertical_alignment=ft.CrossAxisAlignment.START)

    def _on_type_change(self, e):
        """Handle type change - rebuild content field"""
        old_content = self.content_field.value if self.content_field else ""
        
        # Clear the current content field
        self.content_field = None
        if self.language_dropdown:
            self.language_dropdown = None
        
        # Update cell type
        self.cell_data['type'] = e.control.value
        
        # Rebuild components based on new type
        self._build_components()
        
        # Update the main row
        self.main_row.controls = [
            self.type_dropdown,
            ft.Container(width=10),
            self.language_dropdown if self.language_dropdown else ft.Container(width=0, height=0),
            ft.Container(width=10) if self.language_dropdown else ft.Container(width=0, height=0),
            self.content_field,
            ft.Container(width=10),
            ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Удалить ячейку",
                on_click=self._on_delete_click
            )
        ]
        
        # Restore the old content
        self.content_field.value = old_content
        self.update()

    def _on_delete_click(self, e):
        """Handle delete button click"""
        if self.on_delete:
            self.on_delete(self)

    def build(self):
        return self.main_row
    
    def get_cell_data(self) -> Dict[str, Any]:
        """Get the current cell data"""
        cell = {
            'type': self.type_dropdown.value,
            'content': self.content_field.value
        }
        
        if self.type_dropdown.value == 'code' and self.language_dropdown:
            cell['language'] = self.language_dropdown.value
        
        return cell


class SnippetEditor(ft.Control):
    """A component for editing a complete snippet with multiple cells"""
    
    def __init__(self, snippet: Snippet = None, on_save=None, on_cancel=None):
        super().__init__()
        self.snippet = snippet or Snippet(id=None, title="", language="python", cells=[])
        self.on_save = on_save
        self.on_cancel = on_cancel
        self.title_field = None
        self.language_dropdown = None
        self.cells_list = ft.Column()
        self.cell_editors = []

    def _build_components(self):
        """Build the UI components for the snippet editor"""
        # Title field
        self.title_field = ft.TextField(
            value=self.snippet.title,
            label="Название сниппета",
            width=400
        )
        
        # Language dropdown
        self.language_dropdown = ft.Dropdown(
            value=self.snippet.language,
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
        
        # Add cell button
        add_cell_btn = ft.ElevatedButton(
            "Добавить ячейку",
            icon=ft.icons.ADD,
            on_click=self._add_cell
        )
        
        # Save and cancel buttons
        save_btn = ft.ElevatedButton("Сохранить", on_click=self._on_save_click)
        cancel_btn = ft.ElevatedButton("Отмена", on_click=self._on_cancel_click)
        
        # Initialize with existing cells
        for cell_data in self.snippet.cells:
            self._add_cell_editor(cell_data)

    def _add_cell_editor(self, cell_data: Dict[str, Any] = None):
        """Add a new cell editor to the list"""
        cell_editor = CellEditor(
            cell_data=cell_data,
            on_delete=self._remove_cell_editor
        )
        self.cell_editors.append(cell_editor)
        self.cells_list.controls.append(cell_editor)
        self.update()

    def _add_cell(self, e):
        """Add a new empty cell"""
        self._add_cell_editor({'type': 'text', 'content': ''})

    def _remove_cell_editor(self, cell_editor):
        """Remove a cell editor from the list"""
        if cell_editor in self.cell_editors:
            self.cell_editors.remove(cell_editor)
            self.cells_list.controls.remove(cell_editor)
            self.update()

    def _on_save_click(self, e):
        """Handle save button click"""
        if self.on_save:
            # Collect all cell data
            cells = []
            for editor in self.cell_editors:
                cells.append(editor.get_cell_data())
            
            # Create updated snippet
            updated_snippet = Snippet(
                id=self.snippet.id,
                title=self.title_field.value,
                language=self.language_dropdown.value,
                cells=cells
            )
            self.on_save(updated_snippet)

    def _on_cancel_click(self, e):
        """Handle cancel button click"""
        if self.on_cancel:
            self.on_cancel()

    def build(self):
        self._build_components()
        
        return ft.Column([
            ft.Text("Редактирование сниппета", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            self.title_field,
            self.language_dropdown,
            ft.Divider(),
            ft.Text("Ячейки содержимого:", weight=ft.FontWeight.BOLD),
            self.cells_list,
            ft.Divider(),
            ft.Row([self._add_cell_btn(), ft.ElevatedButton("Сохранить", on_click=self._on_save_click), 
                   ft.ElevatedButton("Отмена", on_click=self._on_cancel_click)])
        ], scroll=ft.ScrollMode.AUTO)

    def _add_cell_btn(self):
        """Create add cell button with proper binding"""
        return ft.ElevatedButton("Добавить ячейку", icon=ft.icons.ADD, on_click=self._add_cell)