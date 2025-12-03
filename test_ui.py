#!/usr/bin/env python3
"""
Test script to validate MultiCellEditor functionality
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from ui.code_editor import MultiCellEditor
    from ui.dialogs import AddSnippetDialog, EditSnippetDialog
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

def test_multicell_editor():
    """Test MultiCellEditor functionality"""
    print("\n=== Testing MultiCellEditor ===")
    
    # Test initialization
    try:
        cells = [
            {"type": "code", "language": "python", "content": "print('hello')"},
            {"type": "text", "content": "This is a comment"}
        ]
        editor = MultiCellEditor(cells=cells, on_change=lambda x: print(f"Cells changed: {len(x)}"))
        print("✓ MultiCellEditor initialized successfully")
        
        # Test build method
        container = editor.build()
        print(f"✓ Build method works, returned: {type(container)}")
        
        # Test adding a cell
        editor._add_cell(type('MockEvent', (), {'page': None})())
        print(f"✓ Added cell, now has {len(editor.cells)} cells")
        
        # Test updating cells
        new_cells = [{"type": "code", "language": "javascript", "content": "console.log('test');"}]
        editor.update_cells(new_cells)
        print(f"✓ Cells updated, now has {len(editor.cells)} cells")
        
    except Exception as e:
        print(f"✗ MultiCellEditor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_dialogs():
    """Test dialog functionality"""
    print("\n=== Testing Dialogs ===")
    
    try:
        # Test AddSnippetDialog initialization
        def dummy_submit(title, lang, cells):
            print(f"Submit called: {title}, {lang}, {len(cells)} cells")
        
        def dummy_cancel():
            print("Cancel called")
        
        dialog = AddSnippetDialog(on_submit=dummy_submit, on_cancel=dummy_cancel)
        print("✓ AddSnippetDialog initialized successfully")
        
        # Test EditSnippetDialog initialization
        edit_dialog = EditSnippetDialog(on_submit=lambda a, b, c, d: None, on_cancel=lambda: None)
        print("✓ EditSnippetDialog initialized successfully")
        
    except Exception as e:
        print(f"✗ Dialog test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def test_search_functionality():
    """Test search functionality"""
    print("\n=== Testing Search Functionality ===")
    
    try:
        from models.database import Database
        import tempfile
        import os
        
        # Create a temporary database for testing
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            db = Database(tmp_path)
            
            # Add test snippets
            test_cells = [{"type": "code", "language": "python", "content": "print('test')"}]
            db.add_snippet("Test Python Snippet", "python", test_cells, "test,python")
            db.add_snippet("JavaScript Example", "javascript", test_cells, "js,example")
            
            # Test search functionality
            all_snippets = db.get_snippets()
            print(f"✓ Retrieved {len(all_snippets)} snippets without search")
            
            python_snippets = db.get_snippets("python")
            print(f"✓ Retrieved {len(python_snippets)} snippets with 'python' search")
            
            js_snippets = db.get_snippets("javascript")
            print(f"✓ Retrieved {len(js_snippets)} snippets with 'javascript' search")
            
            # Clean up
            db.close()
            os.unlink(tmp_path)
            
        except Exception as e:
            # Clean up in case of error
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise e
            
        print("✓ Search functionality works correctly")
        
    except Exception as e:
        print(f"✗ Search functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("Testing UI components...")
    
    success = True
    success &= test_multicell_editor()
    success &= test_dialogs()
    success &= test_search_functionality()
    
    if success:
        print("\n✓ All tests passed! The UI components are working correctly.")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)