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
    print("DEBUG: Starting main function")
    page.title = "SnippetHub"
    page.window_width = 1200
    page.window_height = 800

    db = Database()
    mode = ft.Ref[str]()
    mode.current = "list"
    current_snippet_id = ft.Ref[int]()

    def build_snippet_list():
        print("DEBUG: Building snippet list")
        search_field = ft.TextField(label="Поиск", expand=True, on_change=on_search)
        snippets_column = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        add_button = ft.ElevatedButton("Добавить сниппет", on_click=lambda e: open_add_dialog(page, db, refresh_list))

        container = ft.Container(
            content=ft.Column([
                ft.Row([search_field, add_button]),
                ft.Divider(),
                snippets_column
            ]),
            width=400,
            expand=True,
            padding=10
        )
        load_snippets(snippets_column, db, "")
        return container, snippets_column, search_field

    snippet_list, snippets_column, search_field = build_snippet_list()

    editor_container = ft.Container(expand=True, padding=10)

    main_row = ft.Row([snippet_list, editor_container], expand=True, visible=False)

    def switch_mode(new_mode: str, snippet_id: int = None):
        print(f"DEBUG: Switching mode to {new_mode}, snippet_id={snippet_id}")
        mode.current = new_mode
        if new_mode == "edit" and snippet_id:
            current_snippet_id.current = snippet_id
            snippet = db.get_snippet_by_id(snippet_id)
            editor = SnippetEditor(snippet=snippet, on_save=lambda updated: on_save_full_editor(updated, db, refresh_list))
            editor_container.content = editor.build()
        page.controls.clear()
        if new_mode == "list":
            page.add(snippet_list)
        else:
            main_row.visible = True
            page.add(main_row)
        page.update()

    switch_mode("list")

    def refresh_list():
        print("DEBUG: Refreshing snippet list")
        load_snippets(snippets_column, db, search_field.value or "")

    def on_search(e):
        print(f"DEBUG: Search changed: {e.control.value}")
        load_snippets(snippets_column, db, e.control.value or "")

    def load_snippets(container: ft.Column, db: Database, search_query: str = ""):
        print(f"DEBUG: Loading snippets with query '{search_query}'")
        try:
            container.controls.clear()
            snippets = db.get_snippets(search_query)
            for snippet in snippets:
                card = SnippetCard(
                    snippet_id=snippet['id'],
                    title=snippet['title'],
                    language=snippet['language'],
                    cells=snippet['cells'],
                    on_copy=lambda yaml_content: on_copy(yaml_content, page),
                    on_delete=lambda sid: on_delete_snippet(page, db, refresh_list, sid),
                    on_edit=lambda sid, t, l, c: open_edit_dialog(page, db, sid, t, l, c, snippet['tags'], switch_mode)
                )
                container.controls.append(card)
            page.update()
            logger.debug(f"Loaded {len(container.controls)} snippets")
        except Exception as ex:
            logger.error("Error in load_snippets: %s", ex)
            traceback.print_exc()

    def on_copy(yaml_content: str, page: ft.Page):
        print("DEBUG: Copying YAML content")
        import pyperclip
        pyperclip.copy(yaml_content)
        page.snack_bar = ft.SnackBar(ft.Text("YAML скопирован в буфер!"))
        page.snack_bar.open = True
        page.update()

    def on_delete_snippet(page: ft.Page, db: Database, refresh_func, snippet_id: int):
        print(f"DEBUG: Deleting snippet {snippet_id}")
        try:
            db.delete_snippet(snippet_id)
            page.snack_bar = ft.SnackBar(ft.Text("Сниппет удалён"))
            page.snack_bar.open = True
            refresh_func()
        except Exception as ex:
            logger.error("Failed to delete: %s", ex)
            page.snack_bar = ft.SnackBar(ft.Text("Ошибка удаления"))
            page.snack_bar.open = True
        page.update()

    def on_save_full_editor(updated_snippet: dict, db: Database, refresh_func):
        print(f"DEBUG: Saving full editor for snippet {updated_snippet['id']}")
        db.update_snippet(updated_snippet['id'], updated_snippet['title'], updated_snippet['language'], updated_snippet['cells'], updated_snippet['tags'])
        page.snack_bar = ft.SnackBar(ft.Text("Сниппет сохранён"))
        page.snack_bar.open = True
        refresh_func()
        page.update()

    def open_add_dialog(page: ft.Page, db: Database, refresh_func):
        print("DEBUG: Opening add dialog")

        def handle_submit(title: str, lang: str, cells: list, tags: str):
            print(f"DEBUG: Submitting new snippet: {title}, tags={tags}")
            db.add_snippet(title, lang, cells, tags)
            refresh_func()

        def handle_cancel():
            print("DEBUG: Cancel add dialog")
            page.dialog.open = False
            page.update()

        dialog = AddSnippetDialog(on_submit=handle_submit, on_cancel=handle_cancel)
        page.dialog = dialog.dialog
        page.dialog.open = True
        page.update()

    def open_edit_dialog(page: ft.Page, db: Database, snippet_id: int, title: str, language: str, cells: list, tags: str, switch_mode_func):
        print(f"DEBUG: Opening edit dialog for {snippet_id}")

        def handle_quick_save(new_title: str, new_lang: str, new_tags: str):
            print(f"DEBUG: Quick save: {new_title}, tags={new_tags}")
            db.update_snippet(snippet_id, new_title, new_lang, cells, new_tags)
            refresh_list()
            page.dialog.open = False
            page.update()

        def handle_full_edit():
            print("DEBUG: Switching to full edit")
            page.dialog.open = False
            switch_mode_func("edit", snippet_id)
            page.update()

        def handle_cancel():
            print("DEBUG: Cancel edit dialog")
            page.dialog.open = False
            page.update()

        dialog = EditSnippetDialog(on_quick_save=handle_quick_save, on_full_edit=handle_full_edit, on_cancel=handle_cancel)
        dialog.open(page, snippet_id, title, language, cells, tags)

if __name__ == "__main__":
    print("DEBUG: Running app")
    ft.app(target=main)