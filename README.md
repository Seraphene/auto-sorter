# auto-sorter: Automated File Organization System

## Overview
The **auto-sorter** is a Python-based utility designed to automate the organization of files within a local machine, specifically targeting the `Downloads` folder. It scans the directory, identifies file types by their extensions, and moves them to pre-defined destination folders (e.g., Pictures, Documents, Videos).

## System Analysis

### 1. Core Logic
- **Directory Scanning**: The system monitors a target directory (default: `C:/Users/Lenovo/Downloads`).
- **File Categorization**: Files are classified into categories based on their extensions:
    - **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`
    - **Documents**: `.pdf`, `.docx`, `.txt`, `.pptx`, `.xlsx`
    - **Audio**: `.mp3`, `.wav`, `.aac`, `.flac`
    - **Video**: `.mp4`, `.mov`, `.avi`, `.mkv`
    - **Archives**: `.zip`, `.rar`, `.7z`, `.tar.gz`
- **File Operations**: Uses Python's `pathlib` and `shutil` libraries to perform safe file moves across the filesystem.

### 2. Robustness Features
- **Collision Handling**: If a file with the same name already exists in the destination, the system appends a numeric suffix (e.g., `image.png` -> `image_1.png`) to prevent data loss.
- **Error Handling**: Implements try-except blocks to catch filesystem errors, permission issues, or file-in-use scenarios.
- **Directory Management**: Automatically creates destination folders if they do not exist.

### 3. Architecture
The system is built as a modular script with the following components:
- `move_file(path, destination)`: Handles the logic of moving a single file, including collision checks.
- `get_destination(extension)`: Maps file extensions to their respective target folders.
- `main()`: The entry point that iterates through the download folder and orchestrates the sorting process.

### 4. Setup and Usage
1. Ensure Python 3.x is installed.
2. Configure the `POLLING_INTERVAL` in `main.py` (default: 60 seconds).
3. Run the script: `python main.py`.

## Running in the Background (Windows)

To have the auto-sorter run silently in the background without a command prompt window:

### Method 1: Using pythonw
Rename `main.py` to `main.pyw` or run it using `pythonw`:
```powershell
pythonw main.py
```

### Method 2: Windows Startup
To ensure the script starts automatically when you log in:
1. Press `Win + R`, type `shell:startup`, and press Enter.
2. Create a shortcut to `main.py` (or a batch file that runs it with `pythonw`).
3. Place the shortcut in the Startup folder.

## Logs
The system maintains a log file named `auto_sorter.log` in the project directory to track file movements and errors.

## Future Enhancements
- Support for customizable configuration files (JSON/YAML).
- Advance sorting rules (e.g., by date or file size).
