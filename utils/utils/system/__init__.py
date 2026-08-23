from ..system import shell
from ..system import security

import pyperclip as _ppc

def copy_to_clipboard(text) -> None:
    """Copies given content to clipboard"""
    _ppc.copy(text)

def get_clipboard_content() -> str:
    """Gets clipboard content and returns"""
    return _ppc.paste()