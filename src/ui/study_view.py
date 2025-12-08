# src/ui/study_view.py
import flet as ft
from src.utils.ai_helper import query_ollama
import threading


class StudySnippetView(ft.UserControl):
    def __init__(self, snippet: dict, on_back):
        super().__init__()
        self.snippet = snippet
        self.on_back = on_back
        self.explanation_containers = {}  # idx → ft.Markdown или ft.Text

    def _explain_cell(self, e, cell_index: int, cell_content: str):
        """Объяснение кода с простым обновлением (без run_thread_safe)"""
        container = self.explanation_containers[cell_index]

        # Если уже отображается — скрываем
        if hasattr(container, '_visible') and container._visible:
            container.content = None
            container._visible = False
            container.update()
            return

        # Показываем загрузку
        container.content = ft.Row([
            ft.ProgressRing(width=16, height=16),
            ft.Text("Анализирую...", size=12, italic=True)
        ])
        container._visible = True
        container.update()

        # Запрос в фоне
        def worker():
            try:
                prompt = f"""Кратко объясни на русском, что делает этот код на языке {self.snippet['language']}:

{cell_content}
"""
                response = query_ollama(prompt, model="qwen2.5-coder:1.5b")
            except Exception as ex:
                response = f"⚠️ Ошибка: {str(ex)}"

            # Обновляем UI — через page.update() извне
            container.content = ft.Column([
                ft.Markdown(
                    response,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    selectable=True,
                    code_theme="atom-one-dark"
                ),
                ft.TextButton("Скрыть", on_click=lambda _: self._explain_cell(None, cell_index, cell_content))
            ])
            container.update()

        threading.Thread(target=worker, daemon=True).start()

    def build(self):
        # Заголовок
        title = ft.Text(self.snippet["title"], size=24, weight=ft.FontWeight.BOLD)
        meta = ft.Text(
            f"Язык: {self.snippet['language']} | Теги: {self.snippet['tags'] or '—'}",
            color=ft.colors.GREY_700
        )

        header = ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.on_back()),
            ft.Text("Изучение сниппета", size=20),
            ft.Container(expand=True),
            ft.IconButton(ft.icons.SCHOOL, tooltip="Объяснить весь", disabled=True)  # Временно отключено
        ])

        # Основные элементы
        items = [
            header,
            ft.Divider(),
            title,
            meta,
            ft.Divider()
        ]

        # Ячейки
        for idx, cell in enumerate(self.snippet["cells"]):
            cell_type = cell.get("type", "code")
            content = cell.get("content", "")

            if cell_type in ("markdown", "text"):
                md = ft.Markdown(
                    content,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    selectable=True,
                    code_theme="atom-one-dark"
                )
                items.append(ft.Container(md, padding=10))

            elif cell_type == "code":
                code_block = f"```{self.snippet['language']}\n{content}\n```"
                md_code = ft.Markdown(
                    code_block,
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    code_theme="atom-one-dark",
                    selectable=True
                )

                explain_btn = ft.ElevatedButton(
                    "🧠 Объяснить код",
                    on_click=lambda e, i=idx, c=content: self._explain_cell(e, i, c),
                    height=32
                )

                # Контейнер для ответа ИИ (изначально пустой)
                explanation_box = ft.Container(padding=10)
                explanation_box._visible = False
                self.explanation_containers[idx] = explanation_box

                # Группируем элементы БЕЗ внешнего Container — только Row/Column
                cell_group = ft.Column([
                    md_code,
                    ft.Container(explain_btn, padding=ft.padding.only(top=6)),
                    explanation_box
                ], spacing=4)

                items.append(ft.Container(
                    content=cell_group,
                    bgcolor="#00000010",
                    padding=10,
                    border_radius=8,
                    margin=ft.margin.only(bottom=15)
                ))

        # Возвращаем Column с прокруткой
        return ft.Column(
            controls=items,
            scroll=ft.ScrollMode.AUTO,
            spacing=8,
        )

    def _handle_full_explain(self, e):
        # Показываем индикатор загрузки в виде Snackbar
        self.page.show_snack_bar(ft.SnackBar(ft.Text("Готовлю объяснение всего сниппета..."), open=True))

        # Формируем полный текст
        full_text = ""
        for cell in self.snippet["cells"]:
            if cell["type"] in ("markdown", "text"):
                full_text += cell["content"] + "\n\n"
            else:
                full_text += f"```{self.snippet['language']}\n{cell['content']}\n```\n\n"

        prompt = f"""Вы — эксперт-преподаватель по программированию. Объясните сниппет полностью:

    Название: {self.snippet['title']}
    Язык: {self.snippet['language']}
    Теги: {self.snippet['tags']}

    Содержимое:
    {full_text}

    Объясните:
    - Общую цель и назначение сниппета.
    - Какие ключевые концепции, паттерны или технологии в нём используются.
    - Что должен запомнить студент?
    Ответ дайте на русском языке, структурированно, без «воды».
    """

        def worker():
            try:
                response = query_ollama(prompt, model="qwen2.5-coder:1.5b")
            except Exception as ex:
                response = f"⚠️ Ошибка при запросе к ИИ:\n{str(ex)}"

            # Показываем результат в Snackbar (или можно добавить внизу — по желанию)
            def update_ui():
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Column([
                            ft.Text("🧠 Ответ ИИ:", weight=ft.FontWeight.BOLD),
                            ft.Text(response, selectable=True)
                        ], tight=True, spacing=5),
                        duration=10000,  # 10 секунд
                        open=True,
                        bgcolor=ft.colors.SURFACE_VARIANT
                    )
                )

            self.page.run_thread_safe(update_ui)

        threading.Thread(target=worker, daemon=True).start()