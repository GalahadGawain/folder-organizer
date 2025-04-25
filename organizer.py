import argparse
import datetime
import os
import shutil
import traceback
from typing import Dict, List
from tqdm import tqdm
from pathlib import Path
import unittest

# =============== CONFIGURATION ===============
# Default directory to organize
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(DIRECTORY, "file_organizer_log.txt")  # Log file path

# File extension mapping (category -> list of extensions)
EXTENSION_MAP: Dict[str, List[str]] = {
    "Documents": ["pdf", "doc", "docx", "odt", "rtf", "tex", "txt", "wpd", "pages"],
    "Spreadsheets": ["xls", "xlsx", "xlsm", "ods", "csv"],
    "Presentations": ["ppt", "pptx", "odp", "key"],
    "Images": ["png", "jpg", "jpeg", "gif", "bmp", "svg", "webp", "tiff", "ico", "heic"],
    "Videos": ["mp4", "mov", "avi", "flv", "wmv", "mkv", "webm", "m4v", "mpg", "mpeg", "3gp"],
    "Audio": ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a", "aiff", "mid", "midi"],
    "Archives": ["zip", "rar", "7z", "tar", "gz", "bz2", "iso"],
    "Executables": ["exe", "msi", "bat", "sh", "app", "apk", "dmg"],
    "Code": ["py", "js", "html", "css", "java", "cpp", "c", "h", "php", "swift", "json", "xml", "sql", "rb", "go", "kt", "ts"],
    "Design": ["ai", "ps", "eps", "xd", "fig", "indd", "cdr", "sketch"],
    "Ebooks": ["epub", "mobi", "azw", "azw3", "fb2"],
    "Fonts": ["ttf", "otf", "woff", "woff2", "eot"],
    "System": ["dll", "sys", "ini", "cfg"],
    "Torrents": ["torrent"],
    "Logs": ["log", "txtlog"],
    "Temp Files": ["tmp", "bak", "old"],
    "Config Files": ["yml", "yaml", "toml", "env", "conf", "properties"],
    "Game Files": ["unitypackage", "asset", "prefab", "material"],
    "CAD Files": ["stl", "obj", "fbx", "dae", "3ds"],
    "Scripts": ["sh", "bat", "ps1", "cmd"],
    "Database": ["db", "sqlite", "mdb", "accdb"],
    "Web Files": ["html", "css", "js", "php", "xml"],
    "Other": []  # Catch-all for unrecognized extensions
}

# Reverse mapping for faster lookup (extension -> category)
FILE_EXTENSIONS: Dict[str, str] = {
    ext: category for category, exts in EXTENSION_MAP.items() for ext in exts
}

# Ensure "Other" category exists
EXTENSION_MAP.setdefault("Other", [])

# =============== FUNCTIONS ===============


def write_log(message: str) -> None:
    """Write a message to the log file with a timestamp."""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{timestamp} {message}\n")
    except Exception as e:
        print(f"⚠️ Error writing to log file: {e}")


def create_category_folders(root: str) -> None:
    """Create folders for categories only if files exist for those categories."""
    files = os.listdir(root)
    categories_to_create = set()

    for filename in files:
        if should_skip(os.path.join(root, filename)):
            continue

        if '.' in filename:
            ext = filename.split('.')[-1].lower()
            category = FILE_EXTENSIONS.get(ext, "Other")
            categories_to_create.add(category)

    for category in categories_to_create:
        folder_path = os.path.join(root, category)
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                write_log(f"Created folder: {category}")
            except Exception as e:
                write_log(f"❌ Failed to create {category}: {str(e)}")


def should_skip(filepath: str) -> bool:
    """Determine if a file should be skipped (e.g., hidden, temporary, or a directory)."""
    filename = os.path.basename(filepath)
    return (
        os.path.isdir(filepath) or
        filename == os.path.basename(LOG_FILE) or
        filename.startswith('.') or  # Hidden files
        filename.startswith('~')     # Temporary files
    )


def move_file(filepath: str, category: str, target_dir: str) -> None:
    """Move a file to the target directory, appending '_copy' if a file with the same name exists."""
    filename = os.path.basename(filepath)
    target_path = Path(target_dir) / filename

    # Handle duplicate filenames
    if target_path.exists():
        target_path = target_path.with_stem(f"{target_path.stem}_copy")

    DRY_RUN = False  # Set to False to actually move files

    if DRY_RUN:
        write_log(f"🔍 Dry-run: Would move {filename} → {category}/")
    else:
        shutil.move(filepath, str(target_path))
        write_log(f"✅ Moved: {filename} → {category}/")


def organize_files(root: str) -> None:
    """Organize files in the specified directory into categorized subfolders."""
    start_time = datetime.datetime.now()
    write_log(f"\n{'='*50}")
    write_log(f"🚀 Starting file organization in: {root}")
    write_log(f"⏰ Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    write_log(f"{'='*50}\n")

    create_category_folders(root)

    moved_count = 0
    skipped_count = 0
    error_count = 0

    files = os.listdir(root)

    for filename in tqdm(files, desc="📦 Organizing files", unit="file"):
        filepath = os.path.join(root, filename)

        if should_skip(filepath):
            skipped_count += 1
            continue

        if '.' in filename:
            ext = filename.split('.')[-1].lower()
            category = FILE_EXTENSIONS.get(ext, "Other")

            try:
                target_dir = os.path.join(root, category)
                move_file(filepath, category, target_dir)
                moved_count += 1
            except Exception as e:
                write_log(f"❌ Failed to move {filename}: {str(e)}")
                write_log(traceback.format_exc())
                error_count += 1
        else:
            write_log(f"⚠️ No extension: {filename}")
            skipped_count += 1

    # Summary
    duration = datetime.datetime.now() - start_time
    summary = f"""
📊 Organization Summary:
• Files moved: {moved_count}
• Files skipped: {skipped_count}
• Errors: {error_count}
• Duration: {duration.total_seconds():.2f} seconds
"""
    print(summary)
    write_log(summary)
    write_log(f"{'='*50}\n")


# =============== MAIN EXECUTION ===============
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize files in a directory.")
    parser.add_argument("--directory", type=str,
                        default=DIRECTORY, help="Directory to organize")
    parser.add_argument("--log", type=str, default=LOG_FILE,
                        help="Log file path")
    args = parser.parse_args()

    print(f"\n📁 Organizing files in: {args.directory}")
    print("⚙️  Check the log file for details:", args.log)

    try:
        organize_files(args.directory)
        print("✅ File organization completed successfully!")
    except Exception as e:
        print(f"❌ Error during organization: {str(e)}")
        write_log(f"CRITICAL ERROR: {str(e)}")

    print(f"📋 Log file created at: {args.log}\n")


# =============== UNIT TESTS ===============
class TestFileOrganizer(unittest.TestCase):
    def test_should_skip(self):
        self.assertTrue(should_skip(".hidden_file"))
        self.assertFalse(should_skip("document.pdf"))
