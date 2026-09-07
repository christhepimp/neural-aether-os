from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Agent:
    name: str
    capabilities: list[str]
    restart: str = "on-failure"
    running: bool = False
    notes: str = ""


class Registry:
    def __init__(self) -> None:
        self.agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        self.agents[agent.name] = agent

    def spawn(self, name: str) -> Agent:
        agent = self.agents[name]
        agent.running = True
        return agent

    def stop(self, name: str) -> Agent:
        agent = self.agents[name]
        agent.running = False
        return agent

    def running(self) -> list[Agent]:
        return [a for a in self.agents.values() if a.running]
