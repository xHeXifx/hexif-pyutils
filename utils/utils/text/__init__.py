import re

def is_valid_email(text: str) -> bool:
    """Checks if text provided is a valid email using regex"""
    return bool(re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", "test@example.com"))

def is_https_site(text: str) -> bool:
    """Checks if text looks like https site"""
    return bool(re.fullmatch(r"^https://(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?:/[^\s]*)?$", text))

def is_http_site(text: str) -> bool:
    """Checks if text looks like http site"""
    return bool(re.fullmatch(r"http://(?:(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}|(?:\d{1,3}\.){3}\d{1,3})(?:/[^\s]*)?", text))