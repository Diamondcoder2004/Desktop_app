import flet as ft
import logging
import traceback
from src.models.database import Database
from src.ui.components import SnippetEditor
from src.ui.dialogs import AddSnippetDialog, EditSnippetDialog
from src.ui.snippet_card import SnippetCard
from src.ui.main_editor_view import MainEditorView
import os
logging.basicConfig(level=logging.DEBUG, format="DEBUG: %(message)s")
logger = logging.getLogger("snippethub")

def main(page: ft.Page):
    print("DEBUG: Запуск main функции")
    page.title = "SnippetHub"
    page.window.width = 1200
    page.window.height = 800

    try:
        db = Database()
        print("DEBUG: БД успешно инициализирована")
    except Exception as e:
        print(f"DEBUG: Ошибка БД при старте: {e}. Пересоздание.")
        os.remove(db.db_name) if 'db' in locals() else print("DEBUG: Файл БД не найден")
        db = Database()

    mode = ft.Ref[str]()
    mode.current = "list"
    current_snippet_id = ft.Ref[int]()
    # Для управления большим редактором
    # Для управления большим редактором
    is_in_main_editor = ft.Ref[bool]()
    is_in_main_editor.current = False
    main_editor_view = ft.Ref[MainEditorView]()

    def switch_to_main_editor(snippet=None):
        """Переключает в режим большого редактора"""
        if is_in_main_editor.current:
            return

        # Создаем большой редактор
        editor = MainEditorView(
            db=db,
            page=page,
            on_back=lambda: switch_from_main_editor(),
            initial_snippet=snippet
        )
        main_editor_view.current = editor

        # Очищаем страницу и добавляем редактор
        page.controls.clear()
        page.add(editor)
        is_in_main_editor.current = True
        page.update()

    def switch_from_main_editor():
        """Возвращается из большого редактора в основной вид"""
        if not is_in_main_editor.current:
            return

        # Возвращаем основной вид
        page.controls.clear()
        if mode.current == "list":
            page.add(snippet_list)
        else:
            main_row.visible = True
            page.add(main_row)

        is_in_main_editor.current = False
        main_editor_view.current = None
        # Обновляем список сниппетов
        refresh_list(snippets_grid, search_field)
        page.update()

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
            runs_count=3,
            max_extent=300,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10
        )

        # Кнопки в хедере
        header_buttons = ft.Row([
            ft.ElevatedButton(
                "Большой редактор",
                icon=ft.icons.EDIT,
                on_click=lambda _: switch_to_main_editor()
            ),
            ft.ElevatedButton(
                "Добавить сниппет",
                icon=ft.icons.ADD,
                on_click=lambda e: open_add_dialog(page, db, lambda: refresh_list(snippets_grid, search_field))
            )
        ], spacing=10)

        container = ft.Container(
            content=ft.Column([
                ft.Row([search_field, header_buttons]),
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
        # Если мы в большом редакторе - выходим из него
        if is_in_main_editor.current:
            switch_from_main_editor()

        mode.current = new_mode
        if new_mode == "edit" and snippet_id:
            current_snippet_id.current = snippet_id
            snippet = db.get_snippet_by_id(snippet_id)
            print(f"DEBUG: Загружен сниппет для редактирования: {snippet['title'] if snippet else 'Не найден'}")
            if snippet:
                editor = SnippetEditor(snippet=snippet, on_save=lambda updated: on_save_full_editor(updated, db,
                                                                                                    lambda: refresh_list(
                                                                                                        snippets_grid,
                                                                                                        search_field)))
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
        def handle_submit(title, lang, cells, tags):
            db.add_snippet(title, lang, cells, tags)
            refresh_func()
            page.snack_bar = ft.SnackBar(ft.Text("Сниппет добавлен!"))
            page.snack_bar.open = True
            page.update()

        dialog = AddSnippetDialog(handle_submit, lambda: None, page)
        dialog.open()

    def open_edit_dialog(page: ft.Page, db: Database, snippet_id: int, title: str, language: str, cells: list,
                         tags: str, switch_mode_func):
        def handle_save(snippet_id, new_title, new_lang, new_cells, new_tags):
            db.update_snippet(snippet_id, new_title, new_lang, new_cells, new_tags)
            refresh_list(snippets_grid, search_field)
            page.snack_bar = ft.SnackBar(ft.Text("Сниппет обновлён!"))
            page.snack_bar.open = True
            page.update()

        # Обработчик для большого редактора
        def handle_full_edit(snippet_data=None):
            if snippet_data:
                # Если есть данные из диалога - открываем их в большом редакторе
                switch_to_main_editor(snippet_data)
            else:
                # Иначе открываем существующий сниппет
                switch_to_main_editor({
                    "id": snippet_id,
                    "title": title,
                    "language": language,
                    "tags": tags,
                    "cells": cells
                })

        dialog = EditSnippetDialog(handle_save, handle_full_edit, page)
        dialog.open(snippet_id, title, language, cells, tags)


if __name__ == "__main__":
    print("DEBUG: Запуск приложения")
    ft.app(target=main)