import subprocess
from pathlib import Path

class TouchIDError(Exception):
    pass

def ensureTouchID() -> bool:
    """Checks if macos touchid executable exists"""
    exePath = Path('/usr/local/bin/touchid')
    return exePath.exists()


def askForTouchID(reason: str = "confirm a action") -> bool:
    """MACOS ONLY
    Uses the touchid executable to confirm a action
    Install: https://github.com/xHeXifx/hexif-pyutils/tree/main#install-touchid-helper-macos

    Args:
        reason: Will appear in popup as "touchid wants to {reason}"
    
    Returns:
        True: If confirmed
        False: If cancelled
    
    Raises:
        TouchIDError: If touchid feature isn't avalible or not found
    """
    if not ensureTouchID():
        raise TouchIDError("touchid executable is not installed")
    result = subprocess.run(
        ["touchid", reason],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False

    if result.returncode == 2:
        raise TouchIDError(
            result.stderr.strip() or "Touch ID is unavailable"
        )