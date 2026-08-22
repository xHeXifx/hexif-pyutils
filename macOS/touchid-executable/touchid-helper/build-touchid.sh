#!/usr/bin/env bash
#
# build-touchid.sh
#
# Script built by Claude. Dont murder me i do not know bash well enough to make a reliable script

set -euo pipefail

BINARY_NAME="touchid"
INSTALL_PATH="/usr/local/bin/${BINARY_NAME}"

if [[ -t 1 ]]; then
    RED=$'\033[0;31m'
    GREEN=$'\033[0;32m'
    YELLOW=$'\033[0;33m'
    NC=$'\033[0m'
else
    RED=""; GREEN=""; YELLOW=""; NC=""
fi

info()  { printf '%s\n' "${GREEN}==>${NC} $*"; }
warn()  { printf '%s\n' "${YELLOW}==>${NC} $*"; }
error() { printf '%s\n' "${RED}Error:${NC} $*" >&2; }

if ! command -v swift >/dev/null 2>&1; then
    error "'swift' was not found in PATH. Install the Swift toolchain / Xcode command line tools first."
    exit 1
fi
info "Found swift: $(swift --version 2>&1 | head -n1)"

if [[ ! -f "Package.swift" ]]; then
    error "No Package.swift found in the current directory ($(pwd))."
    error "Run this script from the touchid-helper package root, e.g.:"
    error "  cd ~/GitHub/hexif-pyutils/macOS/touchid-executable/touchid-helper"
    exit 1
fi

if ! grep -q "${BINARY_NAME}" Package.swift; then
    warn "Package.swift doesn't seem to mention '${BINARY_NAME}' — double-check you're in the right package."
fi

info "Working directory looks correct: $(pwd)"

info "Building ${BINARY_NAME} (release)..."
swift build -c release

info "Locating built executable under .build/ ..."

CANDIDATES=()
while IFS= read -r -d '' f; do
    CANDIDATES+=("$f")
done < <(find -L .build -type f -name "${BINARY_NAME}" -print0 2>/dev/null)

if [[ ${#CANDIDATES[@]} -eq 0 ]]; then
    error "Could not find a built '${BINARY_NAME}' executable anywhere under .build/."
    error "Try running 'swift build -c release' manually to check for errors."
    exit 1
fi

EXEC_CANDIDATES=()
for f in "${CANDIDATES[@]}"; do
    [[ -x "$f" ]] && EXEC_CANDIDATES+=("$f")
done
if [[ ${#EXEC_CANDIDATES[@]} -gt 0 ]]; then
    CANDIDATES=("${EXEC_CANDIDATES[@]}")
fi

RELEASE_CANDIDATES=()
for f in "${CANDIDATES[@]}"; do
    case "$f" in
        */release/*) RELEASE_CANDIDATES+=("$f") ;;
    esac
done
if [[ ${#RELEASE_CANDIDATES[@]} -gt 0 ]]; then
    CANDIDATES=("${RELEASE_CANDIDATES[@]}")
fi

BUILT_BINARY=$(ls -t "${CANDIDATES[@]}" | head -n1)

if [[ ${#CANDIDATES[@]} -gt 1 ]]; then
    warn "Found multiple candidates, using the most recently built one:"
    for c in "${CANDIDATES[@]}"; do
        printf '    %s\n' "$c"
    done
fi

info "Using executable: ${BUILT_BINARY}"

info "Installing to ${INSTALL_PATH} ..."

if [[ -d "/usr/local/bin" && -w "/usr/local/bin" ]]; then
    cp "${BUILT_BINARY}" "${INSTALL_PATH}"
else
    warn "Elevated permissions required to write to /usr/local/bin"
    sudo mkdir -p /usr/local/bin
    sudo cp "${BUILT_BINARY}" "${INSTALL_PATH}"
    sudo chmod 755 "${INSTALL_PATH}"
fi

chmod 755 "${INSTALL_PATH}" 2>/dev/null || sudo chmod 755 "${INSTALL_PATH}"

info "Installed successfully: ${INSTALL_PATH}"
info "Running test on touchid, should show a popup"
"${INSTALL_PATH}" perform a test >/dev/null 2>&1 || true
info "Done."