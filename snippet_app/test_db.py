import logging
import os
import sys
from main import DatabaseManager

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    handlers=[
        logging.FileHandler('test_db.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_database():
    logger.debug("Starting database tests")
    
    # Создаем экземпляр DatabaseManager
    db = DatabaseManager('test_snippets.db')
    
    # Тест добавления сниппета
    logger.debug("Testing add_snippet")
    snippet_id = db.add_snippet("Test Title", "Test Content", "python")
    logger.info(f"Added snippet with ID: {snippet_id}")
    
    # Тест получения всех сниппетов
    logger.debug("Testing get_all_snippets")
    all_snippets = db.get_all_snippets()
    logger.info(f"Total snippets: {len(all_snippets)}")
    
    # Тест поиска
    logger.debug("Testing search_snippets")
    search_results = db.search_snippets("Test")
    logger.info(f"Search results: {len(search_results)}")
    
    # Тест обновления
    logger.debug("Testing update_snippet")
    db.update_snippet(snippet_id, "Updated Title", "Updated Content", "javascript")
    
    # Проверяем обновленный сниппет
    updated_snippets = db.get_all_snippets()
    logger.info(f"Updated snippet: {updated_snippets[0] if updated_snippets else 'None'}")
    
    # Тест удаления
    logger.debug("Testing delete_snippet")
    db.delete_snippet(snippet_id)
    
    # Проверяем, что сниппет удален
    remaining_snippets = db.get_all_snippets()
    logger.info(f"Remaining snippets after deletion: {len(remaining_snippets)}")
    
    # Удаляем тестовую базу данных
    if os.path.exists('test_snippets.db'):
        os.remove('test_snippets.db')
        logger.debug("Test database removed")
    
    logger.debug("Database tests completed")

if __name__ == "__main__":
    test_database()