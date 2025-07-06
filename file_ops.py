
import os
import re
import shutil
import datetime
import logging
import json

# Supported extensions for all file operations
SUPPORTED_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".pdf"}

def get_video_titles(folder_path, text_widget=None, progress_callback=None):
    """Extract and print unique video titles from the specified folder."""
    try:
        folder_name = os.path.basename(folder_path)
        video_titles = set()
        files = os.listdir(folder_path)
        for i, filename in enumerate(files):
            name, ext = os.path.splitext(filename)
            if ext.lower() in SUPPORTED_EXTENSIONS:
                video_titles.add(name)
            if progress_callback:
                progress = (i + 1) / len(files) * 100
                progress_callback(progress)
        output = f"\n **Folder Name:** {folder_name}\n\n📜 **Unique File Titles:**\n"
        for title in sorted(video_titles):
            output += f"- {title}\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.info(f"Scraped titles from: {os.path.basename(folder_path)}")
    except Exception as e:
        output = f"Error scraping titles: {str(e)}\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.error(f"Error in get_video_titles: {str(e)}")


def backup_files(folder_path, text_widget=None, progress_callback=None):
    """Create a backup of all files in the folder. Note: Subdirectories are not backed up."""
    try:
        backup_dir = os.path.join(folder_path, f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(backup_dir, exist_ok=True)
        files = os.listdir(folder_path)
        for i, filename in enumerate(files):
            src = os.path.join(folder_path, filename)
            dst = os.path.join(backup_dir, filename)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            if progress_callback:
                progress = (i + 1) / len(files) * 100
                progress_callback(progress)
        output = f"\n Backup created at: {os.path.basename(backup_dir)}\n(Warning: Subdirectories are not included in the backup.)\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.info(f"Backup created at: {os.path.basename(backup_dir)}")
        return backup_dir
    except Exception as e:
        output = f"Error creating backup: {str(e)}\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.error(f"Error in backup_files: {str(e)}")
        return None


def detect_duplicates(folder_path, text_widget=None, progress_callback=None):
    """Detect and report duplicate filenames (ignoring extensions)."""
    try:
        name_count = {}
        duplicates = []
        files = os.listdir(folder_path)
        for i, filename in enumerate(files):
            name, ext = os.path.splitext(filename)
            if ext.lower() in SUPPORTED_EXTENSIONS:
                name_count[name] = name_count.get(name, 0) + 1
                if name_count[name] > 1:
                    duplicates.append(name)
            if progress_callback:
                progress = (i + 1) / len(files) * 100
                progress_callback(progress)
        if duplicates:
            output = "\n **Duplicate Filenames Detected:**\n" + "\n".join(f"- {dup}" for dup in set(duplicates)) + "\n"
            if text_widget:
                text_widget.insert('end', output)
            else:
                print(output)
            logging.warning(f"Duplicates found: {', '.join(set(duplicates))}")
            return False
        output = "\n No duplicate filenames detected.\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.info("No duplicates found")
        return True
    except Exception as e:
        output = f"Error detecting duplicates: {str(e)}\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.error(f"Error in detect_duplicates: {str(e)}")
        return False


def validate_regex(patterns, text_widget=None):
    """Validate regex patterns to ensure they are correct."""
    invalid_patterns = []
    for pattern in patterns:
        try:
            re.compile(pattern)
        except re.error:
            invalid_patterns.append(pattern)
    if invalid_patterns:
        output = f"Invalid regex patterns: {', '.join(invalid_patterns)}\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.error(f"Invalid regex patterns: {invalid_patterns}")
        return False
    return True


def preview_changes(folder_path, patterns, replacement, remove_mode=False, text_widget=None, progress_callback=None):
    """Preview filename changes before applying them. Prevents overwriting files."""
    try:
        if not validate_regex(patterns, text_widget):
            return []
        changes = []
        files = os.listdir(folder_path)
        existing_files = set(files)
        for i, filename in enumerate(files):
            name, ext = os.path.splitext(filename)
            if ext.lower() in SUPPORTED_EXTENSIONS:
                new_name = name
                for pattern in patterns:
                    if remove_mode:
                        new_name = re.sub(pattern, '', new_name, flags=re.IGNORECASE)
                    else:
                        new_name = re.sub(pattern, replacement, new_name, flags=re.IGNORECASE)
                if new_name != name and new_name.strip():
                    candidate = new_name + ext
                    if candidate in existing_files and candidate != filename:
                        output = f"[SKIP] {filename} -> {candidate} (Target exists, skipping to prevent overwrite)\n"
                        if text_widget:
                            text_widget.insert('end', output)
                        else:
                            print(output)
                        logging.warning(f"Skipping rename {filename} -> {candidate} (target exists)")
                        continue
                    changes.append((filename, candidate))
            if progress_callback:
                progress = (i + 1) / len(files) * 100
                progress_callback(progress)
        if changes:
            output = "\n **Preview of Changes:**\n" + "\n".join(f"{os.path.basename(old)} -> {os.path.basename(new)}" for old, new in changes) + "\n"
        else:
            output = "\nNo changes to preview.\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.info(f"Previewed changes: {len(changes)} files")
        return changes
    except Exception as e:
        output = f"Error previewing changes: {str(e)}\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.error(f"Error in preview_changes: {str(e)}")
        return []


def replace_text_in_filenames(folder_path, patterns, replacement, changes, text_widget=None, progress_callback=None):
    """Apply filename changes and log for undo. Prevents overwriting files."""
    UNDO_FILE = "undo.json"
    try:
        undo_log = []
        for i, (old_name, new_name) in enumerate(changes):
            src = os.path.join(folder_path, old_name)
            dst = os.path.join(folder_path, new_name)
            if os.path.exists(dst):
                output = f"[SKIP] {old_name} -> {new_name} (Target exists, skipping to prevent overwrite)\n"
                if text_widget:
                    text_widget.insert('end', output)
                else:
                    print(output)
                logging.warning(f"Skipping rename {old_name} -> {new_name} (target exists)")
                continue
            os.rename(src, dst)
            undo_log.append((dst, src))
            output = f"Renamed: {os.path.basename(old_name)} -> {os.path.basename(new_name)}\n"
            if text_widget:
                text_widget.insert('end', output)
            else:
                print(output)
            logging.info(f"Renamed: {os.path.basename(old_name)} -> {os.path.basename(new_name)}")
            if progress_callback:
                progress = (i + 1) / len(changes) * 100
                progress_callback(progress)
        with open(UNDO_FILE, "w") as f:
            json.dump(undo_log, f)
        logging.info("Saved undo log")
    except Exception as e:
        output = f"Error renaming files: {str(e)}\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.error(f"Error in replace_text_in_filenames: {str(e)}")


def undo_last_action(folder_path, text_widget=None):
    """Undo the last rename or move operation."""
    UNDO_FILE = "undo.json"
    try:
        if not os.path.exists(UNDO_FILE):
            output = "No actions to undo.\n"
            if text_widget:
                text_widget.insert('end', output)
            else:
                print(output)
            logging.info("No undo log found")
            return
        with open(UNDO_FILE, "r") as f:
            undo_log = json.load(f)
        for dst, src in undo_log:
            if os.path.exists(dst):
                os.rename(dst, src)
                output = f"Undid: {os.path.basename(dst)} -> {os.path.basename(src)}\n"
                if text_widget:
                    text_widget.insert('end', output)
                else:
                    print(output)
                logging.info(f"Undid: {dst} -> {src}")
        os.remove(UNDO_FILE)
        logging.info("Cleared undo log")
    except Exception as e:
        output = f"Error undoing action: {str(e)}\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.error(f"Error in undo_last_action: {str(e)}")


def organize_by_timestamp(folder_path, text_widget=None):
    """Organize files into folders based on creation timestamp. Prevents overwriting files."""
    try:
        UNDO_FILE = "undo.json"
        undo_log = []
        files = os.listdir(folder_path)
        for i, filename in enumerate(files):
            src = os.path.join(folder_path, filename)
            if os.path.isfile(src):
                name, ext = os.path.splitext(filename)
                if ext.lower() in SUPPORTED_EXTENSIONS:
                    ctime = os.path.getctime(src)
                    date_folder = datetime.datetime.fromtimestamp(ctime).strftime('%Y-%m-%d')
                    dest_folder = os.path.join(folder_path, date_folder)
                    os.makedirs(dest_folder, exist_ok=True)
                    dst = os.path.join(dest_folder, filename)
                    if os.path.exists(dst):
                        output = f"[SKIP] {filename} -> {dest_folder} (Target exists, skipping to prevent overwrite)\n"
                        if text_widget:
                            text_widget.insert('end', output)
                        else:
                            print(output)
                        logging.warning(f"Skipping move {filename} -> {dst} (target exists)")
                        continue
                    shutil.move(src, dst)
                    undo_log.append((dst, src))
                    output = f"Moved: {filename} -> {dest_folder}\n"
                    if text_widget:
                        text_widget.insert('end', output)
                    else:
                        print(output)
                    logging.info(f"Moved: {filename} -> {dest_folder}")
            if text_widget:
                progress = (i + 1) / len(files) * 100
                text_widget.master.children['!progressbar']['value'] = progress
                text_widget.master.update()
        with open(UNDO_FILE, "w") as f:
            json.dump(undo_log, f)
        logging.info("Saved undo log")
        output = " Files organized by creation date.\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.info("Files organized by creation date")
    except Exception as e:
        output = f"Error organizing files: {str(e)}\n"
        if text_widget:
            text_widget.insert('end', output)
        else:
            print(output)
        logging.error(f"Error in organize_by_timestamp: {str(e)}")
