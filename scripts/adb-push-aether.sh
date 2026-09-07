#!/usr/bin/env bash
# Push the userspace control plane into a running emulator.
# Requires adb on PATH and a device that already accepts a root shell.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
adb wait-for-device
adb root || true
adb shell mkdir -p /data/local/tmp/aether
adb push "$ROOT/control-plane" /data/local/tmp/aether/
echo "Pushed. On many AVDs there is no python3. Run the shell on the host for now:"
echo "  cd control-plane && python3 -m aether.shell"
