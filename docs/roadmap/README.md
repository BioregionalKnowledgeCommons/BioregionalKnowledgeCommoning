# Semantic Roadmap

This folder defines the roadmap-of-record in two forms:

1. Machine-readable canonical graph (`semantic-roadmap.json`)
2. Generated human-readable view (`ROADMAP.md`)

## Why this structure

- Human planning stays readable and reviewable in Markdown.
- Automation can safely reason over dependencies, status, and risk via a typed graph.
- Decisions and changes remain auditable in Git.

## Files

- `semantic-roadmap.json`: canonical roadmap graph (source of truth)
- `semantic-roadmap.schema.json`: JSON Schema for structural validation
- `semantic-roadmap.context.json`: JSON-LD context for semantic interoperability
- `ROADMAP.md`: generated projection for humans (do not edit manually)

## Graph model

### Node kinds

- `outcome`
- `initiative`
- `work_item`
- `decision`
- `risk`
- `milestone`
- `metric`

### Edge types

- `depends_on`: `from` must complete before `to`
- `delivers`
- `mitigates`
- `informs`
- `blocks`
- `references`
- `measures`

## Build and validate

From `BioregionalKnowledgeCommoning/`:

```bash
python3 scripts/build_semantic_roadmap.py --check
python3 scripts/build_semantic_roadmap.py
```

## GitHub Project sync

Sync selected roadmap node kinds into a GitHub Project.

### Modes

- `--mode draft` (legacy): manages Project draft items only.
- `--mode issue` (recommended): manages real GitHub issues and maps:
  - Project fields: `Status`, `Priority`, `Start date`, `Target date`
  - Optional dependency field: `Blocked by` (text)
  - Repo metadata: labels (`kind:*`, `horizon:*`, `tag:*`, `status:*`) and milestones

### Recommended commands (issue-backed)

Dry-run:

```bash
python3 scripts/sync_roadmap_to_github_project.py \
  --owner BioregionalKnowledgeCommons \
  --project 1 \
  --repo BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning \
  --mode issue \
  --ensure-fields
```

Apply:

```bash
python3 -u scripts/sync_roadmap_to_github_project.py \
  --owner BioregionalKnowledgeCommons \
  --project 1 \
  --repo BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning \
  --mode issue \
  --ensure-fields \
  --archive-stale \
  --apply
```

### Legacy command (draft mode)

```bash
python3 scripts/sync_roadmap_to_github_project.py \
  --owner BioregionalKnowledgeCommons \
  --project 1 \
  --mode draft \
  --apply
```

### Useful options

- `--kinds initiative,work_item,milestone` (default)
- `--archive-stale`: archive managed project items no longer in scope (or old `SR:` duplicates during issue-mode migration)
- `--blocked-by-field "Blocked by"`: custom project field name for unresolved dependencies projection

## Update workflow

1. Edit `semantic-roadmap.json`.
2. Run `--check` and fix validation errors.
3. Regenerate `ROADMAP.md`.
4. Commit both changed files.

## Evidence discipline

Every roadmap node should link to supporting docs in `source_docs`.  
Use decision logs for material shifts in architecture or governance direction.
