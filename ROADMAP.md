# Roadmap

## Stage 0 — Camp (done in this commit)
- Public GitHub repo
- Vision, architecture notes, emulator research
- Tiny userspace control-plane prototype

## Stage 1 — Rooted Android + Linux userland
- Scripted AVD create + `adb root` path
- AERoot notes for Play images
- Push control-plane into emulator and run under root shell
- Optional: PRoot Ubuntu/Alpine beside Android

## Stage 2 — AI control plane as the "OS personality"
- Intent shell (NL + commands)
- Capability tokens for agents
- Local model hook (optional; works rule-based without a GPU)
- Logging / event bus so the OS can *explain itself*

## Stage 3 — Take over Linux userspace
- Replace ad-hoc init scripts with Aether supervisor
- Service graph instead of random daemons
- Resource budgets and restart policy per agent
- `/dev/aether` character device *or* Unix socket that every process can talk to

## Stage 4 — Kernel experiments
- Linux kernel module that exports Aether events (sched, I/O)
- eBPF probes feeding the control plane
- Isolated Rust microkernel / unikernel spikes in QEMU (not Android)

## Stage 5 — Bootable Aether
- QEMU image that boots our supervisor first
- Linux remains as a compatibility personality if needed
- Hardware bring-up only after QEMU is boringly reliable

## Non-goals for a long time
- Shipping a phone ROM that replaces vendor Android
- Training a giant foundation model inside the kernel
- Security theater that still runs everything as root
