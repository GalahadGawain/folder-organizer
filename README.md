# File Organizer Script

A Python script to automatically organize files in a directory into categorized subfolders based on their file extensions. This tool helps maintain a clean and structured directory, making files easier to locate.

---

## 🚀 Features

- **Automatic Categorization:** Sorts files into predefined categories like Documents, Images, Videos, Audio, Archives, Code, etc.
- **Customizable Categories:** Easily modify or extend the `EXTENSION_MAP` dictionary to add new categories or file types.
- **Folder Creation:** Automatically creates category folders only if files exist for those categories.
- **"Other" Category:** Files with unrecognized extensions are moved to a dedicated "Other" folder.
- **Intelligent Skipping:** Skips directories, hidden files (starting with `.`), temporary files (starting with `~`), and the script's own log file.
- **Detailed Logging:** Logs all actions (folder creation, file movements, errors, skips) with timestamps in a `file_organizer_log.txt` file.
- **Progress Bar:** Displays a progress bar using `tqdm` to track the organization process.
- **Dry-Run Mode:** Simulate the organization process without moving files (for preview purposes).
- **Configurable Directory:** Organize files in any directory by specifying it as a command-line argument.

---

## 🛠️ Installation

1. **Prerequisites:** Ensure you have Python 3 installed on your system.
2. **Clone or Download:** Clone this repository or download the `organizer.py` script to your local machine.
3. **Install Dependencies:** Install the required library `tqdm` using pip:
   ```bash
   pip install tqdm
   ```

---

## 📖 Usage

1. **Navigate to the Script Directory:**
   Open your terminal or command prompt and navigate to the directory where you saved the `organizer.py` script.

2. **Run the Script:**
   Execute the script using Python:

   ```bash
   python organizer.py
   ```

3. **Optional Arguments:**

   - Specify a custom directory to organize:
     ```bash
     python organizer.py --directory "C:\path\to\your\directory"
     ```
   - Specify a custom log file path:
     ```bash
     python organizer.py --log "C:\path\to\log_file.txt"
     ```

4. **Monitor Progress:**
   - View the progress bar in the terminal.
   - Check the `file_organizer_log.txt` file for detailed logs.

---

## ⚙️ Configuration

You can customize the script by modifying the configuration variables at the top of the `organizer.py` file:

### 1. **Target Directory**

Change the `DIRECTORY` variable to specify a default directory to organize:

```python
DIRECTORY = "C:\\Users\\YourUser\\Desktop"  # Example for Windows
```

### 2. **Log File Path**

Modify the `LOG_FILE` variable to change the log file's location or name:

```python
LOG_FILE = os.path.join(DIRECTORY, "custom_log_file.txt")
```

### 3. **File Categories**

Update the `EXTENSION_MAP` dictionary to add or modify categories and their associated file extensions:

```python
EXTENSION_MAP: Dict[str, List[str]] = {
    "CAD Files": ["dwg", "dxf", "stl"],  # Example: Adding a new category
}
```

_Note: The reverse mapping (`FILE_EXTENSIONS`) is automatically generated from `EXTENSION_MAP`._

### 4. **Dry-Run Mode**

By default, the script runs in "dry-run" mode, meaning no files are actually moved. To disable this and move files, set the `DRY_RUN` variable in the `move_file` function to `False`:

```python
DRY_RUN = False  # Set to True for dry-run mode
```

---

## 📋 Logging

The script generates a log file (`file_organizer_log.txt`) in the target directory. The log includes:

- **Start and End Times:** Timestamps for when the script starts and finishes.
- **Folder Creation Logs:** Confirmation of category folder creation.
- **File Movement Logs:** Details of each file moved and its destination category.
- **Skipped Files:** Notes on skipped files (e.g., hidden, temporary, or without extensions).
- **Errors:** Details of any errors encountered during file operations.
- **Summary Report:** A summary of the number of files moved, skipped, errors encountered, and the total duration.

---

## 🧪 Testing

The script includes basic unit tests for key functions. To run the tests, use:

```bash
python -m unittest organizer.py
```

---

## 📊 Example Output

### Terminal Output:

```plaintext
📁 Organizing files in: C:\Users\YourUser\Desktop
⚙️  Check the log file for details: file_organizer_log.txt
📦 Organizing files: 100%|████████████████████████████████████████| 50/50 [00:05<00:00, 10.00 files/s]
✅ File organization completed successfully!
📋 Log file created at: file_organizer_log.txt
```

### Log File (`file_organizer_log.txt`):

```plaintext
[2025-04-25 10:00:00] 🚀 Starting file organization in: C:\Users\YourUser\Desktop
[2025-04-25 10:00:01] Created folder: Documents
[2025-04-25 10:00:02] ✅ Moved: report.pdf → Documents/
[2025-04-25 10:00:03] ⚠️ No extension: README
[2025-04-25 10:00:05] 📊 Organization Summary:
• Files moved: 45
• Files skipped: 5
• Errors: 0
• Duration: 5.00 seconds
```

---

## 📝 Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or find any bugs, feel free to open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
