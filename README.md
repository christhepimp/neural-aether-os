# Neural Aether OS

**An AI-native operating system research project.**

The long-term idea is simple and extreme: the OS itself should think. Not a chatbot sitting on top of Linux. Not an assistant app. The scheduler, the policy engine, the shell, and eventually the kernel services should reason about what the machine is doing and why.

This repository is the starting camp for that work — not a finished kernel that replaces Linux tomorrow.

Repo: https://github.com/christhepimp/neural-aether-os

---

## What this is (and is not)

**This is**
- A public research + engineering repo for an AI-shaped OS
- A documented path that starts where you asked: rooted Android emulators and Linux userland
- A staged architecture that can grow from userspace agents → AI control plane → custom kernel services

**This is not**
- A drop-in replacement for Linux you can flash tonight
- A claim that we already wrote a new kernel from scratch
- A jailbreak / exploit toolkit

Replacing Linux is a multi-year systems project. Pretending otherwise would be lying. The honest path is: **use Linux as the host while we build the AI control plane, then push intelligence downward into the kernel.**

---

## The original goal, translated into an actual plan

You asked to:
1. Find an Android emulator that can be rooted
2. Get a Linux environment inside it
3. Start replacing Linux with a new OS we make ourselves
4. Make that OS *be* an AI

Here is the workable mapping:

| Stage | What we actually do | Why |
|---|---|---|
| 0 | Document rooted Android emulator options | You asked for this first |
| 1 | Get a real Linux userspace (chroot / PRoot / VM / emulator shell) | You need a POSIX world to build in |
| 2 | Run an **AI control plane** as PID 1-adjacent userspace | The OS *feels* like an AI before we rewrite the kernel |
| 3 | Replace init, scheduler policy, and package/service management | Incremental takeover of Linux |
| 4 | Custom kernel modules / unikernel / Rust microkernel experiments | Real replacement work |
| 5 | Bare-metal / QEMU image that boots *Aether* | The actual new OS |

Stage 5 is the destination. Stages 0–3 are how you get there without vaporware.

---

## Rooted Android emulator research (2026)

Practical options, ranked for *this* project:

### 1. Android Studio AVD (Google APIs, not Play Store image) — best default
- Official emulator from Google.
- Images **without** the Play Store often allow `adb root` immediately.
- Play Store images are locked down; use [AERoot](https://github.com/quarkslab/AERoot) to elevate processes on those AVDs.
- Workflow:
  ```bash
  emulator @YourAVD -qemu -s   # if using AERoot + gdb
  adb root
  adb remount
  adb shell
  ```

### 2. AERoot (Quarkslab) — best for Play-flavored AVDs
- Gives root on-the-fly to a PID, process name, or `adbd`.
- Needs gdb with Python support.
- Repo: https://github.com/quarkslab/AERoot

### 3. Genymotion
- Fast x86/x86_64 VMs.
- Historically easy root shells via `adb shell` then `su`.
- Good when you want Android + VirtualBox/QEMU comfort.

### 4. Waydroid (on a Linux host)
- Not an emulator in the classic sense: Android in an LXC container sharing the host kernel.
- Excellent if the *host* is already Linux and you want Android apps + real kernel access.

### 5. Bliss OS / Android-x86 in QEMU or VirtualBox
- Full Android-as-OS, easier to treat like a machine you own.
- Better when the goal is "own the box" rather than "mimic a phone."

### Linux *inside* Android (when you have a device or emulator)
- **PRoot / Complete Linux Installer / Termux + proot-distro** — no real root required, fake root via ptrace.
- **Podroid** — real Alpine VM via QEMU/AVF, containers work like a server.
- These are useful sandboxes. They are **not** replacing the kernel.

See [docs/emulator.md](docs/emulator.md) for commands.

---

## Architecture (target)

```
+-------------------------------------------------------+
|  Aether Shell  (natural language + POSIX)             |
+-------------------------------------------------------+
|  Aether Control Plane                                 |
|   - intent parser                                     |
|   - policy / capability engine                        |
|   - service graph (agents as first-class units)       |
|   - local model runtime (llama.cpp / candle / onnx)   |
+-------------------------------------------------------+
|  Compatibility layer                                  |
|   - Linux syscalls today                              |
|   - Aether ABI tomorrow                               |
+-------------------------------------------------------+
|  Kernel                                               |
|   Phase A: Linux                                      |
|   Phase B: Linux + Aether modules                     |
|   Phase C: custom kernel (Rust microkernel experiments)|
+-------------------------------------------------------+
|  Hardware / QEMU / Android emulator                   |
+-------------------------------------------------------+
```

Design principles:
- **Agents are kernel-shaped objects**, not apps. They have capabilities, restart policy, resource budgets.
- **AI is a device**, not a website. Think `/dev/aether` and a local model, not an API key.
- **Capabilities over ambient root.** Even if we *start* from a rooted emulator, the OS we build should not be "everything is root."
- **Linux is scaffolding.** We stand on it until we can cut it away.

Related prior art worth reading (not forks we claim):
- Maya — AI-native kernel research (Rust, PPO scheduler claims)
- Oxide OS — microkernel built for agents
- EdgeAI-OS — `/dev/ai` on Linux
- openKylin — "AI for OS" rather than "AI on OS"

---

## Repository layout

```
neural-aether-os/
  README.md                 this file
  ROADMAP.md                staged milestones
  docs/
    emulator.md             rooted emulator + Linux-inside-Android notes
    architecture.md         control plane and kernel phases
  control-plane/            userspace AI OS prototype (Python first, Rust later)
  agents/                   example agents (scheduler-advisor, sentinel, shell)
  scripts/                  emulator + adb helpers
  kernel-experiments/       placeholders for modules / unikernel notes
```

---

## Quick start (control plane prototype)

You do **not** need an emulator to try the first slice. The control plane is a userspace process that pretends to be the OS brain.

```bash
cd control-plane
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m aether.shell
```

Then type intents like:
- `status`
- `what is running`
- `spawn sentinel`
- `explain policy`

Hooking this into a rooted emulator is Stage 1: `adb push` the tree, run it under `adb shell`.

---

## License

MIT. See [LICENSE](LICENSE).
