import json
from pathlib import Path
import os

def read(filename: str|Path) -> dict|list|None:
    """Read file with open 'r' and returns json.load()"""
    try:
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"File '{filename}' does not exist.")
    except Exception as e:
        raise Exception(f"Failed to read file {filename}") from e
    
def write(data: dict|list, filename: str|Path, indent=4) -> bool|None:
    """Write dict/list data with 'f' to json file
    
    Args:
        data: JSON data to write
        filename: File to write to
        indent: Indentation to use in the file
    
    Returns:
        bool (True): If operation completes successfully
        None: If operation fails and raises Exception
    """
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception as e:
        raise Exception(f"Failed to write to file {filename}") from e

def extract_dict_obj(text: str) -> dict | None:
    """Finds and returns a dict from a string
    Args:
        text (str): The text you wish to extract object from

    Returns:
        dict: If object was extracted
        None: If no object found
    """
    text = text.strip()
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except Exception:
        pass
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        obj = json.loads(text[start:end + 1])
        return obj if isinstance(obj, dict) else None
    except Exception:
        return None