import sys
import os

sys.path.insert(0, '.')

from models.database import Database


def create_demo_data():
    """Создает демо-данные для наполнения базы"""
    demo_snippets = []

    # Python - Data Science
    demo_snippets.append({
        "title": "Python Data Science Basics",
        "language": "python",
        "tags": "pandas,numpy,scikit-learn,data-science",
        "cells": [
            {
                "type": "markdown",
                "content": "## Основы Data Science с Python\nРабота с pandas, numpy и scikit-learn"
            },
            {
                "type": "code",
                "content": "# Импорт библиотек\nimport pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.ensemble import RandomForestClassifier"
            },
            {
                "type": "code",
                "content": "# Создание DataFrame\nstudents = pd.DataFrame({\n    'name': ['Alice', 'Bob', 'Charlie'],\n    'age': [23, 25, 24],\n    'grade': [85.5, 92.0, 78.5]\n})\nprint(students)"
            },
            {
                "type": "code",
                "content": "# Работа с numpy массивами\narr = np.array([[1, 2, 3], [4, 5, 6]])\nprint(f\"Форма: {arr.shape}\")\nprint(f\"Среднее: {np.mean(arr)}\")"
            },
            {
                "type": "code",
                "content": "# Пример машинного обучения\nX = np.random.rand(100, 4)\ny = np.random.randint(0, 2, 100)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)\nmodel = RandomForestClassifier()\nmodel.fit(X_train, y_train)\naccuracy = model.score(X_test, y_test)\nprint(f\"Точность модели: {accuracy:.2f}\")"
            }
        ]
    })

    # Python - API Development
    demo_snippets.append({
        "title": "Python API Development",
        "language": "python",
        "tags": "requests,fastapi,api,web",
        "cells": [
            {
                "type": "markdown",
                "content": "## Разработка API с Python\nИспользование requests и FastAPI"
            },
            {
                "type": "code",
                "content": "# HTTP запросы с requests\nimport requests\n\n# GET запрос\nresponse = requests.get('https://jsonplaceholder.typicode.com/posts/1')\nprint(f\"Статус: {response.status_code}\")\nprint(f\"Данные: {response.json()}\")"
            },
            {
                "type": "code",
                "content": "# POST запрос\nnew_post = {'title': 'My Post', 'body': 'Content here', 'userId': 1}\nresponse = requests.post('https://jsonplaceholder.typicode.com/posts', json=new_post)\nprint(f\"Создан пост: {response.json()}\")"
            },
            {
                "type": "code",
                "content": "# FastAPI базовый пример\nfrom fastapi import FastAPI\nfrom pydantic import BaseModel\n\napp = FastAPI()\n\nclass Item(BaseModel):\n    name: str\n    price: float\n\n@app.get(\"/\")\nasync def root():\n    return {\"message\": \"Hello World\"}\n\n@app.post(\"/items/\")\nasync def create_item(item: Item):\n    return {\"item\": item}"
            },
            {
                "type": "text",
                "content": "Запуск FastAPI: uvicorn main:app --reload"
            }
        ]
    })

    # Terminal / CMD
    demo_snippets.append({
        "title": "Полезные команды терминала",
        "language": "bash",
        "tags": "terminal,cmd,linux,commands",
        "cells": [
            {
                "type": "markdown",
                "content": "## Полезные команды терминала\nLinux/MacOS/Windows"
            },
            {
                "type": "code",
                "content": "# Навигация и файлы\npwd                    # Показать текущую директорию\nls -la                 # Список файлов с подробностями\ncd /path/to/dir        # Перейти в директорию\nmkdir new_folder       # Создать папку\nrm file.txt            # Удалить файл\nrm -rf folder          # Удалить папку рекурсивно"
            },
            {
                "type": "code",
                "content": "# Работа с процессами\nps aux                 # Список процессов\nkill -9 PID            # Убить процесс по PID\ntop                    # Мониторинг системных ресурсов\nhtop                   # Улучшенный top (требует установки)"
            },
            {
                "type": "code",
                "content": "# Сетевые команды\nping google.com        # Проверить соединение\nnetstat -tuln         # Список сетевых соединений\nifconfig               # Информация о сетевых интерфейсах\nip addr                # Альтернатива ifconfig"
            },
            {
                "type": "code",
                "content": "# Поиск и фильтрация\ngrep \"pattern\" file.txt     # Найти строку в файле\nfind /path -name \"*.py\"     # Найти файлы по шаблону\n|                          # Пайп для передачи вывода\n> file.txt                 # Перенаправить вывод в файл\n>> file.txt                # Добавить вывод в файл"
            }
        ]
    })

    # Docker
    demo_snippets.append({
        "title": "Docker и Docker Compose",
        "language": "docker",
        "tags": "docker,containers,devops",
        "cells": [
            {
                "type": "markdown",
                "content": "## Docker и Docker Compose\nКонтейнеризация приложений"
            },
            {
                "type": "code",
                "content": "# Dockerfile базовый пример\nFROM python:3.9-slim\n\nWORKDIR /app\n\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\n\nCOPY . .\n\nEXPOSE 8000\n\nCMD [\"uvicorn\", \"main:app\", \"--host\", \"0.0.0.0\", \"--port\", \"8000\"]"
            },
            {
                "type": "code",
                "content": "# Основные команды Docker\ndocker build -t my-app .           # Сборка образа\ndocker run -d -p 8000:8000 my-app   # Запуск контейнера\ndocker ps                          # Список запущенных контейнеров\ndocker logs container_name         # Просмотр логов\ndocker stop container_name         # Остановка контейнера\ndocker rm container_name           # Удаление контейнера\ndocker images                      # Список образов"
            },
            {
                "type": "code",
                "content": "# docker-compose.yml пример\nversion: '3.8'\n\nservices:\n  web:\n    build: .\n    ports:\n      - \"8000:8000\"\n    volumes:\n      - .:/app\n    depends_on:\n      - db\n  \n  db:\n    image: postgres:13\n    environment:\n      POSTGRES_DB: mydb\n      POSTGRES_USER: user\n      POSTGRES_PASSWORD: password\n    volumes:\n      - postgres_data:/var/lib/postgresql/data\n\nvolumes:\n  postgres_data:"
            },
            {
                "type": "code",
                "content": "# Команды Docker Compose\ndocker-compose up -d       # Запуск всех сервисов\ndocker-compose down        # Остановка и удаление\ndocker-compose ps          # Статус сервисов\ndocker-compose logs web    # Логи конкретного сервиса\ndocker-compose exec web sh # Запуск shell в контейнере"
            }
        ]
    })

    # Frontend - HTML + JavaScript
    demo_snippets.append({
        "title": "Frontend: HTML + JavaScript",
        "language": "html",
        "tags": "html,javascript,frontend,web",
        "cells": [
            {
                "type": "markdown",
                "content": "## Базовый Frontend\nHTML структура и JavaScript взаимодействие"
            },
            {
                "type": "code",
                "content": "<!-- Базовая HTML структура -->\n<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>My App</title>\n    <style>\n        .container { max-width: 800px; margin: 0 auto; padding: 20px; }\n        .btn { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }\n        .btn:hover { background: #0056b3; }\n    </style>\n</head>\n<body>\n    <div class=\"container\">\n        <h1 id=\"title\">Welcome!</h1>\n        <button id=\"changeBtn\" class=\"btn\">Change Title</button>\n        <div id=\"output\"></div>\n    </div>\n    <script src=\"script.js\"></script>\n</body>\n</html>"
            },
            {
                "type": "code",
                "content": "// script.js\nconst title = document.getElementById('title');\nconst btn = document.getElementById('changeBtn');\nconst output = document.getElementById('output');\n\nbtn.addEventListener('click', () => {\n    title.textContent = 'Title Changed!';\n    output.innerHTML = `<p>Changed at: ${new Date().toLocaleTimeString()}</p>`;\n});\n\n// Fetch API пример\nasync function fetchData() {\n    try {\n        const response = await fetch('https://jsonplaceholder.typicode.com/posts/1');\n        const data = await response.json();\n        console.log('Загружено:', data.title);\n    } catch (error) {\n        console.error('Ошибка:', error);\n    }\n}\n\n// fetchData(); // Раскомментировать для теста"
            },
            {
                "type": "code",
                "content": "// Работа с формами\nfunction handleFormSubmit(event) {\n    event.preventDefault();\n    const formData = new FormData(event.target);\n    const data = Object.fromEntries(formData);\n    console.log('Данные формы:', data);\n}\n\n// Пример использования:\n// <form onsubmit=\"handleFormSubmit(event)\">\n//     <input name=\"email\" type=\"email\" required>\n//     <button type=\"submit\">Submit</button>\n// </form>"
            }
        ]
    })

    # Java
    demo_snippets.append({
        "title": "Java Базовый синтаксис",
        "language": "java",
        "tags": "java,oop,classes,methods",
        "cells": [
            {
                "type": "markdown",
                "content": "## Java: Классы, методы и модификаторы доступа\nОбъяснение прав доступа"
            },
            {
                "type": "code",
                "content": "// Модификаторы доступа в Java\npublic class Person {\n    // public - доступен отовсюду\n    public String name;\n    \n    // protected - доступен в пакете и подклассах\n    protected int age;\n    \n    // default (package-private) - доступен только в пакете\n    String email;\n    \n    // private - доступен только внутри класса\n    private String ssn;\n    \n    // Конструктор\n    public Person(String name, int age, String email, String ssn) {\n        this.name = name;\n        this.age = age;\n        this.email = email;\n        this.ssn = ssn;\n    }\n    \n    // Геттер для private поля\n    public String getSsn() {\n        return this.ssn;\n    }\n}"
            },
            {
                "type": "code",
                "content": "// Наследование и методы\npublic class Student extends Person {\n    private String studentId;\n    \n    public Student(String name, int age, String email, String ssn, String studentId) {\n        super(name, age, email, ssn); // вызов конструктора родителя\n        this.studentId = studentId;\n    }\n    \n    // Метод может быть переопределен\n    @Override\n    public String toString() {\n        return String.format(\"Student[%s, ID: %s]\", name, studentId);\n    }\n    \n    // Статический метод - принадлежит классу, а не экземпляру\n    public static void printUniversity() {\n        System.out.println(\"University Name\");\n    }\n}"
            },
            {
                "type": "code",
                "content": "// Использование классов\npublic class Main {\n    public static void main(String[] args) {\n        Person person = new Person(\"John\", 25, \"john@email.com\", \"123-45-6789\");\n        Student student = new Student(\"Alice\", 20, \"alice@email.com\", \"987-65-4321\", \"S12345\");\n        \n        System.out.println(person.name); // public - доступно\n        System.out.println(person.age);   // protected - доступно (в том же пакете)\n        System.out.println(person.email); // default - доступно (в том же пакете)\n        // System.out.println(person.ssn); // ошибка! private поле недоступно\n        \n        System.out.println(student.toString());\n        Student.printUniversity();\n    }\n}"
            }
        ]
    })

    # C++
    demo_snippets.append({
        "title": "C++ Структуры данных",
        "language": "cpp",
        "tags": "cpp,algorithms,data-structures",
        "cells": [
            {
                "type": "markdown",
                "content": "## C++: Структуры данных\nСтеки, очереди, деревья"
            },
            {
                "type": "code",
                "content": "#include <iostream>\n#include <stack>\n#include <queue>\n#include <vector>\n\n// Реализация стека\nvoid demonstrateStack() {\n    std::stack<int> s;\n    s.push(1);\n    s.push(2);\n    s.push(3);\n    \n    std::cout << \"Stack (LIFO): \";\n    while (!s.empty()) {\n        std::cout << s.top() << \" \";\n        s.pop();\n    }\n    std::cout << std::endl;\n}"
            },
            {
                "type": "code",
                "content": "// Реализация очереди\nvoid demonstrateQueue() {\n    std::queue<int> q;\n    q.push(1);\n    q.push(2);\n    q.push(3);\n    \n    std::cout << \"Queue (FIFO): \";\n    while (!q.empty()) {\n        std::cout << q.front() << \" \";\n        q.pop();\n    }\n    std::cout << std::endl;\n}"
            },
            {
                "type": "code",
                "content": "// Бинарное дерево поиска\nstruct TreeNode {\n    int val;\n    TreeNode* left;\n    TreeNode* right;\n    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}\n};\n\nvoid inorderTraversal(TreeNode* root) {\n    if (root) {\n        inorderTraversal(root->left);\n        std::cout << root->val << \" \";\n        inorderTraversal(root->right);\n    }\n}\n\nTreeNode* insert(TreeNode* root, int val) {\n    if (!root) return new TreeNode(val);\n    if (val < root->val) root->left = insert(root->left, val);\n    else root->right = insert(root->right, val);\n    return root;\n}"
            },
            {
                "type": "code",
                "content": "// Демонстрация использования\nint main() {\n    demonstrateStack();\n    demonstrateQueue();\n    \n    // Дерево\n    TreeNode* root = nullptr;\n    std::vector<int> values = {5, 3, 7, 2, 4, 6, 8};\n    for (int val : values) {\n        root = insert(root, val);\n    }\n    std::cout << \"Inorder traversal: \";\n    inorderTraversal(root);\n    std::cout << std::endl;\n    \n    return 0;\n}"
            }
        ]
    })

    # SQL
    demo_snippets.append({
        "title": "SQL CRUD операции",
        "language": "sql",
        "tags": "sql,database,crud",
        "cells": [
            {
                "type": "markdown",
                "content": "## SQL: Основные CRUD операции\nCreate, Read, Update, Delete"
            },
            {
                "type": "code",
                "content": "/* Создание таблицы */\nCREATE TABLE employees (\n    id INT PRIMARY KEY AUTO_INCREMENT,\n    first_name VARCHAR(50) NOT NULL,\n    last_name VARCHAR(50) NOT NULL,\n    email VARCHAR(100) UNIQUE,\n    department VARCHAR(50),\n    salary DECIMAL(10, 2),\n    hire_date DATE\n);"
            },
            {
                "type": "code",
                "content": "/* CREATE - Вставка данных */\nINSERT INTO employees (first_name, last_name, email, department, salary, hire_date)\nVALUES \n    ('John', 'Doe', 'john.doe@company.com', 'Engineering', 75000.00, '2023-01-15'),\n    ('Jane', 'Smith', 'jane.smith@company.com', 'Marketing', 65000.00, '2023-02-20'),\n    ('Mike', 'Johnson', 'mike.johnson@company.com', 'Engineering', 80000.00, '2023-03-10');"
            },
            {
                "type": "code",
                "content": "/* READ - Выборка данных */\n-- Все сотрудники\nSELECT * FROM employees;\n\n-- Сотрудники из Engineering\nSELECT first_name, last_name, salary \nFROM employees \nWHERE department = 'Engineering';\n\n-- Сотрудники с зарплатой > 70000\nSELECT * FROM employees WHERE salary > 70000 ORDER BY salary DESC;\n\n-- Подсчет сотрудников по отделам\nSELECT department, COUNT(*) as employee_count \nFROM employees \nGROUP BY department;"
            },
            {
                "type": "code",
                "content": "/* UPDATE - Обновление данных */\n-- Повышение зарплаты сотрудника\nUPDATE employees \nSET salary = salary * 1.10 \nWHERE id = 1;\n\n-- Смена отдела\nUPDATE employees \nSET department = 'Data Science' \nWHERE email = 'john.doe@company.com';\n\n/* DELETE - Удаление данных */\n-- Удаление по условию\nDELETE FROM employees WHERE salary < 60000;\n\n-- Удаление конкретного сотрудника\nDELETE FROM employees WHERE id = 3;"
            }
        ]
    })

    return demo_snippets


def test_database():
    try:
        db = Database()
        print("DEBUG: БД инициализирована")
    except Exception as e:
        print(f"DEBUG: Ошибка инициализации БД: {e}")
        return

    print("Тест 1: Получить существующие сниппеты")
    snippets = db.get_snippets()
    print(f"Найдено сниппетов: {len(snippets)}")

    print("\nТест 2: Добавление демо-данных")
    demo_snippets = create_demo_data()

    added_count = 0
    for snippet in demo_snippets:
        try:
            snippet_id = db.add_snippet(
                snippet["title"],
                snippet["language"],
                snippet["cells"],
                snippet["tags"]
            )
            print(f"✅ Добавлен: {snippet['title']} (ID: {snippet_id})")
            added_count += 1
        except Exception as e:
            print(f"❌ Ошибка при добавлении '{snippet['title']}': {e}")

    print(f"\nУспешно добавлено {added_count} демо-сниппетов")

    print("\nТест 3: Проверка итогового количества")
    snippets = db.get_snippets()
    print(f"Итого сниппетов в базе: {len(snippets)}")

    print("\nСписок всех сниппетов:")
    for s in snippets:
        print(f"ID: {s['id']}, Title: {s['title']}, Language: {s['language']}, Tags: {s['tags']}")

    db.close()


if __name__ == "__main__":
    test_database()