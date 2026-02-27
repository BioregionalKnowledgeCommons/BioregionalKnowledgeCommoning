#!/usr/bin/env python3
"""Sync semantic roadmap nodes into a GitHub Project (ProjectV2).

Design goals:
- Idempotent updates keyed by managed title prefix: `SR:<node_id> | ...`
- Safe default (dry-run). Use --apply to mutate project state.
- Two sync modes:
  - draft: project draft items only (legacy mode)
  - issue: real GitHub issues + richer project mapping
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = ROOT / "docs" / "roadmap" / "semantic-roadmap.json"
MANAGED_PREFIX = "SR:"
MANAGED_MARKER_PREFIX = "<!-- roadmap-node-id:"
DEFAULT_REPO = "BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning"

DEFAULT_KINDS = {"initiative", "work_item", "milestone"}
DEFAULT_MODE = "draft"
BLOCKED_BY_FIELD_NAME = "Blocked by"


@dataclass
class FieldInfo:
    id: str
    options: dict[str, str]
    field_type: str


@dataclass
class IssueInfo:
    number: int
    title: str
    body: str
    state: str
    labels: set[str]
    milestone_title: str | None
    url: str


@dataclass
class RepoMilestone:
    number: int
    title: str
    due_on: str | None
    description: str | None


class SyncError(Exception):
    """Raised for sync failures."""


def run_gh(args: list[str], expect_json: bool = False, input_data: str | None = None) -> Any:
    cmd = ["gh", *args]
    try:
        result = subprocess.run(
            cmd,
            check=True,
            text=True,
            capture_output=True,
            input=input_data,
            timeout=120,
        )
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise SyncError(f"Command failed: {' '.join(cmd)}\n{stderr}") from exc
    except subprocess.TimeoutExpired as exc:
        raise SyncError(f"Command timed out after 120s: {' '.join(cmd)}") from exc
    out = result.stdout.strip()
    if expect_json:
        if not out:
            return {}
        return json.loads(out)
    return out


def gh_api(endpoint: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
    args = ["api", endpoint, "-X", method]
    input_data = None
    if payload is not None:
        args.extend(["--input", "-"])
        input_data = json.dumps(payload)
    return run_gh(args, expect_json=True, input_data=input_data)


def load_model(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_project_meta(
    owner: str,
    number: int,
    *,
    apply: bool,
    ensure_fields: bool = False,
    blocked_by_field_name: str = BLOCKED_BY_FIELD_NAME,
) -> tuple[str, dict[str, FieldInfo]]:
    project = run_gh(
        ["project", "view", str(number), "--owner", owner, "--format", "json"],
        expect_json=True,
    )
    project_id = project["id"]

    def _load_fields() -> dict[str, FieldInfo]:
        fields_raw = run_gh(
            ["project", "field-list", str(number), "--owner", owner, "--format", "json"],
            expect_json=True,
        )
        parsed: dict[str, FieldInfo] = {}
        for field in fields_raw.get("fields", []):
            name = field["name"]
            options: dict[str, str] = {}
            for opt in field.get("options", []):
                options[opt["name"]] = opt["id"]
            parsed[name] = FieldInfo(id=field["id"], options=options, field_type=field["type"])
        return parsed

    fields = _load_fields()

    required = ["Status", "Priority", "Target date"]
    missing = [name for name in required if name not in fields]
    if missing:
        raise SyncError(f"Project is missing required fields: {', '.join(missing)}")

    if ensure_fields and blocked_by_field_name not in fields:
        if not apply:
            print(f"DRY-RUN: would create missing project field '{blocked_by_field_name}' (TEXT)")
        else:
            print(f"Creating missing project field: {blocked_by_field_name} (TEXT)")
            run_gh(
                [
                    "project",
                    "field-create",
                    str(number),
                    "--owner",
                    owner,
                    "--name",
                    blocked_by_field_name,
                    "--data-type",
                    "TEXT",
                ]
            )
            fields = _load_fields()

    return project_id, fields


def list_items(owner: str, number: int) -> list[dict[str, Any]]:
    payload = run_gh(
        ["project", "item-list", str(number), "--owner", owner, "--format", "json"],
        expect_json=True,
    )
    return payload.get("items", [])


def desired_title(node: dict[str, Any]) -> str:
    return f"{MANAGED_PREFIX}{node['id']} | {node['title']}"


def extract_managed_node_id(title: str) -> str | None:
    if not title.startswith(MANAGED_PREFIX):
        return None
    rest = title[len(MANAGED_PREFIX) :]
    if " | " not in rest:
        return None
    return rest.split(" | ", 1)[0].strip()


def extract_node_id_from_marker(body: str) -> str | None:
    if not body:
        return None
    match = re.search(r"<!--\s*roadmap-node-id:([a-z0-9._:-]+)\s*-->", body)
    if match:
        return match.group(1)
    return None


def node_sort_key(node: dict[str, Any]) -> tuple[str, str, str]:
    return (node.get("kind", ""), node.get("priority", "P2"), node.get("title", ""))


def map_status(value: str) -> str:
    return {
        "planned": "Todo",
        "in_progress": "In progress",
        "blocked": "Todo",
        "done": "Done",
        "deprecated": "Done",
    }.get(value, "Todo")


def map_priority(value: str) -> str:
    return {
        "P0": "P0",
        "P1": "P1",
        "P2": "P2",
        "P3": "P2",
    }.get(value, "P2")


def horizon_window(as_of: str, horizon: str | None) -> tuple[str | None, str | None]:
    if not horizon:
        return None, None
    try:
        base = date.fromisoformat(as_of)
    except ValueError:
        return None, None
    offsets = {
        "0-30d": (0, 30),
        "30-90d": (30, 90),
        "90-180d": (90, 180),
        "180-365d": (180, 365),
    }
    window = offsets.get(horizon)
    if not window:
        return None, None
    start = base + timedelta(days=window[0])
    end = base + timedelta(days=window[1])
    return start.isoformat(), end.isoformat()


def node_start_date(model: dict[str, Any], node: dict[str, Any]) -> str | None:
    metadata = node.get("metadata") or {}
    explicit = metadata.get("start_date")
    if explicit:
        return explicit
    start, _ = horizon_window(model.get("as_of", ""), node.get("horizon"))
    return start


def node_target_date(model: dict[str, Any], node: dict[str, Any]) -> str | None:
    metadata = node.get("metadata") or {}
    if node.get("due_date"):
        return node["due_date"]
    explicit = metadata.get("target_date")
    if explicit:
        return explicit
    _, end = horizon_window(model.get("as_of", ""), node.get("horizon"))
    return end


def managed_marker(node_id: str) -> str:
    return f"{MANAGED_MARKER_PREFIX}{node_id} -->"


def make_body(
    model: dict[str, Any],
    node: dict[str, Any],
    *,
    dependency_refs: list[str] | None = None,
    delivers_refs: list[str] | None = None,
) -> str:
    lines: list[str] = []
    lines.append(managed_marker(node["id"]))
    lines.append(f"Canonical roadmap node: `{node['id']}`")
    lines.append("")
    lines.append(f"- Program: {model['program']}")
    lines.append(f"- Roadmap: `{model['roadmap_id']}` v{model['version']} (as_of {model['as_of']})")
    lines.append(f"- Kind: `{node.get('kind', '')}`")
    lines.append(f"- Status: `{node.get('status', '')}`")
    lines.append(f"- Priority: `{node.get('priority', '')}`")
    lines.append(f"- Horizon: `{node.get('horizon', '')}`")
    lines.append(f"- Owner: `{node.get('owner', '')}`")
    start = node_start_date(model, node)
    target = node_target_date(model, node)
    if start:
        lines.append(f"- Start date: `{start}`")
    if target:
        lines.append(f"- Target date: `{target}`")
    lines.append("")
    summary = node.get("summary", "").strip()
    if summary:
        lines.append("## Summary")
        lines.append(summary)
        lines.append("")
    if dependency_refs:
        lines.append("## Depends On")
        for dep in dependency_refs:
            lines.append(dep)
        lines.append("")
    if delivers_refs:
        lines.append("## Delivers To")
        for ref in delivers_refs:
            lines.append(ref)
        lines.append("")
    source_docs = node.get("source_docs", [])
    if source_docs:
        lines.append("## Source Docs")
        for src in source_docs:
            lines.append(f"- {src}")
        lines.append("")
    lines.append("Generated by `scripts/sync_roadmap_to_github_project.py`.")
    return "\n".join(lines)


def edit_single_select(
    *,
    apply: bool,
    project_id: str,
    item_id: str,
    field_id: str,
    option_id: str,
    label: str,
) -> None:
    if not apply:
        print(f"DRY-RUN: set {label} on {item_id} -> option {option_id}")
        return
    run_gh(
        [
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            project_id,
            "--field-id",
            field_id,
            "--single-select-option-id",
            option_id,
        ]
    )


def edit_date(
    *,
    apply: bool,
    project_id: str,
    item_id: str,
    field_id: str,
    date_value: str | None,
    label: str,
) -> None:
    if not date_value:
        if not apply:
            print(f"DRY-RUN: clear {label} on {item_id}")
            return
        run_gh(
            [
                "project",
                "item-edit",
                "--id",
                item_id,
                "--project-id",
                project_id,
                "--field-id",
                field_id,
                "--clear",
            ]
        )
        return
    if not apply:
        print(f"DRY-RUN: set {label} on {item_id} -> {date_value}")
        return
    run_gh(
        [
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            project_id,
            "--field-id",
            field_id,
            "--date",
            date_value,
        ]
    )


def edit_text(
    *,
    apply: bool,
    project_id: str,
    item_id: str,
    field_id: str,
    text_value: str | None,
    label: str,
) -> None:
    if not text_value:
        if not apply:
            print(f"DRY-RUN: clear {label} on {item_id}")
            return
        run_gh(
            [
                "project",
                "item-edit",
                "--id",
                item_id,
                "--project-id",
                project_id,
                "--field-id",
                field_id,
                "--clear",
            ]
        )
        return
    if not apply:
        print(f"DRY-RUN: set {label} on {item_id} -> {text_value}")
        return
    run_gh(
        [
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            project_id,
            "--field-id",
            field_id,
            "--text",
            text_value,
        ]
    )


def apply_project_fields(
    *,
    apply: bool,
    project_id: str,
    fields: dict[str, FieldInfo],
    item_id: str,
    model: dict[str, Any],
    node: dict[str, Any],
    blocked_by_text: str | None,
    blocked_by_field_name: str,
) -> None:
    status_name = map_status(node.get("status", "planned"))
    priority_name = map_priority(node.get("priority", "P2"))
    status_option_id = fields["Status"].options.get(status_name)
    priority_option_id = fields["Priority"].options.get(priority_name)
    if not status_option_id:
        raise SyncError(f"Project Status option missing: {status_name}")
    if not priority_option_id:
        raise SyncError(f"Project Priority option missing: {priority_name}")

    edit_single_select(
        apply=apply,
        project_id=project_id,
        item_id=item_id,
        field_id=fields["Status"].id,
        option_id=status_option_id,
        label="Status",
    )
    edit_single_select(
        apply=apply,
        project_id=project_id,
        item_id=item_id,
        field_id=fields["Priority"].id,
        option_id=priority_option_id,
        label="Priority",
    )
    if "Start date" in fields:
        edit_date(
            apply=apply,
            project_id=project_id,
            item_id=item_id,
            field_id=fields["Start date"].id,
            date_value=node_start_date(model, node),
            label="Start date",
        )
    edit_date(
        apply=apply,
        project_id=project_id,
        item_id=item_id,
        field_id=fields["Target date"].id,
        date_value=node_target_date(model, node),
        label="Target date",
    )
    blocked_by_field = fields.get(blocked_by_field_name)
    if blocked_by_field:
        edit_text(
            apply=apply,
            project_id=project_id,
            item_id=item_id,
            field_id=blocked_by_field.id,
            text_value=blocked_by_text,
            label=blocked_by_field_name,
        )


def list_repo_issues(repo: str) -> dict[str, IssueInfo]:
    payload = run_gh(
        [
            "issue",
            "list",
            "--repo",
            repo,
            "--state",
            "all",
            "--limit",
            "500",
            "--search",
            "SR:",
            "--json",
            "number,title,body,state,labels,milestone,url",
        ],
        expect_json=True,
    )
    by_node_id: dict[str, IssueInfo] = {}
    for issue in payload:
        title = issue.get("title", "")
        body = issue.get("body", "") or ""
        node_id = extract_node_id_from_marker(body) or extract_managed_node_id(title)
        if not node_id:
            continue
        labels = {label.get("name", "") for label in issue.get("labels", []) if label.get("name")}
        milestone = issue.get("milestone")
        milestone_title = milestone.get("title") if milestone else None
        by_node_id[node_id] = IssueInfo(
            number=issue["number"],
            title=title,
            body=body,
            state=issue.get("state", "OPEN"),
            labels=labels,
            milestone_title=milestone_title,
            url=issue.get("url", ""),
        )
    return by_node_id


def list_repo_labels(repo: str) -> set[str]:
    labels = run_gh(
        ["label", "list", "--repo", repo, "--limit", "500", "--json", "name"],
        expect_json=True,
    )
    return {x["name"] for x in labels}


def label_color(name: str) -> str:
    if name == "roadmap":
        return "1F6FEB"
    if name.startswith("kind:"):
        kind = name.split(":", 1)[1]
        return {
            "initiative": "0E8A16",
            "work_item": "5319E7",
            "milestone": "FBCA04",
            "outcome": "0052CC",
            "decision": "1D76DB",
            "risk": "D93F0B",
            "metric": "BFDADC",
        }.get(kind, "6E7781")
    if name.startswith("horizon:"):
        return "A371F7"
    if name.startswith("status:"):
        status = name.split(":", 1)[1]
        return {
            "planned": "6E7781",
            "in_progress": "0E8A16",
            "blocked": "D93F0B",
            "done": "1A7F37",
            "deprecated": "8B949E",
        }.get(status, "6E7781")
    if name.startswith("tag:"):
        return "6E7781"
    return "6E7781"


def ensure_repo_labels(*, apply: bool, repo: str, names: set[str]) -> None:
    existing = list_repo_labels(repo)
    missing = sorted(names - existing)
    for name in missing:
        if not apply:
            print(f"DRY-RUN: create label '{name}' in {repo}")
            continue
        run_gh(
            [
                "label",
                "create",
                name,
                "--repo",
                repo,
                "--color",
                label_color(name),
                "--description",
                f"Managed by semantic roadmap sync ({name})",
            ]
        )


def managed_label_names(node: dict[str, Any]) -> set[str]:
    labels: set[str] = {"roadmap"}
    kind = node.get("kind")
    if kind:
        labels.add(f"kind:{kind}")
    horizon = node.get("horizon")
    if horizon:
        labels.add(f"horizon:{horizon}")
    status = node.get("status")
    if status:
        labels.add(f"status:{status}")
    for tag in node.get("tags", []) or []:
        safe = re.sub(r"[^a-z0-9._:-]+", "-", tag.strip().lower()).strip("-")
        if safe:
            labels.add(f"tag:{safe}")
    return labels


def is_managed_label(label: str) -> bool:
    return (
        label == "roadmap"
        or label.startswith("kind:")
        or label.startswith("horizon:")
        or label.startswith("status:")
        or label.startswith("tag:")
    )


def list_repo_milestones(repo: str) -> dict[str, RepoMilestone]:
    payload = run_gh(
        ["api", f"repos/{repo}/milestones?state=all&per_page=100"],
        expect_json=True,
    )
    by_title: dict[str, RepoMilestone] = {}
    for ms in payload:
        by_title[ms["title"]] = RepoMilestone(
            number=ms["number"],
            title=ms["title"],
            due_on=ms.get("due_on"),
            description=ms.get("description"),
        )
    return by_title


def ensure_repo_milestones(
    *,
    apply: bool,
    repo: str,
    milestone_nodes: dict[str, dict[str, Any]],
) -> dict[str, RepoMilestone]:
    existing = list_repo_milestones(repo)
    out = dict(existing)
    for node in sorted(milestone_nodes.values(), key=node_sort_key):
        title = node["title"]
        due_iso = node.get("due_date")
        due_ts = f"{due_iso}T00:00:00Z" if due_iso else None
        if title not in out:
            if not apply:
                print(f"DRY-RUN: create repo milestone '{title}' due={due_ts or 'none'}")
                out[title] = RepoMilestone(number=-1, title=title, due_on=due_ts, description=node.get("summary"))
            else:
                payload: dict[str, Any] = {
                    "title": title,
                    "description": node.get("summary", "")[:1024],
                }
                if due_ts:
                    payload["due_on"] = due_ts
                created = gh_api(f"repos/{repo}/milestones", method="POST", payload=payload)
                out[title] = RepoMilestone(
                    number=created["number"],
                    title=created["title"],
                    due_on=created.get("due_on"),
                    description=created.get("description"),
                )
                print(f"Created repo milestone '{title}' (#{created['number']})")
        else:
            existing_ms = out[title]
            if apply and existing_ms.number > 0 and existing_ms.due_on != due_ts:
                patch_payload: dict[str, Any] = {}
                if due_ts:
                    patch_payload["due_on"] = due_ts
                else:
                    patch_payload["due_on"] = None
                gh_api(f"repos/{repo}/milestones/{existing_ms.number}", method="PATCH", payload=patch_payload)
                print(f"Updated milestone due date '{title}' -> {due_ts or 'none'}")
                out[title] = RepoMilestone(
                    number=existing_ms.number,
                    title=existing_ms.title,
                    due_on=due_ts,
                    description=existing_ms.description,
                )
            elif not apply and existing_ms.due_on != due_ts:
                print(f"DRY-RUN: update milestone due date '{title}' -> {due_ts or 'none'}")
    return out


def choose_milestone_for_node(
    *,
    node_id: str,
    node_to_milestone_nodes: dict[str, list[dict[str, Any]]],
    repo_milestones_by_title: dict[str, RepoMilestone],
) -> RepoMilestone | None:
    candidates = node_to_milestone_nodes.get(node_id, [])
    if not candidates:
        return None
    ordered = sorted(
        candidates,
        key=lambda n: (
            n.get("due_date") or "9999-12-31",
            n.get("title", ""),
        ),
    )
    title = ordered[0]["title"]
    return repo_milestones_by_title.get(title)


def upsert_issue(
    *,
    apply: bool,
    repo: str,
    model: dict[str, Any],
    node: dict[str, Any],
    existing_issue: IssueInfo | None,
    dependency_refs: list[str],
    delivers_refs: list[str],
    desired_labels: set[str],
    milestone: RepoMilestone | None,
) -> IssueInfo:
    title = desired_title(node)
    body = make_body(model, node, dependency_refs=dependency_refs, delivers_refs=delivers_refs)
    current = existing_issue
    if current is None:
        if not apply:
            print(f"DRY-RUN: create issue '{title}'")
            return IssueInfo(
                number=-1,
                title=title,
                body=body,
                state="OPEN",
                labels=set(desired_labels),
                milestone_title=milestone.title if milestone else None,
                url=f"https://github.com/{repo}/issues/dry-run-{node['id']}",
            )
        payload: dict[str, Any] = {"title": title, "body": body}
        if milestone and milestone.number > 0:
            payload["milestone"] = milestone.number
        if desired_labels:
            payload["labels"] = sorted(desired_labels)
        created = gh_api(f"repos/{repo}/issues", method="POST", payload=payload)
        print(f"Created issue #{created['number']} for {node['id']}")
        return IssueInfo(
            number=created["number"],
            title=created["title"],
            body=created.get("body", ""),
            state=created.get("state", "open"),
            labels=set(desired_labels),
            milestone_title=milestone.title if milestone else None,
            url=created["html_url"],
        )

    labels_without_managed = {name for name in current.labels if not is_managed_label(name)}
    final_labels = sorted(labels_without_managed | desired_labels)
    target_milestone_num = milestone.number if milestone and milestone.number > 0 else None
    target_milestone_title = milestone.title if milestone else None

    changed = (
        current.title != title
        or current.body != body
        or set(final_labels) != current.labels
        or current.milestone_title != target_milestone_title
    )
    if not changed:
        return current

    if not apply:
        print(f"DRY-RUN: update issue #{current.number} ({node['id']})")
        return IssueInfo(
            number=current.number,
            title=title,
            body=body,
            state=current.state,
            labels=set(final_labels),
            milestone_title=target_milestone_title,
            url=current.url,
        )

    payload: dict[str, Any] = {
        "title": title,
        "body": body,
        "labels": final_labels,
        "milestone": target_milestone_num,
    }
    updated = gh_api(f"repos/{repo}/issues/{current.number}", method="PATCH", payload=payload)
    print(f"Updated issue #{current.number} ({node['id']})")
    return IssueInfo(
        number=updated["number"],
        title=updated["title"],
        body=updated.get("body", ""),
        state=updated.get("state", "open"),
        labels=set(label["name"] for label in updated.get("labels", [])),
        milestone_title=updated.get("milestone", {}).get("title") if updated.get("milestone") else None,
        url=updated["html_url"],
    )


def add_issue_to_project_if_needed(
    *,
    apply: bool,
    owner: str,
    project_number: int,
    issue_url: str,
    project_item_by_url: dict[str, dict[str, Any]],
) -> str:
    if issue_url in project_item_by_url:
        return project_item_by_url[issue_url]["id"]
    if not apply:
        print(f"DRY-RUN: add issue to project: {issue_url}")
        return f"dry-run:item:{issue_url}"
    created = run_gh(
        [
            "project",
            "item-add",
            str(project_number),
            "--owner",
            owner,
            "--url",
            issue_url,
            "--format",
            "json",
        ],
        expect_json=True,
    )
    item_id = created["id"]
    print(f"Added issue to project: {issue_url} ({item_id})")
    return item_id


def upsert_draft_item(
    *,
    apply: bool,
    owner: str,
    project_number: int,
    model: dict[str, Any],
    node: dict[str, Any],
    existing_item: dict[str, Any] | None,
) -> str:
    target_title = desired_title(node)
    body = make_body(model, node)
    if existing_item:
        item_id = existing_item["id"]
        draft_content_id = existing_item.get("content", {}).get("id")
        current_title = existing_item.get("title", "")
        if current_title != target_title:
            if not draft_content_id:
                print(f"WARN: cannot update title for non-draft item {item_id}")
            elif not apply:
                print(f"DRY-RUN: update title {draft_content_id}: '{current_title}' -> '{target_title}'")
            else:
                run_gh(["project", "item-edit", "--id", draft_content_id, "--title", target_title])
        # NOTE: gh CLI currently fails on body-only updates for draft issues
        # ("Title can't be blank"), so body is set on create and left unchanged
        # on update.
        return item_id
    if not apply:
        print(f"DRY-RUN: create draft item '{target_title}'")
        return f"dry-run:{node['id']}"
    created = run_gh(
        [
            "project",
            "item-create",
            str(project_number),
            "--owner",
            owner,
            "--title",
            target_title,
            "--body",
            body,
            "--format",
            "json",
        ],
        expect_json=True,
    )
    item_id = created["id"]
    print(f"Created draft: {target_title} ({item_id})")
    return item_id


def build_graph_indexes(
    model: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[str, list[str]], dict[str, list[str]], dict[str, list[dict[str, Any]]]]:
    nodes_by_id = {node["id"]: node for node in model.get("nodes", [])}
    depends_on_by_node: dict[str, list[str]] = defaultdict(list)
    delivers_to_by_node: dict[str, list[str]] = defaultdict(list)
    node_to_milestone_nodes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    milestone_nodes = {n_id: node for n_id, node in nodes_by_id.items() if node.get("kind") == "milestone"}

    for edge in model.get("edges", []):
        edge_type = edge.get("type")
        from_id = edge.get("from")
        to_id = edge.get("to")
        if not from_id or not to_id:
            continue
        if edge_type == "depends_on":
            depends_on_by_node[to_id].append(from_id)
        if edge_type == "delivers":
            delivers_to_by_node[from_id].append(to_id)
            if to_id in milestone_nodes and from_id in nodes_by_id:
                node_to_milestone_nodes[from_id].append(milestone_nodes[to_id])

    for node_id in list(depends_on_by_node):
        depends_on_by_node[node_id] = sorted(set(depends_on_by_node[node_id]))
    for node_id in list(delivers_to_by_node):
        delivers_to_by_node[node_id] = sorted(set(delivers_to_by_node[node_id]))
    return nodes_by_id, depends_on_by_node, delivers_to_by_node, node_to_milestone_nodes


def dependencies_text_for_project(
    *,
    node_id: str,
    depends_on_by_node: dict[str, list[str]],
    nodes_by_id: dict[str, dict[str, Any]],
    issue_by_node: dict[str, IssueInfo],
) -> str | None:
    deps = depends_on_by_node.get(node_id, [])
    if not deps:
        return None
    unresolved: list[str] = []
    for dep_id in deps:
        dep_node = nodes_by_id.get(dep_id) or {}
        dep_status = dep_node.get("status")
        if dep_status in {"done", "deprecated"}:
            continue
        issue = issue_by_node.get(dep_id)
        if issue and issue.number > 0:
            unresolved.append(f"{dep_id} (#{issue.number})")
        else:
            unresolved.append(dep_id)
    if not unresolved:
        return None
    return ", ".join(unresolved)


def dependency_refs_for_body(
    *,
    node_id: str,
    depends_on_by_node: dict[str, list[str]],
    nodes_by_id: dict[str, dict[str, Any]],
    issue_by_node: dict[str, IssueInfo],
) -> list[str]:
    deps = depends_on_by_node.get(node_id, [])
    refs: list[str] = []
    for dep_id in deps:
        dep_node = nodes_by_id.get(dep_id) or {}
        dep_title = dep_node.get("title", dep_id)
        dep_status = dep_node.get("status", "planned")
        checkbox = "x" if dep_status in {"done", "deprecated"} else " "
        issue = issue_by_node.get(dep_id)
        if issue and issue.number > 0:
            refs.append(f"- [{checkbox}] #{issue.number} `{dep_id}` — {dep_title}")
        else:
            refs.append(f"- [{checkbox}] `{dep_id}` — {dep_title}")
    return refs


def delivers_refs_for_body(
    *,
    node_id: str,
    delivers_to_by_node: dict[str, list[str]],
    nodes_by_id: dict[str, dict[str, Any]],
    issue_by_node: dict[str, IssueInfo],
) -> list[str]:
    targets = delivers_to_by_node.get(node_id, [])
    refs: list[str] = []
    for target_id in targets:
        target_node = nodes_by_id.get(target_id) or {}
        target_title = target_node.get("title", target_id)
        issue = issue_by_node.get(target_id)
        if issue and issue.number > 0:
            refs.append(f"- #{issue.number} `{target_id}` — {target_title}")
        else:
            refs.append(f"- `{target_id}` — {target_title}")
    return refs


def sync(
    *,
    owner: str,
    project_number: int,
    model_path: Path,
    apply: bool,
    archive_stale: bool,
    kinds: set[str],
    mode: str,
    repo: str,
    ensure_fields: bool,
    blocked_by_field_name: str,
) -> None:
    model = load_model(model_path)
    project_id, fields = get_project_meta(
        owner,
        project_number,
        apply=apply,
        ensure_fields=ensure_fields,
        blocked_by_field_name=blocked_by_field_name,
    )
    items = list_items(owner, project_number)

    managed_items_by_node_id: dict[str, list[dict[str, Any]]] = defaultdict(list)
    project_item_by_url: dict[str, dict[str, Any]] = {}
    for item in items:
        title = item.get("title") or item.get("content", {}).get("title") or ""
        node_id = extract_managed_node_id(title)
        if node_id:
            managed_items_by_node_id[node_id].append(item)
        content = item.get("content") or {}
        if content.get("type") == "Issue":
            url = content.get("url")
            if url:
                project_item_by_url[url] = item

    desired_nodes = [node for node in model.get("nodes", []) if node.get("kind") in kinds]
    desired_nodes.sort(key=node_sort_key)
    desired_ids = {node["id"] for node in desired_nodes}

    print(f"Project #{project_number} owner={owner} project_id={project_id}")
    print(f"Managed existing items: {sum(len(v) for v in managed_items_by_node_id.values())}")
    print(f"Desired nodes to sync: {len(desired_nodes)}")
    print(f"Mode: {'APPLY' if apply else 'DRY-RUN'} ({mode})")

    nodes_by_id, depends_on_by_node, delivers_to_by_node, node_to_milestone_nodes = build_graph_indexes(model)
    processed_project_item_ids: set[str] = set()
    issue_by_node: dict[str, IssueInfo] = {}

    if mode == "issue":
        repo_issues_by_node = list_repo_issues(repo)
        needed_labels: set[str] = set()
        for node in desired_nodes:
            needed_labels.update(managed_label_names(node))
        ensure_repo_labels(apply=apply, repo=repo, names=needed_labels)

        milestone_nodes = {node["id"]: node for node in model.get("nodes", []) if node.get("kind") == "milestone"}
        repo_milestones_by_title = ensure_repo_milestones(
            apply=apply,
            repo=repo,
            milestone_nodes=milestone_nodes,
        )

        # Pass 1: ensure issue exists for every desired node.
        for node in desired_nodes:
            existing_issue = repo_issues_by_node.get(node["id"])
            milestone = choose_milestone_for_node(
                node_id=node["id"],
                node_to_milestone_nodes=node_to_milestone_nodes,
                repo_milestones_by_title=repo_milestones_by_title,
            )
            # Temporary body refs in pass 1 (node ids only); pass 2 refreshes with issue refs.
            dep_refs = [f"- [ ] `{dep}`" for dep in depends_on_by_node.get(node["id"], [])]
            deliver_refs = [f"- `{target}`" for target in delivers_to_by_node.get(node["id"], [])]
            issue = upsert_issue(
                apply=apply,
                repo=repo,
                model=model,
                node=node,
                existing_issue=existing_issue,
                dependency_refs=dep_refs,
                delivers_refs=deliver_refs,
                desired_labels=managed_label_names(node),
                milestone=milestone,
            )
            issue_by_node[node["id"]] = issue

        # Pass 2: rewrite bodies with resolved issue references.
        for node in desired_nodes:
            current_issue = issue_by_node[node["id"]]
            milestone = choose_milestone_for_node(
                node_id=node["id"],
                node_to_milestone_nodes=node_to_milestone_nodes,
                repo_milestones_by_title=repo_milestones_by_title,
            )
            dep_refs = dependency_refs_for_body(
                node_id=node["id"],
                depends_on_by_node=depends_on_by_node,
                nodes_by_id=nodes_by_id,
                issue_by_node=issue_by_node,
            )
            deliver_refs = delivers_refs_for_body(
                node_id=node["id"],
                delivers_to_by_node=delivers_to_by_node,
                nodes_by_id=nodes_by_id,
                issue_by_node=issue_by_node,
            )
            refreshed_issue = upsert_issue(
                apply=apply,
                repo=repo,
                model=model,
                node=node,
                existing_issue=current_issue,
                dependency_refs=dep_refs,
                delivers_refs=deliver_refs,
                desired_labels=managed_label_names(node),
                milestone=milestone,
            )
            issue_by_node[node["id"]] = refreshed_issue

        # Pass 3: ensure issue is in project and set project fields.
        for node in desired_nodes:
            issue = issue_by_node[node["id"]]
            item_id = add_issue_to_project_if_needed(
                apply=apply,
                owner=owner,
                project_number=project_number,
                issue_url=issue.url,
                project_item_by_url=project_item_by_url,
            )
            blocked_by_text = dependencies_text_for_project(
                node_id=node["id"],
                depends_on_by_node=depends_on_by_node,
                nodes_by_id=nodes_by_id,
                issue_by_node=issue_by_node,
            )
            apply_project_fields(
                apply=apply,
                project_id=project_id,
                fields=fields,
                item_id=item_id,
                model=model,
                node=node,
                blocked_by_text=blocked_by_text,
                blocked_by_field_name=blocked_by_field_name,
            )
            if not item_id.startswith("dry-run:"):
                processed_project_item_ids.add(item_id)

    else:
        for node in desired_nodes:
            existing_item = None
            for candidate in managed_items_by_node_id.get(node["id"], []):
                content_type = (candidate.get("content") or {}).get("type")
                if content_type == "DraftIssue":
                    existing_item = candidate
                    break
            item_id = upsert_draft_item(
                apply=apply,
                owner=owner,
                project_number=project_number,
                model=model,
                node=node,
                existing_item=existing_item,
            )
            apply_project_fields(
                apply=apply,
                project_id=project_id,
                fields=fields,
                item_id=item_id,
                model=model,
                node=node,
                blocked_by_text=None,
                blocked_by_field_name=blocked_by_field_name,
            )
            if not item_id.startswith("dry-run:"):
                processed_project_item_ids.add(item_id)

    stale_items: list[tuple[str, str | None]] = []
    for node_id, node_items in managed_items_by_node_id.items():
        for item in node_items:
            item_id = item["id"]
            item_title = item.get("title") or item.get("content", {}).get("title") or ""
            is_out_of_scope = node_id not in desired_ids
            is_duplicate = item_id not in processed_project_item_ids and node_id in desired_ids and mode == "issue"
            if is_out_of_scope or is_duplicate:
                stale_items.append((item_id, node_id))
            elif archive_stale and node_id in desired_ids and mode == "draft":
                # Draft mode does not dedupe issue-backed items.
                _ = item_title

    if stale_items:
        print(f"Stale managed items: {len(stale_items)}")
    for item_id, node_id in stale_items:
        if archive_stale:
            if not apply:
                print(f"DRY-RUN: archive stale item {item_id} ({node_id})")
            else:
                run_gh(
                    [
                        "project",
                        "item-archive",
                        str(project_number),
                        "--owner",
                        owner,
                        "--id",
                        item_id,
                    ]
                )
                print(f"Archived stale item: {item_id} ({node_id})")
        else:
            print(f"Leave stale item untouched: {item_id} ({node_id})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync semantic roadmap to GitHub Project.")
    parser.add_argument("--owner", default="BioregionalKnowledgeCommons")
    parser.add_argument("--project", type=int, default=1)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--repo", default=DEFAULT_REPO, help="Repository for issue-backed sync mode.")
    parser.add_argument(
        "--mode",
        choices=["draft", "issue"],
        default=DEFAULT_MODE,
        help="Sync mode: draft items or issue-backed project items.",
    )
    parser.add_argument(
        "--kinds",
        default="initiative,work_item,milestone",
        help="Comma-separated node kinds to sync.",
    )
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run).")
    parser.add_argument(
        "--archive-stale",
        action="store_true",
        help="Archive previously managed items no longer present in desired set.",
    )
    parser.add_argument(
        "--ensure-fields",
        action="store_true",
        help=f"Create optional project field '{BLOCKED_BY_FIELD_NAME}' if missing.",
    )
    parser.add_argument(
        "--blocked-by-field",
        default=BLOCKED_BY_FIELD_NAME,
        help="Project text field name for unresolved dependency projection.",
    )
    args = parser.parse_args()

    kinds = {k.strip() for k in args.kinds.split(",") if k.strip()}
    if not kinds:
        kinds = set(DEFAULT_KINDS)

    try:
        sync(
            owner=args.owner,
            project_number=args.project,
            model_path=args.model,
            apply=args.apply,
            archive_stale=args.archive_stale,
            kinds=kinds,
            mode=args.mode,
            repo=args.repo,
            ensure_fields=args.ensure_fields,
            blocked_by_field_name=args.blocked_by_field,
        )
    except SyncError as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
