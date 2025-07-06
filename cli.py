import platform
import os
from utils import load_config, save_config
from file_ops import (
    get_video_titles, backup_files, detect_duplicates, validate_regex,
    preview_changes, replace_text_in_filenames, organize_by_timestamp, undo_last_action
)

def print_welcome_note():
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
    print(welcome_message)

def navigate_directory():
    current_path = os.getcwd()
    print(f"\n **Current Directory**: {current_path}\n")
    while True:
        print("\n **Navigation Options:**\n1. List directories\n2. Move up one directory\n3. Enter a specific directory\n4. Use current directory\n5. Enter full path manually\n")
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            dirs = [d for d in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, d))]
            if dirs:
                print("\n **Directories:**\n" + "\n".join(f"{i}. {d}" for i, d in enumerate(dirs, 1)))
            else:
                print("\nNo directories found.")
        elif choice == "2":
            parent_path = os.path.dirname(current_path)
            if parent_path != current_path:
                current_path = parent_path
                print(f"\n **New Directory**: {current_path}")
            else:
                print("\nAlready at root directory.")
        elif choice == "3":
            dir_name = input("Enter directory name: ").strip()
            new_path = os.path.join(current_path, dir_name)
            if os.path.isdir(new_path):
                current_path = new_path
                print(f"\n **New Directory**: {current_path}")
            else:
                print("\nInvalid directory name.")
        elif choice == "4":
            save_config(current_path)
            return current_path
        elif choice == "5":
            manual_path = input("Enter full directory path: ").strip()
            if os.path.isdir(manual_path):
                save_config(manual_path)
                return manual_path
            else:
                print("\nInvalid directory path.")
        else:
            print("\nInvalid choice! Please select 1-5.")

def cli_main():
    print_welcome_note()
    print("\n **Choose Directory Method:**")
    print("1. Navigate directories")
    print("2. Enter path manually")
    choice = input("Choose an option (1-2): ").strip()
    if choice == "1":
        folder_path = navigate_directory()
    elif choice == "2":
        folder_path = input(f"Enter the folder path (last used: {load_config()}): ").strip() or load_config()
    else:
        print("Invalid choice! Exiting...")
        return
    if not folder_path or not os.path.isdir(folder_path):
        print("Invalid folder path!")
        return
    save_config(folder_path)
    while True:
        print("\n **Menu Options:**")
        print("1. Scrape file titles")
        print("2. Replace text in filenames")
        print("3. Remove text from filenames")
        print("4. Organize files by creation date")
        print("5. Undo last action")
        print("6. Exit")
        choice = input("Choose an option (1-6): ").strip()
        if choice in ["1", "2", "3", "4", "5"]:
            if choice in ["1", "2", "3", "4"]:
                backup = input("\nCreate a backup before proceeding? (y/n): ").strip().lower()
                if backup == 'y':
                    backup_files(folder_path)
            if choice in ["2", "3"]:
                if not detect_duplicates(folder_path):
                    proceed = input("\nDuplicates found. Proceed anyway? (y/n): ").strip().lower()
                    if proceed != 'y':
                        continue
        if choice == "1":
            get_video_titles(folder_path)
        elif choice == "2":
            patterns = input("Enter regex patterns (comma-separated, e.g., 'part[0-9]+,lesson'): ").strip().split(',')
            patterns = [p.strip() for p in patterns]
            if not patterns:
                print("Please enter at least one regex pattern.")
                continue
            if not validate_regex(patterns):
                continue
            replacement = input("Enter replacement text: ").strip()
            changes = preview_changes(folder_path, patterns, replacement)
            if changes:
                proceed = input("\nApply these changes? (y/n): ").strip().lower()
                if proceed == 'y':
                    replace_text_in_filenames(folder_path, patterns, replacement, changes)
                    print(" Text replacement completed.")
        elif choice == "3":
            patterns = input("Enter regex patterns to remove (comma-separated, e.g., 'part[0-9]+,lesson'): ").strip().split(',')
            patterns = [p.strip() for p in patterns]
            if not patterns:
                print("Please enter at least one regex pattern.")
                continue
            if not validate_regex(patterns):
                continue
            changes = preview_changes(folder_path, patterns, '', remove_mode=True)
            if changes:
                proceed = input("\nApply these changes? (y/n): ").strip().lower()
                if proceed == 'y':
                    replace_text_in_filenames(folder_path, patterns, '', changes)
                    print(" Text removal completed.")
        elif choice == "4":
            organize_by_timestamp(folder_path)
            print(" Files organized by creation date.")
        elif choice == "5":
            undo_last_action(folder_path)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please select 1-6.")
