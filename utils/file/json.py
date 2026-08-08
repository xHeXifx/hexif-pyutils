import json
from pathlib import Path
import os

def read(filename: str|Path) -> dict|list|None:
    try:
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError(f"File '{filename}' does not exist.")
    except Exception as e:
        raise Exception(f"Failed to read file {filename}") from e
    
def write(data: dict|list, filename: str|Path, indent=4) -> bool|None:
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception as e:
        raise Exception(f"Failed to write to file {filename}") from e