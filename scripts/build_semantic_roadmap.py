#!/usr/bin/env python3
"""Validate and render the semantic roadmap, with optional doc DAG support.

This script treats docs/roadmap/semantic-roadmap.json as the canonical source.
It performs integrity checks and generates docs/roadmap/ROADMAP.md.

With --docs, it also validates canonical doc frontmatter and generates
docs/_meta/doc-graph.json.
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
META_ROOT = ROOT.parent  # meta-repo root (BioregionKnwoledgeCommons/)
ROADMAP_DIR = ROOT / "docs" / "roadmap"
MODEL_PATH = ROADMAP_DIR / "semantic-roadmap.json"
SCHEMA_PATH = ROADMAP_DIR / "semantic-roadmap.schema.json"
OUTPUT_PATH = ROADMAP_DIR / "ROADMAP.md"
DOCS_DIR = ROOT / "docs"
META_DIR = DOCS_DIR / "_meta"
DOC_GRAPH_PATH = META_DIR / "doc-graph.json"

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


# ---------------------------------------------------------------------------
# Doc DAG support (requires --docs flag; yaml is lazy-imported)
# ---------------------------------------------------------------------------

VALID_DOC_KINDS = frozenset(
    ["vision", "foundation", "architecture", "spec", "operations", "research", "positioning"]
)

# external: namespaces resolvable against the meta-repo root
LOCAL_EXTERNAL_NAMESPACES = frozenset(["BioregionKnwoledgeCommons", "Octo"])


def _load_yaml() -> Any:
    """Lazy-import PyYAML; fail with a clear message if missing."""
    try:
        import yaml  # type: ignore
    except ImportError:
        raise SystemExit(
            "ERROR: PyYAML is required for --docs. Install with: pip install pyyaml"
        )
    return yaml


def parse_frontmatter(path: Path) -> dict[str, Any] | None:
    """Extract YAML frontmatter from a markdown file, or return None."""
    yaml = _load_yaml()
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip()
    try:
        data = yaml.safe_load(block)
    except Exception:
        return None
    if not isinstance(data, dict) or "doc_id" not in data:
        return None
    data["_file_path"] = str(path.relative_to(ROOT))
    return data


@dataclass
class DocNode:
    doc_id: str
    doc_kind: str
    status: str
    depends_on: list[str]
    file_path: str
    primary_for: list[str]


def scan_docs() -> dict[str, DocNode]:
    """Scan all markdown files under docs/ for frontmatter with doc_id."""
    nodes: dict[str, DocNode] = {}
    for md_path in sorted(DOCS_DIR.rglob("*.md")):
        if md_path.name.startswith(".") or "_meta" in md_path.parts:
            continue
        fm = parse_frontmatter(md_path)
        if fm is None:
            continue
        doc_id = fm["doc_id"]
        nodes[doc_id] = DocNode(
            doc_id=doc_id,
            doc_kind=fm.get("doc_kind", ""),
            status=fm.get("status", "draft"),
            depends_on=fm.get("depends_on", []),
            file_path=fm["_file_path"],
            primary_for=fm.get("primary_for", []),
        )
    return nodes


def validate_doc_dag(nodes: dict[str, DocNode]) -> list[str]:
    """Validate the doc DAG. Returns a list of error messages."""
    errors: list[str] = []

    # Check doc_kind values
    for doc_id, node in nodes.items():
        if node.doc_kind not in VALID_DOC_KINDS:
            errors.append(
                f"Doc {doc_id}: invalid doc_kind '{node.doc_kind}' "
                f"(must be one of {sorted(VALID_DOC_KINDS)})"
            )

    # Check depends_on targets exist
    for doc_id, node in nodes.items():
        for dep in node.depends_on:
            if dep not in nodes:
                errors.append(f"Doc {doc_id}: depends_on target '{dep}' not found")

    # Cycle detection (DFS)
    graph: dict[str, list[str]] = defaultdict(list)
    for doc_id, node in nodes.items():
        for dep in node.depends_on:
            graph[doc_id].append(dep)

    visiting: set[str] = set()
    visited: set[str] = set()

    def dfs(nid: str) -> None:
        if nid in visited:
            return
        if nid in visiting:
            errors.append(f"Cycle detected in doc depends_on graph at: {nid}")
            return
        visiting.add(nid)
        for nxt in graph.get(nid, []):
            dfs(nxt)
        visiting.discard(nid)
        visited.add(nid)

    for nid in nodes:
        dfs(nid)

    return errors


def resolve_source_doc(ref: str) -> tuple[str, str | None]:
    """Resolve a roadmap source_doc reference.

    Returns (status, resolved_path_or_None).
    status is one of: 'resolved', 'unvalidated', 'missing', 'url'.
    """
    if ref.startswith("http://") or ref.startswith("https://"):
        return ("url", None)

    if ref.startswith("external:"):
        rest = ref[len("external:"):]
        namespace = rest.split("/")[0] if "/" in rest else rest
        if namespace in LOCAL_EXTERNAL_NAMESPACES:
            candidate = META_ROOT / rest
            if candidate.exists():
                return ("resolved", str(candidate))
            return ("missing", str(candidate))
        return ("unvalidated", None)

    # Relative path — resolve against roadmap dir
    candidate = (ROADMAP_DIR / ref).resolve()
    if candidate.exists():
        return ("resolved", str(candidate))
    # Also try from docs/ root
    candidate2 = (DOCS_DIR / ref).resolve()
    if candidate2.exists():
        return ("resolved", str(candidate2))
    return ("missing", str(candidate))


def build_roadmap_links(model: Model) -> dict[str, list[str]]:
    """Map doc file paths to roadmap node ids via source_docs."""
    links: dict[str, list[str]] = defaultdict(list)
    for node in model.nodes_by_id.values():
        for ref in node.get("source_docs", []):
            status, resolved = resolve_source_doc(ref)
            if status == "resolved" and resolved:
                try:
                    rel = str(Path(resolved).relative_to(ROOT))
                except ValueError:
                    rel = resolved
                links[rel].append(node["id"])
    return dict(links)


def cross_validate_source_docs(
    model: Model, doc_nodes: dict[str, DocNode]
) -> list[str]:
    """Warn if roadmap source_docs point to archived docs."""
    warnings: list[str] = []
    doc_by_path = {n.file_path: n for n in doc_nodes.values()}
    for node in model.nodes_by_id.values():
        for ref in node.get("source_docs", []):
            status, resolved = resolve_source_doc(ref)
            if status == "resolved" and resolved:
                try:
                    rel = str(Path(resolved).relative_to(ROOT))
                except ValueError:
                    continue
                if rel in doc_by_path and doc_by_path[rel].status == "archived":
                    warnings.append(
                        f"Roadmap node {node['id']}: source_doc '{ref}' "
                        f"points to archived doc {doc_by_path[rel].doc_id}"
                    )
    return warnings


def count_unclassified_docs() -> list[str]:
    """List docs without frontmatter (informational, not errors)."""
    unclassified: list[str] = []
    for md_path in sorted(DOCS_DIR.rglob("*.md")):
        if md_path.name.startswith(".") or "_meta" in md_path.parts:
            continue
        if md_path.name in ("CLAUDE.md", "README.md"):
            continue
        fm = parse_frontmatter(md_path)
        if fm is None:
            unclassified.append(str(md_path.relative_to(ROOT)))
    return unclassified


def generate_doc_graph(
    doc_nodes: dict[str, DocNode],
    roadmap_links: dict[str, list[str]],
    unclassified: list[str],
    model: Model,
) -> dict[str, Any]:
    """Generate the doc-graph.json content."""
    nodes_out: dict[str, Any] = {}
    edges_out: list[dict[str, str]] = []

    for doc_id, node in sorted(doc_nodes.items()):
        nodes_out[doc_id] = {
            "doc_kind": node.doc_kind,
            "status": node.status,
            "file_path": node.file_path,
            "depends_on": node.depends_on,
            "primary_for": node.primary_for,
        }
        for dep in node.depends_on:
            edges_out.append({"from": doc_id, "to": dep, "type": "depends_on"})

    # Collect unvalidated external refs
    unvalidated: list[str] = []
    for node in model.nodes_by_id.values():
        for ref in node.get("source_docs", []):
            status, _ = resolve_source_doc(ref)
            if status == "unvalidated":
                if ref not in unvalidated:
                    unvalidated.append(ref)

    return {
        "generated_at": datetime.now(tz=UTC).isoformat(),
        "nodes": nodes_out,
        "edges": edges_out,
        "unclassified": unclassified,
        "roadmap_links": roadmap_links,
        "unvalidated_refs": sorted(unvalidated),
    }


def run_docs(check_only: bool, json_output: bool, model: Model) -> bool:
    """Run doc DAG validation and optionally generate doc-graph.json.

    Returns True if validation passed.
    """
    doc_nodes = scan_docs()

    if not doc_nodes:
        msg = "No docs with frontmatter found under docs/"
        if json_output:
            print(json.dumps({"status": "warning", "message": msg}))
        else:
            print(f"WARNING: {msg}")
        return True

    errors = validate_doc_dag(doc_nodes)
    warnings = cross_validate_source_docs(model, doc_nodes)
    unclassified = count_unclassified_docs()
    roadmap_links = build_roadmap_links(model)

    if json_output:
        result: dict[str, Any] = {
            "status": "error" if errors else "ok",
            "doc_count": len(doc_nodes),
            "errors": errors,
            "warnings": warnings,
            "unclassified_count": len(unclassified),
        }
        if not check_only:
            graph = generate_doc_graph(doc_nodes, roadmap_links, unclassified, model)
            result["doc_graph"] = graph
        print(json.dumps(result, indent=2))
    else:
        print(f"Doc DAG: {len(doc_nodes)} canonical docs found")
        if errors:
            for e in errors:
                print(f"  ERROR: {e}")
        else:
            print("  All checks passed")
        if warnings:
            for w in warnings:
                print(f"  WARNING: {w}")
        print(f"  {len(unclassified)} docs without frontmatter (unclassified)")

    if not check_only and not errors:
        graph = generate_doc_graph(doc_nodes, roadmap_links, unclassified, model)
        META_DIR.mkdir(parents=True, exist_ok=True)
        DOC_GRAPH_PATH.write_text(
            json.dumps(graph, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        if not json_output:
            print(f"  Generated {DOC_GRAPH_PATH.relative_to(ROOT)}")

    return len(errors) == 0


def run(check_only: bool, docs: bool = False, json_output: bool = False) -> None:
    schema = load_json(SCHEMA_PATH)
    data = load_json(MODEL_PATH)
    validate_with_jsonschema(schema, data)
    model = build_model(data)
    detect_cycles_depends_on(model)

    markdown = render_markdown(model)
    if not check_only:
        OUTPUT_PATH.write_text(markdown, encoding="utf-8")

    if docs:
        ok = run_docs(check_only=check_only, json_output=json_output, model=model)
        if not ok:
            raise ValidationError("Doc DAG validation failed (see errors above)")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build semantic roadmap markdown from canonical JSON model."
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Validate only; do not write ROADMAP.md or doc-graph.json.",
    )
    parser.add_argument(
        "--docs", action="store_true",
        help="Also validate/generate the doc DAG (requires PyYAML).",
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Machine-readable JSON output (for skill consumption).",
    )
    args = parser.parse_args()
    try:
        run(check_only=args.check, docs=args.docs, json_output=args.json)
    except ValidationError as exc:
        if args.json:
            print(json.dumps({"status": "error", "message": str(exc)}))
        else:
            print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
