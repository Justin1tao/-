from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


SCORE_KEYS = (
    'development_potential',
    'mental_health',
    'economic_pressure',
    'relationship_stability',
)


@dataclass(frozen=True)
class OptionSpec:
    option_id: str
    text: str
    next: str
    score_delta: dict[str, int]
    three_year_state: str
    cost: str
    repair_actions: str
    evidence_note: str = ''
    constraints: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class NodeSpec:
    node_id: str
    scene: str
    prompt: str
    options: dict[str, OptionSpec]
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RuleSet:
    version: int
    start_node: str
    low_mental_health_threshold: int
    nodes: dict[str, NodeSpec]


@dataclass
class SessionState:
    mode: str
    current_node_id: str
    scores: dict[str, int]
    history_stack: list[dict[str, Any]]
    risk_flags: list[str]
    profile: dict[str, Any]


@dataclass
class UserAction:
    kind: str
    option_id: str | None = None
    mode: str | None = None
    step: int | None = None
    text: str | None = None


@dataclass
class EngineResult:
    state: SessionState
    current_node: NodeSpec
    trajectory_card: str | None = None
    stabilizer_card: str | None = None
    crisis_message: str | None = None
