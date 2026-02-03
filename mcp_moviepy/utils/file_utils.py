import os
import tempfile
import uuid

def get_temp_file_path(prefix: str, extension: str) -> str:
    """
    Generates a secure temporary file path.
    """
    if extension.startswith("."):
        extension = extension[1:]
        
    filename = f"{prefix}_{uuid.uuid4().hex}.{extension}"
    temp_dir = tempfile.gettempdir()
    return os.path.join(temp_dir, filename)

def cleanup_temp_file(path: str) -> None:
    """
    Removes the file at the given path if it exists.
    """
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass # Ignore errors during cleanup
