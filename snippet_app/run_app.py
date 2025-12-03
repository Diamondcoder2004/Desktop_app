#!/usr/bin/env python3
"""
Desktop Snippet Manager Application

This is a PyQt5-based desktop application for managing code snippets.
It provides functionality to add, edit, delete, and search through code snippets.
"""

import sys
import os
import logging

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import main

if __name__ == "__main__":
    print("Snippet Manager Desktop Application")
    print("=====================================")
    print("This is a desktop application that requires a graphical environment.")
    print("")
    print("If running in a headless environment, consider using X11 forwarding or VNC.")
    print("")
    print("Starting application...")
    
    try:
        main()
    except Exception as e:
        logging.error(f"Error starting application: {e}", exc_info=True)
        print(f"Error starting application: {e}")
        sys.exit(1)