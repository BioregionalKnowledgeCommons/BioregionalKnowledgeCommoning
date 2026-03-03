#!/usr/bin/env python3
"""Back-populate github_url into semantic-roadmap.json from existing GitHub issues.

Reads the canonical roadmap JSON, queries GitHub issues with the SR: prefix,
matches them to roadmap nodes via the <!-- roadmap-node-id:... --> body marker
(fallback: SR: title prefix), and writes the github_url back into each node.

Idempotent — safe to run multiple times.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "docs" / "roadmap" / "semantic-roadmap.json"
DEFAULT_REPO = "BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning"
MANAGED_PREFIX = "SR:"


def run_gh(args: list[str]) -> Any:
    result = subprocess.run(
        ["gh", *args],
        check=True,
        text=True,
        capture_output=True,
        timeout=120,
    )
    out = result.stdout.strip()
    return json.loads(out) if out else []


def extract_node_id_from_marker(body: str) -> str | None:
    if not body:
        return None
    match = re.search(r"<!--\s*roadmap-node-id:([a-z0-9._:-]+)\s*-->", body)
    return match.group(1) if match else None


def extract_node_id_from_title(title: str) -> str | None:
    if not title.startswith(MANAGED_PREFIX):
        return None
    rest = title[len(MANAGED_PREFIX):]
    if " | " not in rest:
        return None
    return rest.split(" | ", 1)[0].strip()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Backfill github_url into roadmap JSON.")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--repo", default=DEFAULT_REPO)
    parser.add_argument("--apply", action="store_true", help="Write changes (default is dry-run).")
    args = parser.parse_args()

    model_path: Path = args.model
    with model_path.open("r", encoding="utf-8") as f:
        model = json.load(f)

    nodes_by_id: dict[str, dict[str, Any]] = {}
    for node in model.get("nodes", []):
        nodes_by_id[node["id"]] = node

    # Query all SR: issues from the repo
    issues = run_gh([
        "issue", "list",
        "--repo", args.repo,
        "--state", "all",
        "--limit", "500",
        "--search", "SR:",
        "--json", "number,title,body,url",
    ])

    matched = 0
    already_set = 0
    unmatched = []

    for issue in issues:
        title = issue.get("title", "")
        body = issue.get("body", "") or ""
        url = issue.get("url", "")
        number = issue.get("number", 0)

        node_id = extract_node_id_from_marker(body) or extract_node_id_from_title(title)
        if not node_id:
            unmatched.append(f"  #{number}: {title}")
            continue

        node = nodes_by_id.get(node_id)
        if not node:
            unmatched.append(f"  #{number}: {title} (node_id={node_id} not in roadmap)")
            continue

        if node.get("github_url") == url:
            already_set += 1
            continue

        node["github_url"] = url
        matched += 1
        print(f"  {node_id} -> {url}")

    total = len(nodes_by_id)
    with_url = sum(1 for n in nodes_by_id.values() if n.get("github_url"))

    print(f"\nResults: {matched} newly linked, {already_set} already set, {with_url}/{total} nodes have github_url")

    if unmatched:
        print(f"\nUnmatched issues ({len(unmatched)}):")
        for line in unmatched:
            print(line)

    if args.apply and matched > 0:
        with model_path.open("w", encoding="utf-8") as f:
            json.dump(model, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"\nWrote {model_path}")
    elif matched > 0:
        print(f"\nDRY-RUN: would write {matched} changes to {model_path}. Use --apply to save.")
    else:
        print("\nNo changes needed.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
