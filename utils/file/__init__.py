from . import json

from pathlib import Path as _Path
from os.path import isfile as _isfile
from typing import Any as _Any

def read(filename: str|_Path) -> str|None:
    try:
        if _isfile(filename):
            with open(filename, 'r') as f:
                return f.read()
        else:
            raise FileNotFoundError(f"File '{filename}' does not exist.")
    except Exception as e:
        raise Exception(f"Failed to read file {filename}") from e
    
def write(data: _Any, filename: str|_Path) -> bool|None:
    try:
        with open(filename, 'w') as f:
            f.write(data)
        return True
    except Exception as e:
        raise Exception(f"Failed to write to file {filename}") from e