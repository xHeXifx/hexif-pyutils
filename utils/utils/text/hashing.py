import hashlib as _hshl
from typing import Literal as _Literal
from pathlib import Path as _Path

def hash_text(text: str, algorithm: _Literal['sha256']) -> str:
    """Hash text using hashlib"""
    match algorithm:
        case "sha256":
            return _hshl.sha256(text.encode('utf-8')).hexdigest()

def hash_file(path: str|_Path, algorithm: _Literal['sha256']) -> str:
    """Get the hash of a file
    Args:
        path: File path to hash
        algorithm: Algorithm to hash with
    Returns:
        str: File hash
    """
    path = _Path(path)
    hasher = _hshl.new(algorithm)

    with path.open('rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)

    return hasher.hexdigest()

def compare_file_hash(file: str|_Path, expected: str, algorithm: _Literal['sha256']) -> bool:
    """Hash a file and compare its hash with expected
    Args:
        file: File path
        expected: Expected hash of file
        algorith: Algorithm expected is in and to hash file with
    
    Returns:
        bool: If hash is same or not
    """
    currentHash = hash_file(file, algorithm)
    return currentHash == expected