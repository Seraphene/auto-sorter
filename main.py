import shutil
import logging
import time
import signal
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("auto_sorter.log"),
        logging.StreamHandler()
    ]
)

# Configuration
DOWNLOAD_FOLDER = Path.home() / "Downloads"
POLLING_INTERVAL = 60  # seconds
DESTINATIONS = {
    "Pictures": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"},
    "Documents": {".pdf", ".docx", ".txt", ".pptx", ".xlsx", ".csv", ".md"},
    "Audio": {".mp3", ".wav", ".aac", ".flac"},
    "Video": {".mp4", ".mov", ".avi", ".mkv"},
    "Archives": {".zip", ".rar", ".7z", ".tar.gz"},
    "Scripts": {".py", ".js", ".sh", ".bat"},
}

def get_destination_folder(extension):
    """Returns the target folder name for a given file extension."""
    for folder, extensions in DESTINATIONS.items():
        if extension.lower() in extensions:
            return folder
    return "Others"

def move_file(source_path):
    """Moves a file to the appropriate destination folder with collision handling."""
    extension = source_path.suffix
    dest_name = get_destination_folder(extension)
    dest_folder = source_path.parent / dest_name
    
    # Create destination folder if it doesn't exist
    dest_folder.mkdir(exist_ok=True)
    
    target_path = dest_folder / source_path.name
    
    # Handle filename collision
    counter = 1
    while target_path.exists():
        stem = source_path.stem
        target_path = dest_folder / f"{stem}_{counter}{extension}"
        counter += 1
        
    try:
        shutil.move(str(source_path), str(target_path))
        logging.info(f"Moved: {source_path.name} -> {dest_name}/{target_path.name}")
    except Exception as e:
        logging.error(f"Failed to move {source_path.name}: {e}")

def organize_downloads():
    """Scans and organizes the download folder once."""
    if not DOWNLOAD_FOLDER.exists():
        logging.error(f"Download folder {DOWNLOAD_FOLDER} does not exist.")
        return

    files_moved = 0
    for item in DOWNLOAD_FOLDER.iterdir():
        # Skip directories and hidden files
        if item.is_file() and not item.name.startswith('.'):
            move_file(item)
            files_moved += 1
            
    if files_moved > 0:
        logging.info(f"Scan complete. Total files moved: {files_moved}")

def signal_handler(sig, frame):
    logging.info("Shutting down auto-sorter...")
    sys.exit(0)

def main():
    # Handle Ctrl+C and other termination signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logging.info(f"Auto-sorter started. Monitoring {DOWNLOAD_FOLDER} every {POLLING_INTERVAL}s...")
    
    while True:
        try:
            organize_downloads()
            time.sleep(POLLING_INTERVAL)
        except Exception as e:
            logging.error(f"Unexpected error in main loop: {e}")
            time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    main()
