import tkinter as tk
import os
from tkinter import filedialog, scrolledtext, messagebox, ttk
from utils import load_config, save_config
from file_ops import (
    get_video_titles, backup_files, detect_duplicates, validate_regex,
    preview_changes, replace_text_in_filenames, organize_by_timestamp, undo_last_action
)

def print_welcome_note(text_widget=None):
    welcome_message = (
        "\n **Welcome to File Manager Script!** \n\n"
        "This script helps you manage video and PDF files in a directory.\n\n"
        " **How to Copy Directory Path:**\n"
        "- **Windows**: Right-click the folder in File Explorer, select 'Properties', copy the 'Location' path, "
        "or hold Shift + Right-click and select 'Copy as path'.\n"
        "- **Linux/macOS**: Right-click the folder in your file manager, select 'Properties' to copy the path, "
        "or use 'pwd' in terminal to get the current directory path.\n\n"
        "Alternatively, use the directory navigation feature to select a folder.\n"
    )
    if text_widget:
        text_widget.insert(tk.END, welcome_message)
    else:
        print(welcome_message)

def create_gui():
    window = tk.Tk()
    window.title("File Manager - Practical Edition")
    window.geometry("700x600")
    window.resizable(True, True)
    folder_path_var = tk.StringVar(value=load_config())
    patterns_var = tk.StringVar()
    replacement_var = tk.StringVar()
    folder_frame = tk.Frame(window)
    folder_frame.pack(pady=10, fill=tk.X)
    tk.Label(folder_frame, text="Folder Path:").pack(side=tk.LEFT)
    tk.Entry(folder_frame, textvariable=folder_path_var, width=60).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    tk.Button(folder_frame, text="Browse", command=lambda: folder_path_var.set(filedialog.askdirectory())).pack(side=tk.LEFT)
    input_frame = tk.Frame(window)
    input_frame.pack(pady=10, fill=tk.X)
    tk.Label(input_frame, text="Regex Patterns (comma-separated):").pack(anchor='w')
    tk.Entry(input_frame, textvariable=patterns_var, width=70).pack(pady=5, fill=tk.X)
    tk.Label(input_frame, text="Replacement Text (for option 2):").pack(anchor='w')
    tk.Entry(input_frame, textvariable=replacement_var, width=70).pack(pady=5, fill=tk.X)
    progress_bar = ttk.Progressbar(window, maximum=100)
    progress_bar.pack(pady=5, fill=tk.X)
    output_text = scrolledtext.ScrolledText(window, width=90, height=18, wrap=tk.WORD)
    output_text.pack(pady=10, fill=tk.BOTH, expand=True)
    def run_action(action, remove_mode=False):
        folder_path = folder_path_var.get()
        if not folder_path or not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder path.")
            return
        save_config(folder_path)
        output_text.delete(1.0, tk.END)
        progress_bar['value'] = 0
        window.update()
        def update_progress(val):
            progress_bar['value'] = val
            window.update_idletasks()
        if messagebox.askyesno("Backup", "Create a backup before proceeding?"):
            backup_files(folder_path, output_text, progress_callback=update_progress)
        if action == "scrape":
            get_video_titles(folder_path, output_text, progress_callback=update_progress)
        elif action in ["replace", "remove"]:
            patterns = [p.strip() for p in patterns_var.get().split(',') if p.strip()]
            if not patterns:
                messagebox.showerror("Error", "Please enter at least one regex pattern.")
                return
            if not validate_regex(patterns, output_text):
                return
            replacement = replacement_var.get() if action == "replace" else ""
            if not detect_duplicates(folder_path, output_text, progress_callback=update_progress):
                if not messagebox.askyesno("Warning", "Duplicates found. Proceed anyway?"):
                    return
            changes = preview_changes(folder_path, patterns, replacement, remove_mode, output_text, progress_callback=update_progress)
            if changes and messagebox.askyesno("Confirm", "Apply these changes?"):
                replace_text_in_filenames(folder_path, patterns, replacement, changes, output_text, progress_callback=update_progress)
                output_text.insert(tk.END, f" {'Text replacement' if action == 'replace' else 'Text removal'} completed.\n")
        elif action == "organize":
            organize_by_timestamp(folder_path, output_text)
        elif action == "undo":
            undo_last_action(folder_path, output_text)
        progress_bar['value'] = 0
    button_frame = tk.Frame(window)
    button_frame.pack(pady=10, fill=tk.X)
    tk.Button(button_frame, text="Scrape File Titles", command=lambda: run_action("scrape"), width=18).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Replace Text", command=lambda: run_action("replace"), width=18).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Remove Text", command=lambda: run_action("remove", True), width=18).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Organize by Date", command=lambda: run_action("organize"), width=18).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Undo Last Action", command=lambda: run_action("undo"), width=18).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Exit", command=window.quit, width=10).pack(side=tk.RIGHT, padx=5)
    print_welcome_note(output_text)
    window.mainloop()
