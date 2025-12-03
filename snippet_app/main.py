import sys
import logging
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLineEdit, QTextEdit, 
                             QListWidget, QListWidgetItem, QMessageBox, QSplitter,
                             QLabel, QInputDialog, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3
import os

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler('snippet_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path='snippets.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        logger.debug("Initializing database")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS snippets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                language TEXT DEFAULT 'plain'
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.debug("Database initialized")
    
    def get_all_snippets(self):
        logger.debug("Getting all snippets from database")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, title, content, language FROM snippets ORDER BY title")
        snippets = cursor.fetchall()
        
        conn.close()
        logger.debug(f"Retrieved {len(snippets)} snippets")
        return snippets
    
    def search_snippets(self, query):
        logger.debug(f"Searching snippets for query: {query}")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, title, content, language 
            FROM snippets 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY title
        """, (f'%{query}%', f'%{query}%'))
        
        snippets = cursor.fetchall()
        
        conn.close()
        logger.debug(f"Found {len(snippets)} snippets matching query: {query}")
        return snippets
    
    def add_snippet(self, title, content, language='plain'):
        logger.debug(f"Adding new snippet: {title}")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO snippets (title, content, language)
            VALUES (?, ?, ?)
        """, (title, content, language))
        
        conn.commit()
        snippet_id = cursor.lastrowid
        conn.close()
        logger.debug(f"Snippet added with ID: {snippet_id}")
        return snippet_id
    
    def update_snippet(self, snippet_id, title, content, language='plain'):
        logger.debug(f"Updating snippet ID: {snippet_id}, title: {title}")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE snippets
            SET title=?, content=?, language=?
            WHERE id=?
        """, (title, content, language, snippet_id))
        
        conn.commit()
        conn.close()
        logger.debug(f"Snippet ID {snippet_id} updated")
    
    def delete_snippet(self, snippet_id):
        logger.debug(f"Deleting snippet ID: {snippet_id}")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM snippets WHERE id=?", (snippet_id,))
        
        conn.commit()
        conn.close()
        logger.debug(f"Snippet ID {snippet_id} deleted")

class SnippetCard(QWidget):
    def __init__(self, snippet_id, title, content, language, parent=None):
        super().__init__(parent)
        self.snippet_id = snippet_id
        self.title = title
        self.content = content
        self.language = language
        
        logger.debug(f"Creating SnippetCard for snippet ID: {self.snippet_id}, title: {self.title}")
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок сниппета
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #333;")
        title_label.setWordWrap(True)
        layout.addWidget(title_label)
        
        # Содержимое сниппета
        content_label = QLabel(self.content[:100] + "..." if len(self.content) > 100 else self.content)
        content_label.setWordWrap(True)
        content_label.setStyleSheet("color: #666; font-size: 12px; margin-top: 5px;")
        layout.addWidget(content_label)
        
        # Язык программирования
        lang_label = QLabel(f"Language: {self.language}")
        lang_label.setStyleSheet("color: #888; font-size: 10px; margin-top: 3px;")
        layout.addWidget(lang_label)
        
        self.setLayout(layout)
        
        # Установка стиля для карточки
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QWidget:hover {
                background-color: #f0f8ff;
            }
        """)

class SnippetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.selected_snippet_id = None
        
        logger.debug("Initializing SnippetApp")
        
        self.init_ui()
        self.load_snippets()
    
    def init_ui(self):
        logger.debug("Setting up UI")
        
        self.setWindowTitle('Snippet Manager')
        self.setGeometry(100, 100, 1000, 700)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной слой
        main_layout = QHBoxLayout(central_widget)
        
        # Левая панель для списка сниппетов
        left_panel = QVBoxLayout()
        
        # Поле поиска
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search snippets...')
        self.search_input.textChanged.connect(self.on_search_changed)
        left_panel.addWidget(QLabel('Search:'))
        left_panel.addWidget(self.search_input)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton('Add Snippet')
        self.add_btn.clicked.connect(self.add_snippet)
        button_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton('Edit Snippet')
        self.edit_btn.clicked.connect(self.edit_snippet)
        button_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton('Delete Snippet')
        self.delete_btn.clicked.connect(self.delete_snippet)
        button_layout.addWidget(self.delete_btn)
        
        left_panel.addLayout(button_layout)
        
        # Список сниппетов
        self.snippets_list = QListWidget()
        self.snippets_list.itemClicked.connect(self.on_snippet_selected)
        left_panel.addWidget(QLabel('Snippets:'))
        left_panel.addWidget(self.snippets_list)
        
        # Правая панель для деталей сниппета
        right_panel = QVBoxLayout()
        
        # Заголовок
        right_panel.addWidget(QLabel('Title:'))
        self.title_input = QLineEdit()
        right_panel.addWidget(self.title_input)
        
        # Язык
        right_panel.addWidget(QLabel('Language:'))
        self.language_input = QLineEdit()
        self.language_input.setText('plain')
        right_panel.addWidget(self.language_input)
        
        # Содержимое
        right_panel.addWidget(QLabel('Content:'))
        self.content_input = QTextEdit()
        right_panel.addWidget(self.content_input)
        
        # Кнопка копирования
        self.copy_btn = QPushButton('Copy to Clipboard')
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        right_panel.addWidget(self.copy_btn)
        
        # Разделитель
        splitter = QSplitter(Qt.Horizontal)
        
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([400, 600])
        
        main_layout.addWidget(splitter)
        
        logger.debug("UI setup complete")
    
    def load_snippets(self, search_query=''):
        logger.debug(f"Loading snippets with search query: '{search_query}'")
        
        if search_query:
            snippets = self.db.search_snippets(search_query)
        else:
            snippets = self.db.get_all_snippets()
        
        self.snippets_list.clear()
        
        for snippet_id, title, content, language in snippets:
            item = QListWidgetItem()
            card = SnippetCard(snippet_id, title, content, language)
            
            item.setSizeHint(card.sizeHint())
            self.snippets_list.addItem(item)
            self.snippets_list.setItemWidget(item, card)
        
        logger.debug(f"Loaded {len(snippets)} snippets into the list")
    
    def on_search_changed(self, text):
        logger.debug(f"Search text changed: '{text}'")
        self.load_snippets(text)
    
    def on_snippet_selected(self, item):
        logger.debug("Snippet selected")
        
        # Найти соответствующую карточку
        card = self.snippets_list.itemWidget(item)
        if isinstance(card, SnippetCard):
            self.selected_snippet_id = card.snippet_id
            self.title_input.setText(card.title)
            self.content_input.setText(card.content)
            self.language_input.setText(card.language)
            logger.debug(f"Selected snippet ID: {self.selected_snippet_id}")
    
    def add_snippet(self):
        logger.debug("Add snippet button clicked")
        
        title, ok = QInputDialog.getText(self, 'Add Snippet', 'Snippet Title:')
        if not ok or not title:
            logger.debug("Add snippet cancelled or empty title")
            return
        
        content, ok = QInputDialog.getText(self, 'Add Snippet', 'Snippet Content:')
        if not ok:
            logger.debug("Add snippet content cancelled")
            return
        
        language, ok = QInputDialog.getText(self, 'Add Snippet', 'Language (optional):', text='plain')
        if not ok:
            language = 'plain'
        
        snippet_id = self.db.add_snippet(title, content, language)
        logger.info(f"Added new snippet with ID: {snippet_id}")
        
        self.load_snippets()
        self.clear_selection()
    
    def edit_snippet(self):
        logger.debug(f"Edit snippet button clicked, selected ID: {self.selected_snippet_id}")
        
        if self.selected_snippet_id is None:
            QMessageBox.warning(self, 'Edit Snippet', 'Please select a snippet to edit.')
            logger.warning("No snippet selected for editing")
            return
        
        title = self.title_input.text()
        content = self.content_input.toPlainText()
        language = self.language_input.text()
        
        if not title:
            QMessageBox.warning(self, 'Edit Snippet', 'Please enter a title.')
            logger.warning("Empty title provided for editing")
            return
        
        self.db.update_snippet(self.selected_snippet_id, title, content, language)
        logger.info(f"Updated snippet with ID: {self.selected_snippet_id}")
        
        self.load_snippets()
        self.clear_selection()
    
    def delete_snippet(self):
        logger.debug(f"Delete snippet button clicked, selected ID: {self.selected_snippet_id}")
        
        if self.selected_snippet_id is None:
            QMessageBox.warning(self, 'Delete Snippet', 'Please select a snippet to delete.')
            logger.warning("No snippet selected for deletion")
            return
        
        reply = QMessageBox.question(
            self, 
            'Delete Snippet', 
            'Are you sure you want to delete this snippet?', 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_snippet(self.selected_snippet_id)
            logger.info(f"Deleted snippet with ID: {self.selected_snippet_id}")
            
            self.load_snippets()
            self.clear_selection()
    
    def copy_to_clipboard(self):
        logger.debug("Copy to clipboard button clicked")
        
        content = self.content_input.toPlainText()
        if content:
            clipboard = QApplication.clipboard()
            clipboard.setText(content)
            QMessageBox.information(self, 'Copy to Clipboard', 'Content copied to clipboard!')
            logger.info("Content copied to clipboard")
        else:
            QMessageBox.warning(self, 'Copy to Clipboard', 'No content to copy.')
            logger.warning("Attempted to copy empty content")
    
    def clear_selection(self):
        logger.debug("Clearing selection")
        self.selected_snippet_id = None
        self.title_input.clear()
        self.content_input.clear()
        self.language_input.setText('plain')

def main():
    logger.debug("Starting application")
    app = QApplication(sys.argv)
    window = SnippetApp()
    window.show()
    logger.debug("Application started")
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()