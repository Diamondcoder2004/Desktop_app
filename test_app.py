"""
Simple test script to verify that the CodeSnippet Hub application modules work correctly.
"""
import sys
import os

# Add src directory to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported without errors."""
    print("Testing module imports...")
    
    try:
        from src.database import Database
        print("✓ Database module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Database: {e}")
        return False
    
    try:
        from src.snippet_card import SnippetCard
        print("✓ SnippetCard module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import SnippetCard: {e}")
        return False
    
    try:
        from src.dialogs import AddSnippetDialog, EditSnippetDialog
        print("✓ Dialogs module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Dialogs: {e}")
        return False
    
    try:
        import src.main
        print("✓ Main module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Main: {e}")
        return False
    
    return True

def test_database():
    """Test basic database functionality."""
    print("\nTesting database functionality...")
    
    try:
        from src.database import Database
        
        # Create a temporary database for testing
        db = Database("test_snippets.db")
        print("✓ Database connection established")
        
        # Test adding a snippet
        snippet_id = db.add_snippet("Test Title", "python", "print('Hello World')")
        print(f"✓ Snippet added with ID: {snippet_id}")
        
        # Test retrieving snippets
        snippets = db.get_snippets()
        print(f"✓ Retrieved {len(snippets)} snippet(s)")
        
        # Test updating snippet
        if snippets:
            db.update_snippet(snippet_id, "Updated Title", "javascript", "console.log('Hello');")
            print("✓ Snippet updated successfully")
        
        # Test deleting snippet
        if snippets:
            db.delete_snippet(snippet_id)
            print("✓ Snippet deleted successfully")
        
        # Clean up test database file
        import os
        if os.path.exists("test_snippets.db"):
            os.remove("test_snippets.db")
        
        db.close()
        print("✓ Database test completed successfully")
        
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("Running CodeSnippet Hub tests...\n")
    
    success = True
    
    success &= test_imports()
    success &= test_database()
    
    print(f"\n{'='*50}")
    if success:
        print("✓ All tests passed! CodeSnippet Hub is ready to use.")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    print(f"{'='*50}")
    
    return success

if __name__ == "__main__":
    main()