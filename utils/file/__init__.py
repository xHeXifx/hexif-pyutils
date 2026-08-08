from . import json

from pathlib import Path as _Path
from os.path import isfile as _isfile
from os.path import exists as _exists
from typing import Any as _Any

class File:
    def __init__(self, filename: str|_Path):
        if not isinstance(filename, _Path):
            filename = _Path(filename)
        self.path = filename
        self.exists = self.path.exists()

        self.is_file = self.path.is_file()
        self.is_dir = self.path.is_dir()
        self.is_symlink = self.path.is_symlink()

        self.name = self.path.name
        self.stem = self.path.stem
        self.extension = self.path.suffix
        self.parent = self.path.parent
        self.absolute = self.path.absolute()
        self.resolved = self.path.resolve()

        self.size_bytes = self.path.stat().st_size
        self.size_kb = self.size_bytes / 1024
        self.size_mb = self.size_bytes / 1024**2
        self.size_gb = self.size_bytes / 1024**3
        

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

def get(file: str|_Path) -> File|None:
    if _exists(file):
        return File(file)
    else:
        raise FileNotFoundError()

def touch(file: str|_Path) -> None:
    if _exists(file):
        return None
    