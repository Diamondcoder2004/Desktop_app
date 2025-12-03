#!/usr/bin/env python3
"""
Desktop application launcher for CodeSnippet Hub.
This script runs the application as a desktop app without web parameters.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main
import flet as ft


def run_desktop_app():
    """Run the CodeSnippet Hub as a desktop application."""
    print("Starting CodeSnippet Hub as Desktop Application...")
    print("No port or web view specified - running as native desktop app")
    
    # Run the application without port or web view parameters
    ft.app(target=main)


if __name__ == "__main__":
    run_desktop_app()