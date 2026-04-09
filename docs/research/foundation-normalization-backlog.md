---
doc_id: bkc.foundation-normalization-backlog
doc_kind: research
status: active
date: 2026-04-08
depends_on:
  - bkc.project-vision
---

# Foundation Normalization Backlog

Audit of BKC foundation docs lacking governed YAML frontmatter, produced during the bounded-context refresh (2026-04-08). This backlog is deferred work — not part of the current refresh pass.

## Foundation docs missing all frontmatter

These docs have no YAML frontmatter block. They need `doc_id`, `doc_kind`, `status`, and `depends_on` added.

| File | Suggested doc_id | Suggested doc_kind | Notes |
|:-----|:----------------|:-------------------|:------|
| `ontology-commoning-framework.md` | `bkc.ontology-commoning-framework` | foundations | Mapping lifecycle + governance |
| `ontology-commoning-ops-v0.1.md` | `bkc.ontology-commoning-ops` | operations | Operational workflow for mapping proposals |
| `koi-federation-operations-runbook.md` | `bkc.koi-federation-ops-runbook` | operations | Peering, bootstrap, troubleshooting |
| `commonschange-reference-profile-v0.1.md` | `bkc.commonschange-reference-profile` | spec | Event/snapshot exchange profile |
| `node-participation-profiles.md` | `bkc.node-participation-profiles` | foundations | Non-KOI, KOI full, KOI gateway |
| `bioregion-onboarding-playbook.md` | `bkc.bioregion-onboarding-playbook` | guidance | 30/60/90 day onboarding tracks |
| `bioregional-mapping-model-v0.1.md` | `bkc.bioregional-mapping-model` | spec | Graph-first profile over ontology |
| `bioregional-mapping-intake-contract-v0.1.md` | `bkc.bioregional-mapping-intake-contract` | spec | Docs-level canonical packet |
| `interview-to-graph-mvp-v0.1.md` | `bkc.interview-to-graph-mvp` | spec | Operator-first interview pipeline |
| `rights-licensing-consent-policy-slots.md` | `bkc.rights-licensing-consent-policy-slots` | foundations | Required policy metadata slots |
| `transcription-and-processing-pipeline.md` | `bkc.transcription-pipeline` | operations | Consent-aware interview workflow |

## Foundation docs with partial metadata

| File | Issue | Notes |
|:-----|:------|:------|
| `data-classification-matrix-v0.1.md` | Status/date in body, not frontmatter | Needs proper frontmatter extraction |
| `flow-funding-foundations.md` | "Draft v0.1" in body, not frontmatter | Needs proper frontmatter extraction |

## Docs outside foundations/ missing frontmatter

| File | Suggested doc_id | Notes |
|:-----|:----------------|:------|
| `bioregional-swarm-telos.md` | `bkc.bioregional-swarm-telos` | External-facing positioning doc |
| `bioregional-ai-swarms-positioning.md` | `bkc.bioregional-ai-swarms-positioning` | External-facing one-pager |

## Files that should remain ungoverned

- `README.md` — repo entry point, not a governed doc
- `docs/foundations/README.md` — index file
- `docs/roadmap/README.md` — index file
- All `CLAUDE.md` files — operator context, not canon

## doc_kind taxonomy observation

Current values in use: `vision`, `architecture`, `spec`, `foundation`, `foundations`, `synthesis`, `research`, `operations`, `guidance`. The singular/plural inconsistency (`foundation` vs `foundations`) should be normalized when frontmatter is added.

Suggested taxonomy: `vision`, `architecture`, `spec`, `foundations`, `synthesis`, `research`, `operations`, `guidance`, `positioning`.
