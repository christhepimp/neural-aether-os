# Architecture

## Why not rewrite Linux this week

A general-purpose kernel is drivers, memory, scheduling, filesystems, IPC, security, and 30 years of hardware pain. An AI model does not replace that. An AI *policy layer* can sit on top of it, then eat pieces of it.

## Control plane (now)

The control plane is a userspace process with:

- **Bus** — JSON events (`spawn`, `kill`, `anomaly`, `intent`)
- **Registry** — named agents with capabilities
- **Policy** — allow / deny / ask
- **Shell** — human language in, structured actions out
- **Explain** — every action can be narrated

Rule-based first. Swap the interpreter for a local LLM when you have a model file. The API stays the same.

## Agents as OS objects

Each agent record:

```json
{
  "name": "sentinel",
  "capabilities": ["proc.read", "net.observe"],
  "restart": "on-failure",
  "budget_cpu_ms": 50
}
```

No ambient authority. Root on the emulator is only the bootstrap hammer.

## Kernel phases

1. **Observe** — eBPF / procfs / logcat feeding the bus
2. **Advise** — control plane recommends nice values, kill candidates, network policy
3. **Act** — supervisor applies those decisions
4. **Replace** — custom scheduler class or microkernel experiment in QEMU

## AI-as-device

Target interface:

```
echo "summarize /var/log/aether" > /dev/aether
```

or a Unix socket at `/run/aether.sock` until a real device node exists.

## Implementation languages

- Prototype: Python 3 (this repo)
- Next: Rust for the supervisor and any kernel-adjacent code
- Models: out of process (llama.cpp server). Never block the kernel on a 7B forward pass.
