import subprocess
from pathlib import Path

class TouchIDError(Exception):
    pass

def ensureTouchID() -> bool:
    """Checks if macos touchid executable exists"""
    exePath = Path('/usr/local/bin/touchid')
    return exePath.exists()


def askForTouchID(reason: str = "confirm a action") -> bool:
    result = subprocess.run(
        ["touchid", reason],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode == 0:
        return True

    if result.returncode == 2:
        raise TouchIDError(
            result.stderr.strip() or "Touch ID is unavailable"
        )