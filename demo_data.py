"""
Script to create demo data for CodeSnippet Hub
"""
import sys
import os

# Add src directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database import Database

def create_demo_data():
    """Create sample snippets for demonstration."""
    print("Creating demo data for CodeSnippet Hub...")
    
    db = Database("snippets.db")  # Use the same database as the app
    
    # Sample snippets
    snippets = [
        {
            "title": "Python List Comprehension",
            "language": "python",
            "code": "# Create a list of squares for even numbers\nsquares = [x**2 for x in range(10) if x % 2 == 0]\nprint(squares)\n# Output: [0, 4, 16, 36, 64]"
        },
        {
            "title": "JavaScript Array Filter",
            "language": "javascript",
            "code": "// Filter even numbers from an array\nconst numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];\nconst evenNumbers = numbers.filter(num => num % 2 === 0);\nconsole.log(evenNumbers);\n// Output: [2, 4, 6, 8, 10]"
        },
        {
            "title": "Bubble Sort Algorithm",
            "language": "python",
            "code": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]\n    return arr\n\n# Example usage\ndata = [64, 34, 25, 12, 22, 11, 90]\nsorted_data = bubble_sort(data.copy())\nprint(f\"Original: {data}\")\nprint(f\"Sorted: {sorted_data}\")"
        },
        {
            "title": "SQL Query Example",
            "language": "sql",
            "code": "-- Get all users with their order counts\nSELECT \n    u.id,\n    u.name,\n    u.email,\n    COUNT(o.id) as order_count\nFROM users u\nLEFT JOIN orders o ON u.id = o.user_id\nGROUP BY u.id, u.name, u.email\nHAVING COUNT(o.id) > 0\nORDER BY order_count DESC;"
        },
        {
            "title": "HTML Structure",
            "language": "html",
            "code": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>Document</title>\n</head>\n<body>\n    <header>\n        <h1>Welcome</h1>\n    </header>\n    <main>\n        <p>This is the main content</p>\n    </main>\n    <footer>\n        <p>Footer content</p>\n    </footer>\n</body>\n</html>"
        },
        {
            "title": "CSS Flexbox Centering",
            "language": "css",
            "code": "/* Center an element both horizontally and vertically */\n.container {\n    display: flex;\n    justify-content: center;\n    align-items: center;\n    height: 100vh;\n}\n\n/* Alternative method */\n.centered {\n    position: absolute;\n    top: 50%;\n    left: 50%;\n    transform: translate(-50%, -50%);\n}"
        }
    ]
    
    # Add snippets to database
    for snippet in snippets:
        db.add_snippet(snippet["title"], snippet["language"], snippet["code"])
        print(f"✓ Added: {snippet['title']}")
    
    print(f"\n✓ Added {len(snippets)} demo snippets to the database!")
    print("You can now run the application with: uv run python src/main.py")
    
    db.close()

if __name__ == "__main__":
    create_demo_data()