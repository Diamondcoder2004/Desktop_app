#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))  # src выше

try:
    from src.models.database import Database
    from src.ui.components import CellEditor, SnippetEditor
    from src.ui.dialogs import AddSnippetDialog, EditSnippetDialog
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def test_cell_editor():
    print("\n=== Testing CellEditor ===")
    try:
        editor = CellEditor({"type": "markdown", "content": "# Header"})
        print("✓ Initialized")
        editor._update_preview(None)  # Тест preview
        print("✓ Preview updated")
        data = editor.get_cell_data()
        assert data['type'] == "markdown"
        print("✓ Get data works")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    return True

def test_snippet_editor():
    print("\n=== Testing SnippetEditor ===")
    try:
        snippet = {"id": 1, "title": "Test", "language": "python", "cells": [{"type": "code", "content": "print()"}], "tags": "test"}
        editor = SnippetEditor(snippet=snippet)
        print("✓ Initialized")
        data = editor.get_snippet_data()
        assert data['title'] == "Test"
        print("✓ Get data works")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    return True

def test_dialogs():
    print("\n=== Testing Dialogs ===")
    try:
        add_dialog = AddSnippetDialog(on_submit=lambda *args: None, on_cancel=lambda: None)
        print("✓ AddDialog init")
        edit_dialog = EditSnippetDialog(on_quick_save=lambda *args: None, on_full_edit=lambda: None, on_cancel=lambda: None)
        print("✓ EditDialog init")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    return True

def test_search_functionality():
    print("\n=== Testing Search Functionality ===")
    try:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.db') as tmp:
            db = Database(tmp.name)
            test_cells = [{"type": "code", "content": "test"}]
            db.add_snippet("Python Test", "python", test_cells, "python")
            db.add_snippet("JS Test", "javascript", test_cells, "js")
            snippets = db.get_snippets("python")
            assert len(snippets) == 1
            print("✓ Search works")
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False
    return True

if __name__ == "__main__":
    success = True
    success &= test_cell_editor()
    success &= test_snippet_editor()
    success &= test_dialogs()
    success &= test_search_functionality()
    if success:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Failed!")
        sys.exit(1)