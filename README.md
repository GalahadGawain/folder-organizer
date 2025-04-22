# File Organizer Script

A Python script designed to automatically organize files within a specified directory into categorized subfolders based on their file extensions. This helps maintain a clean and structured directory, making files easier to locate.

## Features

* **Automatic Categorization:** Sorts files into predefined categories like Documents, Images, Videos, Audio, Archives, Code, etc.
* **Customizable Mappings:** Easily modify or extend the `EXTENSION_MAP` dictionary in the script to change categories or add support for more file types.
* **Folder Creation:** Automatically creates necessary category folders if they do not already exist in the target directory.
* **"Other" Category:** Files with unrecognized extensions are moved to a dedicated "Other" folder.
* **Intelligent Skipping:** Skips directories, hidden files (starting with '.'), temporary files (starting with '~'), and the script's own log file to prevent unwanted operations.
* **Detailed Logging:** Records all actions (folder creation, file movements, errors, skips) with timestamps in a `file_organizer_log.txt` file located in the target directory. Includes a summary report at the end of each run.
* **Progress Indication:** Utilizes `tqdm` to display a progress bar during the organization process.
* **Configurable Target Directory:** By default, organizes the directory where the script is located, but this can be easily changed within the script.

## Installation

1.  **Prerequisites:** Ensure you have Python 3 installed on your system.
2.  **Clone or Download:** Clone this repository or download the Python script (`organizer.py`) to your local machine.
3.  **Install Dependencies:** This script requires the `tqdm` library for the progress bar. Install it using pip:
    ```bash
    pip install tqdm
    ```

## Usage

1.  **Navigate:** Open your terminal or command prompt and navigate to the directory where you saved the script (`organizer.py`).
2.  **Run the Script:** Execute the script using Python:
    ```bash
    python organizer.py
    ```

* By default, the script will organize the files within the **same directory** where the script itself resides.
* Monitor the progress bar in the terminal.
* Check the `file_organizer_log.txt` file created in the same directory for detailed information about the operations performed.

## Configuration

You can customize the script's behavior by modifying the configuration variables at the beginning of the `organizer.py` file:

* `DIRECTORY`: Change this variable to specify a different target directory path if you don't want to organize the script's current directory.
    ```python
    # Example: Organize files on the Desktop
    # DIRECTORY = "/path/to/your/Desktop" # Linux/macOS
    # DIRECTORY = "C:\\Users\\YourUser\\Desktop" # Windows
    DIRECTORY = os.path.dirname(os.path.abspath(__file__)) # Default
    ```
* `LOG_FILE`: Modify the path/name for the log file if needed.
    ```python
    LOG_FILE = os.path.join(DIRECTORY, "file_organizer_log.txt")
    ```
* `EXTENSION_MAP`: This dictionary defines the core logic.
    * **Add new extensions:** Append the extension (lowercase, without the dot) to the list associated with an existing category.
    * **Add new categories:** Add a new key-value pair, where the key is the category name (which will be the folder name) and the value is a list of associated extensions.
    ```python
    # Example: Adding a new category for CAD files
    EXTENSION_MAP: Dict[str, List[str]] = {
        # ... other categories ...
        "CAD Files": ["dwg", "dxf", "stl"],
        # ... rest of the categories ...
    }
    ```
    *Remember that the reverse mapping `FILE_EXTENSIONS` is generated automatically from `EXTENSION_MAP`.*

## Logging

A log file named `file_organizer_log.txt` is created (or appended to) in the directory being organized (`DIRECTORY`). This file contains:

* Timestamped entries for script start and end.
* Confirmation of category folder creation.
* Records of each file moved and its destination category.
* Notes on skipped files or files without extensions.
* Details of any errors encountered during file operations.
* A summary section detailing the number of files moved, skipped, errors encountered, and the total duration of the process.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or find any bugs, please feel free to open an issue or submit a pull request.