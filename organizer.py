import datetime
import os
import shutil
from typing import Dict, List
from tqdm import tqdm

# =============== CONFIGURATION ===============
# Directory to organize (default: script's location)
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Log file path
LOG_FILE = os.path.join(DIRECTORY, "file_organizer_log.txt")

# File extension mapping (category -> list of extensions)
EXTENSION_MAP: Dict[str, List[str]] = {
    # Documents
    "Documents": ["pdf", "doc", "docx", "odt", "rtf", "tex", "txt", "wpd", "pages"],
    
    # Spreadsheets
    "Spreadsheets": ["xls", "xlsx", "xlsm", "ods", "csv", "numbers"],
    
    # Presentations
    "Presentations": ["ppt", "pptx", "odp", "key"],
    
    # Images
    "Images": ["png", "jpg", "jpeg", "gif", "bmp", "svg", "webp", "psd", "tiff", 
               "raw", "ico", "heic", "cr2", "nef", "orf", "sr2"],
    
    # Videos
    "Videos": ["mp4", "mov", "avi", "flv", "wmv", "mkv", "webm", "m4v", "mpg", 
               "mpeg", "3gp", "m2ts", "mts", "vob"],
    
    # Audio
    "Audio": ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a", "aiff", "mid", 
              "midi", "opus", "amr"],
    
    # Archives
    "Archives": ["zip", "rar", "7z", "tar", "gz", "bz2", "iso", "xz", "z", "lz", 
                 "pkg", "deb", "rpm"],
    
    # Executables
    "Executables": ["exe", "msi", "bat", "sh", "app", "apk", "dmg", "pkg", "run"],
    
    # Code
    "Code": ["py", "js", "html", "css", "java", "cpp", "c", "h", "php", "swift", 
             "json", "xml", "sql", "rb", "go", "kt", "ts", "sh", "pl", "lua", 
             "r", "m", "asm", "s", "hs", "scala"],
    
    # Design
    "Design": ["skp", "skf", "ai", "ps", "eps", "xd", "fig", "indd", "cdr", "afdesign", 
               "sketch", "psb", "blend", "max", "ma", "mb", "dwg", "dxf"],
    
    # Database
    "Database": ["db", "sqlite", "mdb", "accdb", "frm", "sqlitedb", "nsf", "kdbx"],
    
    # Ebooks
    "Ebooks": ["epub", "mobi", "azw", "azw3", "fb2", "ibooks"],
    
    # Fonts
    "Fonts": ["ttf", "otf", "woff", "woff2", "eot", "pfa", "pfb", "sfd"],
    
    # System Files
    "System": ["dll", "sys", "ini", "cfg", "inf", "msi", "cat", "drv", "cur", "deskthemepack"],
    
    # Virtual Machines
    "Virtual Machines": ["vdi", "vmdk", "ova", "ovf", "vhd", "vhdx", "nvram"],
    
    # Torrents
    "Torrents": ["torrent"],
    
    # Logs
    "Logs": ["log", "logs", "txtlog", "eventlog"],
    
    # Temporary Files
    "Temp Files": ["tmp", "temp", "bak", "backup", "old"],
    
    # Config Files
    "Config Files": ["yml", "yaml", "toml", "env", "conf", "config", "properties"],
    
    # Game Files
    "Game Files": ["unitypackage", "asset", "prefab", "material", "anim", "controller"],
    
    # CAD Files
    "CAD Files": ["stl", "obj", "fbx", "dae", "3ds", "iges", "step", "stp"]
}

# Reverse mapping for faster lookup (extension -> category)
FILE_EXTENSIONS: Dict[str, str] = {
    ext: category for category, exts in EXTENSION_MAP.items() for ext in exts
}


# Add "Other" category for unrecognized extensions
if "Other" not in EXTENSION_MAP:
    EXTENSION_MAP["Other"] = []

# =============== FUNCTIONS ===============
def write_log(message: str) -> None:
    """Write a message to the log file with timestamp."""
    timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"{timestamp} {message}\n")
    except Exception as e:
        print(f"⚠️ Error writing to log file: {e}")

def create_category_folders(root: str) -> None:
    """Create all category folders if they don't exist."""
    for category in EXTENSION_MAP.keys():
        folder_path = os.path.join(root, category)
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                write_log(f"Created folder: {category}")
            except Exception as e:
                write_log(f"❌ Failed to create {category}: {str(e)}")

def should_skip(filepath: str) -> bool:
    """Check if a file should be skipped during organization."""
    filename = os.path.basename(filepath)
    return (
        os.path.isdir(filepath) or
        filename == os.path.basename(LOG_FILE) or
        filename.startswith('.') or  # Hidden files
        filename.startswith('~')     # Temporary files
    )

def organize_files(root: str) -> None:
    """Main function to organize files in the specified directory."""
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
    
    for filename in tqdm(files, desc="📦 Organizing files"):
        filepath = os.path.join(root, filename)
        
        if should_skip(filepath):
            skipped_count += 1
            continue
        
        if '.' in filename:
            ext = filename.split('.')[-1].lower()
            category = FILE_EXTENSIONS.get(ext, "Other")
            
            try:
                target_dir = os.path.join(root, category)
                shutil.move(filepath, os.path.join(target_dir, filename))
                write_log(f"✅ Moved: {filename} → {category}/")
                moved_count += 1
            except Exception as e:
                write_log(f"❌ Failed to move {filename}: {str(e)}")
                error_count += 1
        else:
            write_log(f"⚠️ No extension: {filename}")
            skipped_count += 1
    
    # Summary
    duration = datetime.datetime.now() - start_time
    write_log(f"\n{'='*50}")
    write_log("📊 Organization Summary:")
    write_log(f"• 📂 Files moved: {moved_count}")
    write_log(f"• ⏭️ Files skipped: {skipped_count}")
    write_log(f"• ❌ Errors: {error_count}")
    write_log(f"• ⏱️ Duration: {duration.total_seconds():.2f} seconds")
    write_log(f"{'='*50}\n")

# =============== MAIN EXECUTION ===============
if __name__ == "__main__":
    print(f"\n📁 Organizing files in: {DIRECTORY}")
    print("⚙️  Check the log file for details:", LOG_FILE)
    
    try:
        organize_files(DIRECTORY)
        print("✅ File organization completed successfully!")
    except Exception as e:
        print(f"❌ Error during organization: {str(e)}")
        write_log(f"CRITICAL ERROR: {str(e)}")
    
    print(f"📋 Log file created at: {LOG_FILE}\n")