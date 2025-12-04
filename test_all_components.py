#!/usr/bin/env python3
"""
Test script to verify all components and identify issues in the application
"""

import sys
import traceback
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test all imports to identify import errors"""
    print("Testing imports...")
    
    modules_to_test = [
        "src.models.database",
        "src.ui.code_editor",
        "src.ui.components", 
        "src.ui.dialogs",
        "src.ui.snippet_card",
        "src.ui.main_view"
    ]
    
    for module_path in modules_to_test:
        try:
            # Import the module
            module_parts = module_path.split('.')
            module = __import__(module_parts[0])
            for part in module_parts[1:]:
                module = getattr(module, part)
            print(f"✓ Successfully imported {module_path}")
        except Exception as e:
            print(f"✗ Failed to import {module_path}: {e}")
            traceback.print_exc()
            print()

def test_database():
    """Test database functionality"""
    print("\nTesting database...")
    try:
        from src.models.database import Database
        db = Database()
        
        # Test basic operations
        result = db.add_snippet("Test", "python", [{"type": "code", "content": "print('hello')"}])
        print(f"✓ Added snippet with ID: {result}")
        
        snippets = db.get_snippets()
        print(f"✓ Retrieved {len(snippets)} snippets")
        
        if snippets:
            db.delete_snippet(snippets[0]['id'])
            print(f"✓ Deleted snippet with ID: {snippets[0]['id']}")
        
        db.close()
        print("✓ Database operations work correctly")
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        traceback.print_exc()

def test_code_editor():
    """Test code editor components"""
    print("\nTesting code editor...")
    try:
        from src.ui.code_editor import MultiCellEditor
        editor = MultiCellEditor()
        print("✓ MultiCellEditor initialized successfully")
        
        # Test get_cells method
        cells = editor.get_cells()
        print(f"✓ get_cells() returned: {cells}")
        
        # Test load_cells method
        test_cells = [{"type": "code", "content": "test"}]
        editor.load_cells(test_cells)
        loaded_cells = editor.get_cells()
        print(f"✓ load_cells() and get_cells() work: {loaded_cells}")
        
    except Exception as e:
        print(f"✗ Code editor test failed: {e}")
        traceback.print_exc()

def test_dialogs():
    """Test dialog components"""
    print("\nTesting dialogs...")
    try:
        from src.ui.dialogs import AddSnippetDialog, EditSnippetDialog
        
        # Test AddSnippetDialog
        def dummy_submit(title, lang, cells, tags):
            print(f"Add dialog submit: {title}, {lang}, {len(cells)} cells, {tags}")
        
        def dummy_cancel():
            print("Add dialog cancel")
            
        add_dialog = AddSnippetDialog(on_submit=dummy_submit, on_cancel=dummy_cancel)
        print("✓ AddSnippetDialog initialized successfully")
        
        # Test EditSnippetDialog
        def dummy_quick_save(title, lang, tags):
            print(f"Edit quick save: {title}, {lang}, {tags}")
        
        def dummy_full_edit():
            print("Edit full edit")
            
        def dummy_edit_cancel():
            print("Edit dialog cancel")
        
        # This should fail due to wrong constructor signature
        edit_dialog = EditSnippetDialog(
            on_quick_save=dummy_quick_save, 
            on_full_edit=dummy_full_edit, 
            on_cancel=dummy_edit_cancel
        )
        print("✓ EditSnippetDialog initialized successfully")
        
    except Exception as e:
        print(f"✗ Dialogs test failed: {e}")
        traceback.print_exc()

def test_snippet_card():
    """Test snippet card component"""
    print("\nTesting snippet card...")
    try:
        from src.ui.snippet_card import SnippetCard
        
        def dummy_copy(code):
            print(f"Copy called with: {code[:20]}...")
        
        def dummy_delete(snippet_id):
            print(f"Delete called for ID: {snippet_id}")
        
        def dummy_edit(snippet_id, title, language, cells):
            print(f"Edit called for ID: {snippet_id}, title: {title}")
        
        card = SnippetCard(
            snippet_id=1,
            title="Test Snippet",
            language="python", 
            cells=[{"type": "code", "content": "print('hello')"}],
            on_copy=dummy_copy,
            on_delete=dummy_delete,
            on_edit=dummy_edit
        )
        print("✓ SnippetCard initialized successfully")
        
        # Test update_content
        card.update_content("Updated Title", "javascript", [{"type": "text", "content": "Hello"}])
        print("✓ SnippetCard.update_content works")
        
    except Exception as e:
        print(f"✗ Snippet card test failed: {e}")
        traceback.print_exc()

def test_main_view():
    """Test main view component"""
    print("\nTesting main view...")
    try:
        from src.ui.main_view import MainView
        from src.models.database import Database
        
        db = Database()
        # This should fail because of the signature mismatch between MainView and SnippetCard
        main_view = MainView(db)
        print("✓ MainView initialized successfully")
        
        db.close()
    except Exception as e:
        print(f"✗ MainView test failed: {e}")
        traceback.print_exc()

def main():
    print("Running comprehensive test of all components...")
    print("="*50)
    
    test_imports()
    test_database()
    test_code_editor()
    test_dialogs()
    test_snippet_card()
    test_main_view()
    
    print("\n" + "="*50)
    print("Test completed. Check for any errors above.")

if __name__ == "__main__":
    main()