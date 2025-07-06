# File Management Tool

A cross-platform (Windows/Linux) file management utility for large collections of video and PDF files. Features both a practical GUI (Windows) and a CLI (Linux/macOS).

## Features
- List unique file titles (without extensions)
- Batch rename or remove text from filenames using regex
- Organize files by creation date
- Detect duplicate filenames (ignoring extension)
- Undo last rename/move
- Backup files (excluding subdirectories)
- GUI for Windows, CLI for Linux/macOS

## Usage

### Windows (GUI)
1. Run: `python3 main.py`
2. Use the GUI to select a folder, enter regex, and manage files.

### Linux/macOS (CLI)
1. Run: `python3 main.py`
2. Follow the prompts to select a folder and manage files.

### Unit Tests
Run all tests:
```
python3 test_file_manager.py
```

## Project Structure
- `main.py` — Entry point, chooses GUI or CLI
- `cli.py` — Command-line interface
- `gui.py` — Tkinter GUI
- `file_ops.py` — File management logic
- `utils.py` — Config, logging, helpers
- `test_file_manager.py` — Unit tests

## Requirements
- Python 3.x
- Tkinter (standard with most Python installations)

## Notes
- Backups do not include subdirectories.
- Undo only supports the last action.
- All output is formatted for clarity (filenames only, not full paths).
