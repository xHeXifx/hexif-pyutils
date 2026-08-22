# hexif-pyutils

Super simple Python utilities.

This was mainly put on PyPi so i can install it without cloning it off gitea and then pip installing it off the local path.

## Install

```bash
pip install hexif-pyutils
```

## Install (TouchID Helper MacOS)

(If not cloned clone)
```zsh
git clone https://github.com/xHeXifx/hexif-pyutils
```

```zsh
cd {repo}/macOS/touchid-executable/touchid-helper
swift build -c release
```

Find the executable, will be somewhere in ./build and named 'touchid'
```zsh
cp {executable location} /usr/local/bin/touchid
sudo chmod +x /usr/local/bin/touchid
```

Optional test
```zsh
/usr/local/bin/touchid "perform a test"
```

## Usage

### Logger

```python
from utils.logger import Logger

log = Logger("app", log_file="app.log")
log.info("Hello")
```

What it does: simple logging wrapper with console and file output.

### File helpers

```python
from utils.file import read, write, get, touch

write("hello", "test.txt")
print(read("test.txt"))
print(get("test.txt").name)
touch("new.txt")
```

What it does: basic file reading/writing, file metadata lookup, and creating empty files.

### JSON

```python
from utils.file.json import read, write

write({"name": "hexif"}, "data.json")
data = read("data.json")
print(data)
```

What it does: reads and writes JSON files quickly.

### Shell

```python
from utils.system.shell import run

result = run("echo hello", capture_output=True, text=True)
print(result.stdout)
```

What it does: runs shell commands using Python subprocess.

### Touch ID

```python
from utils.system.security import askForTouchID

allowed = askForTouchID("confirm action")
print(allowed)
```

What it does: checks for the macOS Touch ID helper and asks for confirmation.

## Credits

- https://hexif.vercel.app
- https://github.com/xHeXifx