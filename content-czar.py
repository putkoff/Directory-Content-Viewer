import os
import re
import shutil
from tkinter import filedialog, Menu, Listbox, Toplevel, Canvas
import tkinter as tk
from send_chunks import send_chunks_to_chatgpt
def display_directory_contents(root, directory, is_new_window=False):
    if is_new_window:
        new_window = Toplevel(root)
        root = new_window

    for widget in root.grid_slaves():
        if isinstance(widget, tk.Button) or isinstance(widget, Listbox):
            widget.destroy()

    for row, item in enumerate(os.listdir(directory)):
        item_path = os.path.join(directory, item)

        button = tk.Button(root, text=item)
        button.grid(row=row, column=0, padx=5, pady=5)
        button.bind('<Button-3>', lambda event, item=item_path: on_right_click(event, item))

        if os.path.isdir(item_path):
            folder_button = tk.Button(root, text="📁", command=lambda item=item_path: display_directory_contents(root, item, is_new_window=True))
            folder_button.grid(row=row, column=1, padx=5, pady=5)

def on_right_click(event, item):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Analyze", command=lambda: analyze_file(item))
    context_menu.add_command(label="Send for Revision", command=lambda: send_for_revision(item))
    context_menu.add_command(label="Make Test Copy", command=lambda: make_test_copy(item))
    context_menu.add_command(label="Copy Path", command=lambda: copy_path(item))

    context_menu.post(event.x_root, event.y_root)

def copy_path(item):
    root.clipboard_clear()
    root.clipboard_append(item)
    print(f"Copied path: {item}")
def on_right_click(event, item):
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Analyze", command=lambda: analyze_file(item))
    context_menu.add_command(label="Send for Revision", command=lambda: send_for_revision(item))
    context_menu.add_command(label="Make Test Copy", command=lambda: make_test_copy(item))

    context_menu.post(event.x_root, event.y_root)

def analyze_file(item):
    print(f"Analyze: {item}")
    if item.endswith(".js") or item.endswith(".jsx"):
        imports, exports = analyze_js_file(item)
        input([imports, exports])
        display_associated_files(imports, exports)

def display_associated_files(imports, exports):
    associated_files = imports + exports

    associated_files_listbox = Listbox(root)
    for file in associated_files:
        associated_files_listbox.insert(tk.END, file)
    associated_files_listbox.grid(row=1, column=0, padx=5, pady=5)

def send_for_revision(item):
    print(f"Send for Revision: {item}")
    # Implement the send for revision functionality
    send_chunks_to_chatgpt(item,'gpt-4')


def make_test_copy(item):
    print(f"Make Test Copy: {item}")
    destination_directory = filedialog.askdirectory()
    if destination_directory:
        destination_path = os.path.join(destination_directory, os.path.basename(item))
        shutil.copyfile(item, destination_path)
        print(f"Copied {item} to {destination_path}")
    
def browse_directory():
    directory = filedialog.askdirectory()
    display_directory_contents(root, directory)

root = tk.Tk()
root.title("Directory Content Viewer")

browse_button = tk.Button(root, text="Browse", command=browse_directory)
browse_button.grid(row=0, column=0, padx=5, pady=5)

root.mainloop()
