import flet as ft
from src.models.database import Database
from src.ui.main_view import MainView
from src.models.database import Snippet
import yaml


def initialize_demo_data(db: Database):
    """Initialize the database with demo snippets"""
    # Check if database is empty
    if not db.get_snippets():
        print("Initializing demo data...")
        
        # Python Data Science snippets
        python_ds_snippet = Snippet(
            id=None,
            title="Python: Data Science библиотеки",
            language="python",
            cells=[
                {
                    'type': 'text',
                    'content': '### Основные библиотеки для Data Science на Python\n\n- **pandas** - работа с табличными данными\n- **numpy** - числовые вычисления\n- **scikit-learn** - машинное обучение\n- **pytorch** - глубокое обучение'
                },
                {
                    'type': 'code',
                    'language': 'python',
                    'content': '''# Импорт основных библиотек
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import torch
import torch.nn as nn

# Пример работы с pandas
df = pd.DataFrame({
    'feature1': [1, 2, 3, 4, 5],
    'feature2': [10, 20, 30, 40, 50],
    'target': [100, 200, 300, 400, 500]
})

# Пример работы с numpy
arr = np.array([[1, 2, 3], [4, 5, 6]])
print("Массив numpy:", arr)

# Пример scikit-learn
X = df[['feature1', 'feature2']]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = LinearRegression()
model.fit(X_train, y_train)

# Пример PyTorch
class SimpleNet(nn.Module):
    def __init__(self):
        super(SimpleNet, self).__init__()
        self.fc = nn.Linear(2, 1)
    
    def forward(self, x):
        return self.fc(x)
'''
                }
            ]
        )
        db.add_snippet(python_ds_snippet)
        
        # API snippets
        api_snippet = Snippet(
            id=None,
            title="API: requests и fastapi",
            language="python",
            cells=[
                {
                    'type': 'text',
                    'content': '### Работа с API в Python\n\n- **requests** - для HTTP-запросов\n- **fastapi** - для создания API'
                },
                {
                    'type': 'code',
                    'language': 'python',
                    'content': '''# Пример использования requests
import requests

# GET-запрос
response = requests.get('https://api.example.com/data')
data = response.json()

# POST-запрос
payload = {'key': 'value'}
response = requests.post('https://api.example.com/data', json=payload)

# Пример FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items/")
def create_item(item: Item):
    return item
'''
                }
            ]
        )
        db.add_snippet(api_snippet)
        
        # Terminal snippets
        terminal_snippet = Snippet(
            id=None,
            title="Terminal: Полезные команды",
            language="bash",
            cells=[
                {
                    'type': 'text',
                    'content': '### Полезные команды для терминала\n\nКоманды для работы в командной строке Linux/Windows'
                },
                {
                    'type': 'code',
                    'language': 'bash',
                    'content': '''# Навигация
pwd                 # Показать текущую директорию
ls                  # Показать содержимое директории
cd <путь>          # Перейти в директорию
mkdir <имя>        # Создать директорию
rmdir <имя>        # Удалить пустую директорию

# Работа с файлами
cp <файл> <путь>   # Копировать файл
mv <файл> <путь>   # Переместить файл
rm <файл>          # Удалить файл
cat <файл>         # Показать содержимое файла
touch <файл>       # Создать пустой файл

# Системная информация
ps aux             # Показать все процессы
top                # Мониторинг ресурсов
df -h              # Информация о дисковом пространстве
free -m            # Информация об оперативной памяти

# Поиск
find /path -name "*.txt"    # Найти файлы по имени
grep "pattern" file.txt     # Найти строку в файле
'''
                }
            ]
        )
        db.add_snippet(terminal_snippet)
        
        # Docker snippets
        docker_snippet = Snippet(
            id=None,
            title="Docker: Основные команды",
            language="dockerfile",
            cells=[
                {
                    'type': 'text',
                    'content': '### Основные команды Docker\n\nКоманды для работы с контейнерами и образами'
                },
                {
                    'type': 'code',
                    'language': 'dockerfile',
                    'content': '''# Dockerfile пример
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

# Основные команды Docker
docker build -t myapp .                    # Собрать образ
docker run myapp                          # Запустить контейнер
docker run -d -p 80:80 myapp             # Запустить в фоне с порт-форвардингом
docker ps                                # Показать запущенные контейнеры
docker ps -a                             # Показать все контейнеры
docker stop <container_id>               # Остановить контейнер
docker rm <container_id>                 # Удалить контейнер
docker images                            # Показать образы
docker rmi <image_id>                    # Удалить образ
docker exec -it <container_id> bash      # Войти в запущенный контейнер

# Docker Compose
docker-compose up                        # Запустить сервисы
docker-compose down                      # Остановить сервисы
docker-compose build                     # Пересобрать сервисы
'''
                },
                {
                    'type': 'code',
                    'language': 'yaml',
                    'content': '''# docker-compose.yml пример
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/code
    environment:
      - FLASK_ENV=development
  redis:
    image: "redis:alpine"
'''
                }
            ]
        )
        db.add_snippet(docker_snippet)
        
        # Frontend snippets
        frontend_snippet = Snippet(
            id=None,
            title="Frontend: HTML + JavaScript",
            language="html",
            cells=[
                {
                    'type': 'text',
                    'content': '### Основы фронтенда\n\nПримеры HTML и JavaScript кода'
                },
                {
                    'type': 'code',
                    'language': 'html',
                    'content': '''<!DOCTYPE html>
<html>
<head>
    <title>Пример страницы</title>
</head>
<body>
    <h1 id="title">Привет, мир!</h1>
    <button onclick="changeText()">Нажми меня</button>
    
    <script>
        // Пример JavaScript
        function changeText() {
            document.getElementById('title').textContent = 'Текст изменен!';
        }
        
        // Пример асинхронного запроса
        async function fetchData() {
            try {
                const response = await fetch('https://api.example.com/data');
                const data = await response.json();
                console.log(data);
            } catch (error) {
                console.error('Ошибка:', error);
            }
        }
    </script>
</body>
</html>
'''
                }
            ]
        )
        db.add_snippet(frontend_snippet)
        
        # Java snippets
        java_snippet = Snippet(
            id=None,
            title="Java: Классы и методы",
            language="java",
            cells=[
                {
                    'type': 'text',
                    'content': '### Основы Java\n\nПримеры классов, методов и модификаторов доступа'
                },
                {
                    'type': 'code',
                    'language': 'java',
                    'content': '''public class Example {
    // Модификаторы доступа:
    // public - доступен из любого места
    // private - доступен только внутри класса
    // protected - доступен внутри пакета и подклассов
    // package-private (без модификатора) - доступен только внутри пакета
    
    private String privateField = "private";     // Доступ только внутри класса
    protected String protectedField = "protected"; // Внутри пакета и подклассов
    public String publicField = "public";        // Везде
    
    // Конструктор
    public Example() {
        System.out.println("Конструктор вызван");
    }
    
    // Публичный метод
    public void publicMethod() {
        System.out.println("Публичный метод");
        privateMethod(); // Можно вызвать приватный метод изнутри
    }
    
    // Приватный метод
    private void privateMethod() {
        System.out.println("Приватный метод");
    }
    
    // Защищенный метод
    protected void protectedMethod() {
        System.out.println("Защищенный метод");
    }
    
    // Метод с параметрами и возвратом
    public int add(int a, int b) {
        return a + b;
    }
    
    // Статический метод
    public static void staticMethod() {
        System.out.println("Статический метод");
    }
}

// Пример использования
public class Main {
    public static void main(String[] args) {
        Example obj = new Example();
        obj.publicMethod();
        System.out.println("Результат: " + obj.add(5, 3));
    }
}
'''
                }
            ]
        )
        db.add_snippet(java_snippet)
        
        # C++ snippets
        cpp_snippet = Snippet(
            id=None,
            title="C++: Структуры данных",
            language="c++",
            cells=[
                {
                    'type': 'text',
                    'content': '### Структуры данных в C++\n\nПримеры стека, очереди и дерева'
                },
                {
                    'type': 'code',
                    'language': 'c++',
                    'content': '''#include <iostream>
#include <stack>
#include <queue>
#include <vector>

// Узел для бинарного дерева
struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

// Пример использования стека
void stackExample() {
    std::stack<int> stack;
    
    // Добавление элементов
    stack.push(1);
    stack.push(2);
    stack.push(3);
    
    // Извлечение элементов
    while (!stack.empty()) {
        std::cout << stack.top() << " ";
        stack.pop();
    }
    std::cout << std::endl;
}

// Пример использования очереди
void queueExample() {
    std::queue<int> queue;
    
    // Добавление элементов
    queue.push(1);
    queue.push(2);
    queue.push(3);
    
    // Извлечение элементов
    while (!queue.empty()) {
        std::cout << queue.front() << " ";
        queue.pop();
    }
    std::cout << std::endl;
}

// Пример создания дерева
TreeNode* createTree() {
    TreeNode* root = new TreeNode(1);
    root->left = new TreeNode(2);
    root->right = new TreeNode(3);
    root->left->left = new TreeNode(4);
    root->left->right = new TreeNode(5);
    return root;
}

int main() {
    std::cout << "Стек: ";
    stackExample();
    
    std::cout << "Очередь: ";
    queueExample();
    
    return 0;
}
'''
                }
            ]
        )
        db.add_snippet(cpp_snippet)
        
        # SQL snippets
        sql_snippet = Snippet(
            id=None,
            title="SQL: CRUD операции",
            language="sql",
            cells=[
                {
                    'type': 'text',
                    'content': '### CRUD операции в SQL\n\nCreate, Read, Update, Delete'
                },
                {
                    'type': 'code',
                    'language': 'sql',
                    'content': '''-- CREATE (Создание)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- INSERT - добавление данных
INSERT INTO users (name, email) VALUES ('Иван Иванов', 'ivan@example.com');
INSERT INTO users (name, email) VALUES 
    ('Мария Петрова', 'maria@example.com'),
    ('Алексей Сидоров', 'alex@example.com');

-- READ (Чтение)
SELECT * FROM users;                              -- Все записи
SELECT name, email FROM users;                    -- Только указанные поля
SELECT * FROM users WHERE name = 'Иван Иванов';  -- Условие
SELECT * FROM users ORDER BY created_at DESC;     -- Сортировка
SELECT COUNT(*) FROM users;                       -- Подсчет

-- UPDATE (Обновление)
UPDATE users 
SET email = 'new_email@example.com' 
WHERE name = 'Иван Иванов';

-- DELETE (Удаление)
DELETE FROM users WHERE id = 1;                  -- Удалить конкретную запись
DELETE FROM users WHERE name LIKE '%Иван%';      -- Удалить по условию
DELETE FROM users;                               -- Удалить все записи

-- Дополнительные полезные операции
-- JOIN - соединение таблиц
SELECT u.name, p.title 
FROM users u
JOIN posts p ON u.id = p.user_id;

-- GROUP BY - группировка
SELECT name, COUNT(*) as post_count
FROM users u
JOIN posts p ON u.id = p.user_id
GROUP BY u.name;
'''
                }
            ]
        )
        db.add_snippet(sql_snippet)
        
        print("Demo data initialized successfully!")


def main(page: ft.Page):
    # Page setup
    page.title = "CodeSnippet Hub"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 800
    page.padding = 20
    
    # Initialize database
    db = Database()
    
    # Initialize demo data if database is empty
    initialize_demo_data(db)
    
    # Create and add main view
    main_view = MainView(db)
    page.add(main_view)


if __name__ == "__main__":
    ft.app(target=main)