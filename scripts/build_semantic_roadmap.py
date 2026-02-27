#!/usr/bin/env python3
"""Validate and render the semantic roadmap.

This script treats docs/roadmap/semantic-roadmap.json as the canonical source.
It performs integrity checks and generates docs/roadmap/ROADMAP.md.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ROADMAP_DIR = ROOT / "docs" / "roadmap"
MODEL_PATH = ROADMAP_DIR / "semantic-roadmap.json"
SCHEMA_PATH = ROADMAP_DIR / "semantic-roadmap.schema.json"
OUTPUT_PATH = ROADMAP_DIR / "ROADMAP.md"

PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
STATUS_ORDER = {"in_progress": 0, "planned": 1, "blocked": 2, "done": 3, "deprecated": 4}
HORIZON_ORDER = {"0-30d": 0, "30-90d": 1, "90-180d": 2, "180-365d": 3}


class ValidationError(Exception):
    """Raised when semantic roadmap validation fails."""


@dataclass
class Model:
    data: dict[str, Any]
    nodes_by_id: dict[str, dict[str, Any]]
    edges: list[dict[str, Any]]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_with_jsonschema(schema: dict[str, Any], model: dict[str, Any]) -> None:
    """Validate against JSON Schema when jsonschema is available."""
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(model), key=lambda e: e.path)
    if errors:
        first = errors[0]
        path = ".".join(str(p) for p in first.path)
        raise ValidationError(f"Schema validation failed at '{path}': {first.message}")


def build_model(model_data: dict[str, Any]) -> Model:
    nodes = model_data.get("nodes", [])
    edges = model_data.get("edges", [])

    nodes_by_id: dict[str, dict[str, Any]] = {}
    for node in nodes:
        node_id = node["id"]
        if node_id in nodes_by_id:
            raise ValidationError(f"Duplicate node id: {node_id}")
        nodes_by_id[node_id] = node

    for edge in edges:
        src = edge["from"]
        dst = edge["to"]
        if src not in nodes_by_id:
            raise ValidationError(f"Edge references unknown node in 'from': {src}")
        if dst not in nodes_by_id:
            raise ValidationError(f"Edge references unknown node in 'to': {dst}")

    return Model(data=model_data, nodes_by_id=nodes_by_id, edges=edges)


def detect_cycles_depends_on(model: Model) -> None:
    """Detect cycles in dependency edges.

    For `depends_on`, the semantic is: edge.from must complete before edge.to.
    """
    graph: dict[str, list[str]] = defaultdict(list)
    visiting: set[str] = set()
    visited: set[str] = set()

    for edge in model.edges:
        if edge["type"] == "depends_on":
            graph[edge["from"]].append(edge["to"])

    def dfs(node_id: str) -> None:
        if node_id in visited:
            return
        if node_id in visiting:
            raise ValidationError(f"Cycle detected in depends_on graph at node: {node_id}")
        visiting.add(node_id)
        for nxt in graph.get(node_id, []):
            dfs(nxt)
        visiting.remove(node_id)
        visited.add(node_id)

    for node_id in model.nodes_by_id:
        dfs(node_id)


def sorted_nodes(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def key(n: dict[str, Any]) -> tuple[int, int, int, str]:
        return (
            STATUS_ORDER.get(n.get("status", "planned"), 99),
            PRIORITY_ORDER.get(n.get("priority", "P3"), 99),
            HORIZON_ORDER.get(n.get("horizon", "180-365d"), 99),
            n.get("title", ""),
        )

    return sorted(nodes, key=key)


def nodes_of_kind(model: Model, kind: str) -> list[dict[str, Any]]:
    return [n for n in model.nodes_by_id.values() if n.get("kind") == kind]


def topological_work_order(model: Model) -> list[str]:
    work_ids = {n["id"] for n in nodes_of_kind(model, "work_item")}
    deps: dict[str, list[str]] = defaultdict(list)
    indegree: dict[str, int] = {wid: 0 for wid in work_ids}

    for edge in model.edges:
        if edge["type"] != "depends_on":
            continue
        src = edge["from"]
        dst = edge["to"]
        if src in work_ids and dst in work_ids:
            deps[src].append(dst)
            indegree[dst] += 1

    q = deque(sorted([wid for wid in work_ids if indegree[wid] == 0]))
    ordered: list[str] = []
    while q:
        node_id = q.popleft()
        ordered.append(node_id)
        for nxt in deps.get(node_id, []):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                q.append(nxt)

    for wid in work_ids:
        if wid not in ordered:
            ordered.append(wid)
    return ordered


def status_counts(model: Model) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for node in model.nodes_by_id.values():
        counts[node.get("status", "planned")] += 1
    return dict(counts)


def render_table(nodes: list[dict[str, Any]]) -> str:
    lines = [
        "| ID | Title | Status | Priority | Horizon | Owner |",
        "|---|---|---|---|---|---|",
    ]
    for n in sorted_nodes(nodes):
        lines.append(
            f"| `{n['id']}` | {n['title']} | `{n.get('status', '')}` | "
            f"`{n.get('priority', '')}` | `{n.get('horizon', '')}` | "
            f"`{n.get('owner', '')}` |"
        )
    return "\n".join(lines)


def render_markdown(model: Model) -> str:
    now = datetime.now(tz=UTC).strftime("%Y-%m-%d %H:%M UTC")
    counts = status_counts(model)
    outcomes = nodes_of_kind(model, "outcome")
    initiatives = nodes_of_kind(model, "initiative")
    work_items = nodes_of_kind(model, "work_item")
    decisions = nodes_of_kind(model, "decision")
    risks = nodes_of_kind(model, "risk")
    milestones = nodes_of_kind(model, "milestone")
    metrics = nodes_of_kind(model, "metric")

    work_order = topological_work_order(model)

    risk_mitigations: dict[str, list[str]] = defaultdict(list)
    for e in model.edges:
        if e["type"] == "mitigates" and model.nodes_by_id[e["to"]]["kind"] == "risk":
            risk_mitigations[e["to"]].append(e["from"])

    lines: list[str] = []
    lines.append("# Semantic Roadmap")
    lines.append("")
    lines.append(f"- Program: **{model.data['program']}**")
    lines.append(f"- Roadmap ID: `{model.data['roadmap_id']}`")
    lines.append(f"- Version: `{model.data['version']}`")
    lines.append(f"- As of: `{model.data['as_of']}`")
    lines.append(f"- Generated: `{now}`")
    lines.append("")
    lines.append("## Status Summary")
    lines.append("")
    lines.append("| Status | Count |")
    lines.append("|---|---|")
    for status in ("in_progress", "planned", "blocked", "done", "deprecated"):
        lines.append(f"| `{status}` | {counts.get(status, 0)} |")
    lines.append("")
    lines.append("## Outcomes")
    lines.append("")
    lines.append(render_table(outcomes))
    lines.append("")
    lines.append("## Initiatives")
    lines.append("")
    lines.append(render_table(initiatives))
    lines.append("")
    lines.append("## Work Items")
    lines.append("")
    lines.append(render_table(work_items))
    lines.append("")
    lines.append("### Dependency Execution Order (depends_on)")
    lines.append("")
    for idx, wid in enumerate(work_order, start=1):
        node = model.nodes_by_id[wid]
        lines.append(f"{idx}. `{wid}` — {node['title']} ({node['status']})")
    lines.append("")
    lines.append("## Risks and Mitigations")
    lines.append("")
    for risk in sorted_nodes(risks):
        mitigators = [f"`{rid}`" for rid in sorted(risk_mitigations.get(risk["id"], []))]
        mitigation_text = ", ".join(mitigators) if mitigators else "_none linked_"
        lines.append(f"- `{risk['id']}`: {risk['title']} | mitigated by: {mitigation_text}")
    lines.append("")
    lines.append("## Milestones")
    lines.append("")
    lines.append(render_table(milestones))
    lines.append("")
    lines.append("## Decisions")
    lines.append("")
    lines.append(render_table(decisions))
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    lines.append(render_table(metrics))
    lines.append("")
    lines.append("## Canonical Sources")
    lines.append("")
    lines.append("- Machine model: `docs/roadmap/semantic-roadmap.json`")
    lines.append("- Schema: `docs/roadmap/semantic-roadmap.schema.json`")
    lines.append("- JSON-LD context: `docs/roadmap/semantic-roadmap.context.json`")
    return "\n".join(lines) + "\n"


def run(check_only: bool) -> None:
    schema = load_json(SCHEMA_PATH)
    data = load_json(MODEL_PATH)
    validate_with_jsonschema(schema, data)
    model = build_model(data)
    detect_cycles_depends_on(model)

    markdown = render_markdown(model)
    if check_only:
        return
    OUTPUT_PATH.write_text(markdown, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build semantic roadmap markdown from canonical JSON model.")
    parser.add_argument("--check", action="store_true", help="Validate only; do not write ROADMAP.md.")
    args = parser.parse_args()
    try:
        run(check_only=args.check)
    except ValidationError as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
