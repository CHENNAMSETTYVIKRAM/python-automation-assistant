import os
import shutil
from utils.logger import log_error, log_info

def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True, f"Folder created at {path}"
    except Exception as e:
        log_error(f"Failed to create folder at {path}: {e}")
        return False, f"Error creating folder"

def move_files(source, destination):
    try:
        shutil.move(source, destination)
        return True, f"Moved {source} to {destination}"
    except Exception as e:
        log_error(f"Failed to move {source} to {destination}: {e}")
        return False, f"Error moving files"

def organize_downloads():
    # Simple organizer: move images to an 'Images' folder, etc.
    try:
        downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
        images_dir = os.path.join(downloads_path, 'Images')
        docs_dir = os.path.join(downloads_path, 'Documents')
        
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(docs_dir, exist_ok=True)
        
        count = 0
        for item in os.listdir(downloads_path):
            item_path = os.path.join(downloads_path, item)
            if os.path.isfile(item_path):
                if item.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                    shutil.move(item_path, os.path.join(images_dir, item))
                    count += 1
                elif item.lower().endswith(('.pdf', '.docx', '.txt', '.xlsx')):
                    shutil.move(item_path, os.path.join(docs_dir, item))
                    count += 1
        
        return True, f"Organized {count} files in Downloads."
    except Exception as e:
        log_error(f"Failed to organize downloads: {e}")
        return False, "Error organizing downloads"

def delete_temp_files():
    try:
        temp_dir = os.environ.get('TEMP')
        if not temp_dir:
            return False, "Temp directory not found"
        
        count = 0
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            try:
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    count += 1
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    count += 1
            except Exception:
                pass # skip files in use
                
        return True, f"Cleaned up {count} temporary items."
    except Exception as e:
        log_error(f"Failed to delete temp files: {e}")
        return False, "Error deleting temporary files"

def open_folder(folder_name):
    try:
        folder_name = folder_name.lower()
        base_dir = os.path.expanduser('~')
        paths = {
            "documents": os.path.join(base_dir, 'Documents'),
            "downloads": os.path.join(base_dir, 'Downloads'),
            "desktop": os.path.join(base_dir, 'Desktop'),
            "pictures": os.path.join(base_dir, 'Pictures'),
            "music": os.path.join(base_dir, 'Music'),
            "videos": os.path.join(base_dir, 'Videos'),
        }
        
        target = paths.get(folder_name)
        if target and os.path.exists(target):
            os.startfile(target)
            return True, f"Opened {folder_name} folder."
        elif os.path.exists(folder_name):
            os.startfile(folder_name)
            return True, f"Opened folder {folder_name}."
        else:
            return False, f"Could not find folder {folder_name}."
    except Exception as e:
        log_error(f"Failed to open folder: {e}")
        return False, "Error opening folder."
