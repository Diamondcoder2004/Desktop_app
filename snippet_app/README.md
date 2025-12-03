# Snippet Manager Desktop Application

This is a desktop application built with PyQt5 for managing code snippets.

## Features

- Add, edit, and delete code snippets
- Search through your snippets
- Copy snippet content to clipboard
- Organize snippets with titles and language tags
- Persistent storage using SQLite

## Requirements

- Python 3.7+
- PyQt5

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application:

```bash
python main.py
```

Note: This application requires a graphical environment to run. If you're running it in a headless environment (like a server without a display), you might need to use X11 forwarding or a virtual display.

## Troubleshooting

If you get a Qt platform plugin error, try installing additional system dependencies:

```bash
# On Ubuntu/Debian
sudo apt-get install python3-pyqt5

# On CentOS/RHEL
sudo yum install python3-qt5
```

## Logging

The application creates a log file `snippet_app.log` in the same directory that records all operations for debugging purposes.