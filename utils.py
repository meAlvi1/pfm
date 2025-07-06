import os
import json
import logging

CONFIG_FILE = "config.json"

def setup_logging():
    logging.basicConfig(filename='file_manager.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    """Load last folder path from config file."""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                return config.get("last_folder", "")
        return ""
    except Exception as e:
        logging.error(f"Error loading config: {str(e)}")
        return ""

def save_config(folder_path):
    """Save folder path to config file."""
    try:
        config = {"last_folder": folder_path}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        logging.info(f"Saved config with folder: {folder_path}")
    except Exception as e:
        logging.error(f"Error saving config: {str(e)}")
