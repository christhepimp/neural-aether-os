from __future__ import annotations

from .bus import Bus
from .registry import Agent, Registry


class Aether:
    """Userspace stand-in for the OS brain."""

    def __init__(self) -> None:
        self.bus = Bus()
        self.registry = Registry()
        self._seed()

    def _seed(self) -> None:
        self.registry.register(
            Agent(
                name="sentinel",
                capabilities=["proc.read", "net.observe"],
                notes="Watches process and network anomalies.",
            )
        )
        self.registry.register(
            Agent(
                name="scheduler-advisor",
                capabilities=["proc.nice"],
                notes="Suggests scheduling policy. Does not yet write the kernel runqueue.",
            )
        )
        self.registry.register(
            Agent(
                name="shell",
                capabilities=["intent.parse", "explain"],
                notes="Talks to the human.",
                running=True,
            )
        )
        self.bus.emit("boot", message="Aether control plane online (userspace)")

    def interpret(self, raw: str) -> str:
        text = raw.strip().lower()
        if not text:
            return ""
        if text in {"help", "?"}:
            return (
                "commands: status | what is running | spawn <agent> | "
                "stop <agent> | explain policy | events | help"
            )
        if text in {"status", "what is running"}:
            running = ", ".join(a.name for a in self.registry.running()) or "(none)"
            known = ", ".join(self.registry.agents)
            return f"running: {running}\nregistered: {known}"
        if text.startswith("spawn "):
            name = text.split(None, 1)[1]
            if name not in self.registry.agents:
                return f"unknown agent: {name}"
            agent = self.registry.spawn(name)
            self.bus.emit("spawn", agent=name)
            return f"spawned {agent.name} caps={agent.capabilities}"
        if text.startswith("stop "):
            name = text.split(None, 1)[1]
            if name not in self.registry.agents:
                return f"unknown agent: {name}"
            self.registry.stop(name)
            self.bus.emit("stop", agent=name)
            return f"stopped {name}"
        if text in {"explain policy", "explain"}:
            return (
                "Phase A: Linux owns hardware. Aether owns intent, "
                "capabilities, and narration. No ambient root inside the OS we are building."
            )
        if text in {"events", "log"}:
            lines = [f"{e.ts} {e.kind} {e.payload}" for e in self.bus.history[-12:]]
            return "\n".join(lines) or "(quiet)"
        self.bus.emit("intent.unknown", raw=raw)
        return (
            "I heard you, but I have no model plugged in yet. "
            "Try 'help'. Later this path calls a local LLM."
        )
