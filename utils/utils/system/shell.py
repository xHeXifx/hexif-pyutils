import subprocess as _sbp

def run(command: str, **kwargs) -> _sbp.CompletedProcess | None:
    """Run a command with subprocess.

    Args:
        command: Command to execute as a string.
        **kwargs: Additional arguments passed to subprocess.run().

    Returns:
        The command's stdout if capture_output=True, otherwise None.

    Raises:
        RuntimeError: If the command returns a non-zero exit code.
        subprocess.CalledProcessError: If check=True and the command fails.
    """
    return _sbp.run(
        command.split(),
        **kwargs
    )