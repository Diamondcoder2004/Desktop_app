# src/ui/study_view.py
import flet as ft
import threading
from src.utils.ai_helper import query_ollama


class StudySnippetView(ft.UserControl):
    def __init__(self, snippet: dict, on_back):
        super().__init__()
        self.snippet = snippet
        self.on_back = on_back
        self.explanation_markdowns = {}      # Markdown-контролы объяснений
        self.toggle_buttons = {}             # Кнопки "Показать"/"Скрыть"
        self.sidebar_visible = False
        self.full_explanation_md = None

    def build(self):
        title = ft.Text(self.snippet["title"], size=24, weight=ft.FontWeight.BOLD)
        meta = ft.Text(
            f"Язык: {self.snippet['language']} | Теги: {self.snippet['tags'] or '—'}",
            color=ft.colors.GREY_700
        )

        header = ft.Row([
            ft.IconButton(ft.icons.ARROW_BACK, on_click=lambda _: self.on_back()),
            ft.Text("Изучение сниппета", size=20),
            ft.Container(expand=True),
            ft.IconButton(
                ft.icons.SCHOOL,
                tooltip="Объяснить весь сниппет",
                on_click=self._handle_full_explain
            )
        ])

        items = [
            header,
            ft.Divider(),
            title,
            meta,
            ft.Divider()
        ]

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

                # Кнопка объяснения
                explain_btn = ft.ElevatedButton(
                    "Объяснить код",
                    on_click=lambda e, i=idx, c=content: self._explain_cell(e, i, c),
                    height=32
                )

                # Markdown для объяснения (изначально скрыт)
                explanation_md = ft.Markdown(
                    "",
                    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                    selectable=True,
                    code_theme="atom-one-dark",
                    visible=False
                )
                self.explanation_markdowns[idx] = explanation_md

                # Кнопка переключения (изначально скрыта)
                toggle_btn = ft.TextButton(
                    "Показать",
                    on_click=lambda e, i=idx: self._toggle_explanation(i),
                    visible=False
                )
                self.toggle_buttons[idx] = toggle_btn

                # Контейнер с кодом и кнопками
                button_row = ft.Row([
                    explain_btn,
                    ft.Container(expand=True),  # Отступ
                    toggle_btn
                ], expand=True)

                cell_group = ft.Column([
                    md_code,
                    ft.Container(button_row, padding=ft.padding.only(top=6)),
                    explanation_md
                ], spacing=4)

                items.append(ft.Container(
                    content=cell_group,
                    bgcolor="#00000010",
                    padding=10,
                    border_radius=8,
                    margin=ft.margin.only(bottom=15)
                ))

        main_content = ft.Column(
            controls=items,
            scroll=ft.ScrollMode.AUTO,
            spacing=8,
            expand=True
        )

        # Полное объяснение — ВНУТРИ прокручиваемого контейнера
        self.full_explanation_md = ft.Markdown(
            "Нажмите кнопку \"Объяснить весь\", чтобы получить объяснение всего сниппета",
            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
            selectable=True,
            code_theme="atom-one-dark"
        )

        # Оборачиваем Markdown в Column с прокруткой
        explanation_scroll = ft.Column(
            [self.full_explanation_md],
            scroll=ft.ScrollMode.AUTO,
            expand=True
        )

        self.sidebar_content = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Объяснение сниппета", size=18, weight=ft.FontWeight.BOLD),
                    ft.IconButton(ft.icons.CLOSE, on_click=self._toggle_sidebar, tooltip="Скрыть"),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                explanation_scroll
            ], expand=True),
            width=400,
            padding=10,
            bgcolor=ft.colors.SURFACE_VARIANT,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=8,
            visible=False
        )

        return ft.Row([
            ft.Container(
                content=main_content,
                expand=True,
                padding=ft.padding.only(right=10)
            ),
            self.sidebar_content
        ], expand=True)

    def _toggle_explanation(self, idx: int):
        md = self.explanation_markdowns[idx]
        toggle_btn = self.toggle_buttons[idx]

        md.visible = not md.visible
        toggle_btn.text = "Скрыть" if md.visible else "Показать"
        md.update()
        toggle_btn.update()

    def _explain_cell(self, e, cell_index: int, cell_content: str):
        md = self.explanation_markdowns[cell_index]
        toggle_btn = self.toggle_buttons[cell_index]

        # Если уже загружено — просто переключаем видимость
        if md.value and md.value != "":
            self._toggle_explanation(cell_index)
            return

        # Показываем загрузку
        md.value = "_Анализирую..._"
        md.visible = True
        toggle_btn.text = "Скрыть"
        toggle_btn.visible = True
        md.update()
        toggle_btn.update()

        def worker():
            try:
                prompt = f"""Кратко объясни на русском, что делает этот код на языке {self.snippet['language']}:

{cell_content}
"""
                response = query_ollama(prompt, model="qwen2.5-coder:1.5b")
            except Exception as ex:
                response = f" Ошибка: {str(ex)}"

            md.value = response
            md.update()

        threading.Thread(target=worker, daemon=True).start()

    def _handle_full_explain(self, e):
        self.sidebar_visible = True
        self.sidebar_content.visible = True
        self.full_explanation_md.value = "_Анализирую весь сниппет..._"
        self.full_explanation_md.update()
        self.sidebar_content.update()

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

Содержимое сниппета:
{full_text}

Объясните подробно:
1. Общую цель и назначение сниппета
2. Ключевые концепции и технологии
3. Как работает код пошагово
4. Что должен запомнить студент?
5. Практическое применение этого кода

Отвечайте на русском языке, структурированно и понятно.
"""

        def worker():
            try:
                response = query_ollama(prompt, model="qwen2.5-coder:1.5b")
            except Exception as ex:
                response = f"#Ошибка при запросе\n\n```\n{str(ex)}\n```"

            self.full_explanation_md.value = response
            self.full_explanation_md.update()

        threading.Thread(target=worker, daemon=True).start()

    def _toggle_sidebar(self, e=None):
        self.sidebar_visible = not self.sidebar_visible
        self.sidebar_content.visible = self.sidebar_visible
        self.sidebar_content.update()