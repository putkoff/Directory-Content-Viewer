# Directory-Content-Viewer
A simple Python application that utilizes the Tkinter library to create a graphical user interface for browsing and managing files and directories. This application includes features such as analyzing JavaScript files for imports and exports, sending files for revision using the GPT-4 AI model, making test copies of files, and copying file paths.

**README.md**

```
# Directory Content Viewer


## Features

- Browse directories
- Right-click context menu with options:
    - Analyze JavaScript files (`.js` and `.jsx`) for imports and exports
    - Send files for revision using the GPT-4 AI model (requires `send_chunks.py` and the GPT-4 model)
    - Make test copies of files
    - Copy file paths
- Display associated files based on imports and exports in a Listbox
- Open directories in new windows

## Installation

1. Clone the repository or download the source code.

2. Install the required packages using `pip`:

   ```
   pip install -r requirements.txt
   ```

3. Run the `directory_content_viewer.py` script:

   ```
   python directory_content_viewer.py
   ```

## Usage

1. Click the "Browse" button to open a directory.

2. Right-click on a file or folder to access the context menu with the available options.

3. Use the associated file Listbox to view and manage associated files based on imports and exports.
```

**requirements.txt**

```
tkinter
```

You can create a new file named `README.md` in your project directory and paste the contents above. Similarly, create a new file named `requirements.txt` and paste the contents above.

These files should help others understand the purpose and functionality of your project, as well as how to install and use it.
