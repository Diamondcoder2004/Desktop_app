import flet as ft
import logging
import traceback
from src.models.database import Database
from src.ui.components import SnippetEditor
from src.ui.dialogs import AddSnippetDialog, EditSnippetDialog
from src.ui.snippet_card import SnippetCard

logging.basicConfig(level=logging.DEBUG, format="DEBUG: %(message)s")
logger = logging.getLogger("snippethub")

def main(page: ft.Page):
    print("DEBUG: Запуск main функции")
    page.title = "SnippetHub"
    page.window.width = 1200
    page.window.height = 800

    db = Database()
    mode = ft.Ref[str]()
    mode.current = "list"
    current_snippet_id = ft.Ref[int]()

    # Определяем все функции заранее
    def refresh_list(snippets_grid, search_field):
        print("DEBUG: Обновление списка сниппетов")
        load_snippets(snippets_grid, db, search_field.value or "")

    def on_search(e, snippets_grid):
        print(f"DEBUG: Поиск изменён: {e.control.value}")
        load_snippets(snippets_grid, db, e.control.value or "")

    def load_snippets(container: ft.GridView, db: Database, search_query: str = ""):
        print(f"DEBUG: Загрузка сниппетов с запросом '{search_query}'")
        try:
            container.controls.clear()
            snippets = db.get_snippets(search_query)
            for snippet in snippets:
                print(f"DEBUG: Добавление карточки для сниппета ID {snippet['id']}")
                card = SnippetCard(
                    snippet_id=snippet['id'],
                    title=snippet['title'],
                    language=snippet['language'],
                    cells=snippet['cells'],
                    on_copy=lambda yaml_content: on_copy(yaml_content, page),
                    on_delete=lambda sid: confirm_delete_snippet(page, db, lambda: refresh_list(snippets_grid, search_field), sid),
                    on_edit=lambda sid, t, l, c: open_edit_dialog(page, db, sid, t, l, c, snippet['tags'], switch_mode)
                )
                container.controls.append(card)
            page.update()
            logger.debug(f"Загружено {len(container.controls)} сниппетов")
        except Exception as ex:
            print(f"DEBUG: Ошибка в load_snippets: {ex}")
            logger.error(f"Ошибка в load_snippets: {ex}")
            traceback.print_exc()

    def build_snippet_list():
        print("DEBUG: Построение списка сниппетов")
        search_field = ft.TextField(label="Поиск", expand=True)
        search_field.on_change = lambda e: on_search(e, snippets_grid)
        snippets_grid = ft.GridView(
            expand=True,
            runs_count=3,  # 3 карточки в ряд для заполнения окна
            max_extent=300,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10
        )
        add_button = ft.ElevatedButton("Добавить сниппет", on_click=lambda e: open_add_dialog(page, db, lambda: refresh_list(snippets_grid, search_field)))

        container = ft.Container(
            content=ft.Column([
                ft.Row([search_field, add_button]),
                ft.Divider(),
                snippets_grid
            ]),
            expand=True,
            padding=10
        )
        load_snippets(snippets_grid, db, "")
        return container, snippets_grid, search_field

    snippet_list, snippets_grid, search_field = build_snippet_list()

    editor_container = ft.Container(expand=True, padding=10)

    main_row = ft.Row([snippet_list, editor_container], expand=True, visible=False)

    def switch_mode(new_mode: str, snippet_id: int = None):
        print(f"DEBUG: Переключение режима на {new_mode}, snippet_id={snippet_id}")
        mode.current = new_mode
        if new_mode == "edit" and snippet_id:
            current_snippet_id.current = snippet_id
            snippet = db.get_snippet_by_id(snippet_id)
            print(f"DEBUG: Загружен сниппет для редактирования: {snippet['title'] if snippet else 'Не найден'}")
            if snippet:
                editor = SnippetEditor(snippet=snippet, on_save=lambda updated: on_save_full_editor(updated, db, lambda: refresh_list(snippets_grid, search_field)))
                editor_container.content = editor.build()
        page.controls.clear()
        if new_mode == "list":
            page.add(snippet_list)
        else:
            main_row.visible = True
            page.add(main_row)
        page.update()

    switch_mode("list")

    def confirm_delete_snippet(page: ft.Page, db: Database, refresh_func, snippet_id: int):
        print(f"DEBUG: Открытие диалога подтверждения удаления для {snippet_id}")

        def on_confirm(e):
            print("DEBUG: Подтверждение удаления")
            db.delete_snippet(snippet_id)
            page.snack_bar = ft.SnackBar(ft.Text("Сниппет удалён"))
            page.snack_bar.open = True
            refresh_func()
            page.dialog.open = False
            page.update()

        def on_cancel(e):
            print("DEBUG: Отмена удаления")
            page.dialog.open = False
            page.update()

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Подтвердите удаление"),
            content=ft.Text("Вы уверены, что хотите удалить этот сниппет?"),
            actions=[
                ft.TextButton("Отмена", on_click=on_cancel),
                ft.ElevatedButton("Удалить", on_click=on_confirm, color="red")
            ]
        )
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    def on_copy(yaml_content: str, page: ft.Page):
        print("DEBUG: Копирование YAML контента")
        import pyperclip
        pyperclip.copy(yaml_content)
        page.snack_bar = ft.SnackBar(ft.Text("YAML скопирован в буфер!"))
        page.snack_bar.open = True
        page.update()

    def on_save_full_editor(updated_snippet: dict, db: Database, refresh_func):
        print(f"DEBUG: Сохранение полного редактора для сниппета {updated_snippet['id']}")
        db.update_snippet(updated_snippet['id'], updated_snippet['title'], updated_snippet['language'], updated_snippet['cells'], updated_snippet['tags'])
        page.snack_bar = ft.SnackBar(ft.Text("Сниппет сохранён"))
        page.snack_bar.open = True
        refresh_func()
        page.update()

    def open_add_dialog(page: ft.Page, db: Database, refresh_func):
        print("DEBUG: Открытие диалога добавления")

        def handle_submit(title: str, lang: str, cells: list, tags: str):
            print(f"DEBUG: Отправка нового сниппета: {title}, tags={tags}")
            db.add_snippet(title, lang, cells, tags)
            refresh_func()
            page.dialog.open = False
            page.update()

        def handle_cancel():
            print("DEBUG: Отмена диалога добавления")
            page.dialog.open = False
            page.update()

        dialog = AddSnippetDialog(on_submit=handle_submit, on_cancel=handle_cancel)
        page.dialog = dialog.dialog
        page.dialog.open = True
        page.update()

    def open_edit_dialog(page: ft.Page, db: Database, snippet_id: int, title: str, language: str, cells: list, tags: str, switch_mode_func):
        print(f"DEBUG: Открытие диалога редактирования для {snippet_id}")

        def handle_submit(updated_id: int, new_title: str, new_lang: str, new_cells: list, new_tags: str):
            print(f"DEBUG: Быстрое сохранение: {new_title}, tags={new_tags}")
            db.update_snippet(updated_id, new_title, new_lang, new_cells, new_tags)
            refresh_list(snippets_grid, search_field)
            page.dialog.open = False
            page.update()

        def handle_full_edit():
            print("DEBUG: Переход к полному редактированию")
            page.dialog.open = False
            switch_mode_func("edit", snippet_id)
            page.update()

        def handle_cancel():
            print("DEBUG: Отмена диалога редактирования")
            page.dialog.open = False
            page.update()

        dialog = EditSnippetDialog(on_submit=handle_submit, on_full_edit=handle_full_edit, on_cancel=handle_cancel)
        dialog.open(page, snippet_id, title, language, cells, tags)

if __name__ == "__main__":
    print("DEBUG: Запуск приложения")
    ft.app(target=main)