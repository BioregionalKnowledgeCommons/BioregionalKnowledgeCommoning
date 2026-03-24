# MVIS Pilot Spec — Regenerate Cascadia Intent Registry

## Status: Draft (2026-03-24)

This is the operational contract for the Minimum Viable Intent System (MVIS) pilot in the Regenerate Cascadia bioregion, May–July 2026. It scopes what the pilot builds and defers, defines coordinator workflows, and specifies the technical infrastructure.

For the full architectural vision (4 intent types, 4 agent roles, criteria blocks, bilateral reveal), see [Intent Publication & Agent-Mediated Routing](../../docs/ge-integration/intent-publication.md). This document is the subset we build and test.

---

## 1. Scope & Deferred Features

### In Scope

| Feature | Detail |
|---------|--------|
| Intent types | OFFER, WANT, SWAP |
| Participants | 5–10 landscape groups in Cascadia bioregion |
| Asset vocabulary | Controlled, seeded from mapping workshops |
| Matching | Coordinator-vetted; no automated solvers |
| Intake | Hybrid: transcript extraction + manual scribe, both creating `draft` intents |
| State model | Intent lifecycle + separate match proposal lifecycle |
| Privacy | Three response projections; contact info coordinator-only |
| Infrastructure | PostgreSQL on personal-koi backend; FastAPI router |

### Deferred to Post-Pilot

| Feature | Reason |
|---------|--------|
| CONDITIONAL intents | Learn from real OFFER/WANT/SWAP data first |
| Bilateral reveal | Requires RegenCHOICE question sets not yet designed |
| Criteria / question sets | Facilitation layer only in pilot; structured criteria matching deferred |
| Competitive solvers | Coordinator-vetted matching is sufficient for 5–10 groups |
| On-chain events | No blockchain integration in pilot |
| DIDs / verifiable credentials | Identity is local; coordinator knows participants |
| Automated partial fulfillment | Manual clone by coordinator in v1 |

---

## 2. Hybrid Intake Workflow

The intake process has two distinct layers:

**Facilitation layer (workshops):** Workshops use RegenCHOICE-style question frameworks to surface and refine intents through facilitated discussion. The workshop is relational — no structured data entry happens during the session.

**Data entry layer (afterward):** Structured registry ingestion happens after workshops, from notes, transcripts, or scribe review.

### Intake Pipeline

```
Workshop discussion (facilitated, question-guided)
        │
        ▼
Notes / transcripts / scribe observations
        │
        ├──▶ Transcript extraction (commitment_router.py:345 pattern)
        │         creates draft intents with ai_confidence score
        │
        └──▶ Scribe manual entry
                  creates draft intents with capture_method='manual'
        │
        ▼
Human review (coordinator or scribe)
        │
        ▼
draft → active  ← this is the human-in-the-loop membrane
```

**Key constraint:** Nothing becomes `active` until human review. The `draft → active` transition is the single quality gate.

**Workshop feedback loop:** Each follow-up workshop opens with a Match Report: "4 matched, 2 expired, 4 pending — refresh?" This closes the loop between registry state and participant awareness.

> **Reconciliation note:** Existing docs (commitment-economy-vision.md §2.3) describe question capture in workshops. This spec describes the separate data entry step. The two are complementary: workshops use question frameworks to guide conversation; structured intent capture happens afterward.

---

## 3. Intent State Model

Two separate lifecycles that never mix. Intent status never tracks coordinator workflow.

### Intent Lifecycle (`intent_registry.status`)

```
draft → active → fulfilled
              ↘ stale → archived
              ↘ archived (manual withdraw)
```

| State | Meaning | Entry condition |
|-------|---------|----------------|
| `draft` | Created by extraction or scribe, awaiting review | Default on creation |
| `active` | Reviewed and published to registry | Human promotes from draft |
| `fulfilled` | Match accepted and completed | Coordinator confirms |
| `stale` | Priority decayed below governance-defined floor (e.g., 0.1) | Decay function triggers |
| `archived` | Withdrawn or auto-archived | Manual withdraw, or no response to stale prompt |

### Match Proposal Lifecycle (`intent_match_proposals.status`)

```
candidate → introduced → accepted
                      → declined
                      → expired
```

| State | Meaning |
|-------|---------|
| `candidate` | Algorithm found potential match, awaiting coordinator review |
| `introduced` | Coordinator has introduced the parties |
| `accepted` | Both parties confirmed |
| `declined` | One or both parties declined |
| `expired` | Proposal timed out without coordinator or party action |

These lifecycles are independent. An intent stays `active` while match proposals are worked. An intent is not `fulfilled` until a match is `accepted` and the exchange is confirmed complete.

---

## 4. Priority Decay Model

Intents decay in priority over time unless refreshed. This treats attention as a scarce resource — stale intents should not crowd out fresh ones.

**Formula:**

```
P(t) = P₀ · e^(-λ(t - t_last_refresh))
```

| Parameter | Source | Default |
|-----------|--------|---------|
| P₀ | Initial priority (100.0 at creation or refresh) | 100.0 |
| λ | `landscape_group_config.decay_lambda` | 0.023 (~30-day half-life) |
| t_last_refresh | `intent_registry.last_refreshed_at` | — |

**Decay rates:**

| Rate | Half-life | λ | Use case |
|------|-----------|---|----------|
| `normal` | ~30 days | 0.023 | Standard intents |
| `urgent` | ~7 days | 0.099 | Time-sensitive needs |

**Refresh:** User confirms the intent is still valid. Resets priority to P₀ = 100.0 and updates `last_refreshed_at`.

**Stale threshold:** When `P(t)` drops below the governance-defined floor (default: 0.1), the intent transitions to `stale` and triggers a recovery prompt.

---

## 5. Recovery Semantics

Three failure/degradation modes, each with a defined recovery path:

### Flake (match fails after introduction)

The match proposal moves to `declined`. The intent reverts to `active` with priority reset to P₀ = 100.0. Rationale: the intent is still valid; it was the match that failed.

### Partial Fulfillment

Manual in v1. The coordinator creates a new intent for the unfulfilled remainder, preserving the original intent's timestamp in metadata for audit trail. The original intent is marked `fulfilled`.

Automated cloning is deferred to post-pilot.

### Stagnant (priority below floor)

iffit-style prompt sent to publisher:
1. **Refresh** — confirm intent still valid, reset priority
2. **Modify** — update terms, reset priority
3. **Archive** — intent no longer needed

No response within governance-defined window → auto-archive.

---

## 6. Coordinator Review Flow

Coordinators are the human layer between algorithmic matching and participant introductions.

### Matching Cadence

- **Weekly** batch matching (default), configurable per landscape group
- **On-demand** via API for time-sensitive situations

### Match Proposal Workflow

```
Matching algorithm finds compatible intents
        │
        ▼
Match proposal created (status: candidate)
        │
        ▼
Coordinator reviews candidate
        │
        ├──▶ Introduces parties (status: introduced)
        │         │
        │         ├──▶ Both confirm (status: accepted) → intent fulfilled
        │         ├──▶ One declines (status: declined) → intent stays active
        │         └──▶ No response (status: expired)
        │
        └──▶ Rejects candidate (deleted or expired)
```

### Coordinator Digest

Generated per landscape group, containing:

| Section | Contents |
|---------|----------|
| Local matches | Candidate matches within the landscape group |
| Cross-landscape | Potential matches with other landscape groups (regional visibility) |
| Unmet needs | Active WANT intents with no candidate matches |
| Stale intents | Intents approaching or past decay floor |

The digest is the coordinator's primary operational tool. It uses `IntentCoordinatorResponse` format (includes contact info). Participants never see this view.

---

## 7. Privacy Architecture: Three Projections

Following RegenCHOICE's staged disclosure model: publish categories, not identities. Share match structure, not full records. Reveal contact only after mutual consent.

### Projection Model

| Projection | Contents | Audience | API Response Model |
|------------|----------|----------|--------------------|
| **Discovery** | Asset category, landscape group, intent type, rough availability | Public / regional (per visibility setting) | `IntentDiscoveryResponse` |
| **Match** | Structured answers + requirements for criteria matching | Home node + trusted processors only | *Deferred — no criteria in pilot* |
| **Contact** | Publisher name, contact details, source excerpt, free text | Coordinator only, after match proposal | `IntentCoordinatorResponse` |

### Enforcement

**Pilot deployment:** The personal-koi backend runs on `localhost:8351` (or via WireGuard to NUC). Local-only deployment is the access control. No public API.

**Code-level separation:** Three response models enforce projections at the code level. `IntentDiscoveryResponse` returns categories only — no names, keys, or contact info. `IntentDetailResponse` (internal) adds publisher name, intent key, and process metadata. `IntentCoordinatorResponse` (digest only) adds contact and source excerpt. This prevents accidental data leakage regardless of deployment model.

**If API becomes external:** Add capability/auth gates to `/detail` and `/digest` endpoints. The response model separation means the privacy architecture does not need retrofitting.

### Cross-Node Matching (v2)

Home node sends only discovery/match projections to trusted peers. Remote nodes return opaque candidate IDs, matched answer slices, and missing-question feedback. No names, contacts, or raw transcript excerpts leave the home node. Coordinator proposes introduction only after bilateral correspondence is confirmed.

---

## 8. Controlled Asset Vocabulary

Matching is exact on `asset_key` — no fuzzy matching. This forces vocabulary convergence through workshop governance rather than algorithmic guessing.

### Schema: `intent_asset_vocabulary`

| Column | Type | Description |
|--------|------|-------------|
| `asset_key` | TEXT UNIQUE | Machine key, e.g., `tractor_repair` |
| `display_name` | TEXT | Human label, e.g., "Tractor Repair" |
| `category` | TEXT | Grouping, e.g., `equipment`, `food`, `labor`, `monitoring`, `transport` |
| `landscape_group` | TEXT | NULL = global; otherwise group-specific term |

### Governance

- Seeded from first mapping workshop outputs
- Landscape groups can add group-specific terms
- Vocabulary changes reviewed at coordinator check-ins
- Success metric: < 10% churn after first 2 workshops indicates stabilization

---

## 9. Landscape Group Configuration

Centralized in `landscape_group_config` table — governance parameters and coordinator info in one versioned source, not scattered in code.

### Schema: `landscape_group_config`

| Column | Type | Description |
|--------|------|-------------|
| `group_key` | TEXT UNIQUE | e.g., `olympic_peninsula` |
| `display_name` | TEXT | e.g., "Olympic Peninsula" |
| `decay_lambda` | FLOAT | Priority decay rate (default: 0.023, ~30-day half-life) |
| `coordinator_name` | TEXT | Primary coordinator |
| `coordinator_contact` | TEXT | Email (never exposed via API) |
| `metadata` | JSONB | Extensible fields (matching cadence, stale threshold, etc.) |

---

## 10. Technical Infrastructure

### Backend

- **Database:** PostgreSQL tables on personal-koi backend (`localhost:8351`)
- **API:** FastAPI router (`intent_router.py`)
- **Entity integration:** Intents are first-class KOI graph entities — each intent gets an `entity_registry` row (type: `Intent`) and an `intent_registry` row linked via `entity_uri`
- **State audit:** `intent_state_log` table records all status transitions (insert-only)

### Delivery Slices

| Slice | Scope | Depends on |
|-------|-------|------------|
| **1: Registry** | Schema + entity integration + CRUD / refresh / vocabulary endpoints + tests | — |
| **2: Matching & Digest** | `intent_match_proposals` table + matching algorithm + coordinator digest + privacy-safe responses | Slice 1 |
| **3: Federation** | Domain event handler + cross-node intent propagation | Slice 1 |

### Key Tables

| Table | Purpose |
|-------|---------|
| `intent_registry` | Core intent storage (status, publisher, assets, priority, provenance) |
| `intent_state_log` | Insert-only audit trail of status transitions |
| `intent_match_proposals` | Match proposal lifecycle (Slice 2) |
| `intent_asset_vocabulary` | Controlled asset types |
| `landscape_group_config` | Per-group governance parameters |

---

## 11. Success Criteria

| Criterion | Measurement |
|-----------|-------------|
| At least 3 successful coordinator-introduced matches | Match proposals reaching `accepted` status |
| Asset vocabulary stabilized | < 10% churn in `intent_asset_vocabulary` after first 2 workshops |
| Match report used in at least 1 follow-up workshop | Coordinator confirms report presented at workshop opening |
| Draft → active review workflow tested | At least 1 transcript extraction → draft → human review → active cycle completed |

---

## References

- [Intent Publication & Agent-Mediated Routing](../../docs/ge-integration/intent-publication.md) — Full architectural vision
- [RegenCHOICE](https://wiki.simongrant.org/doku.php/ch:index) — Criteria-based matching, staged disclosure
- Will Ruddick, ["A Physics of Intention"](https://willruddick.substack.com/p/a-physics-of-intention) — Intention as system primitive
- [Commitment Economy Vision](../../docs/ge-integration/commitment-economy-vision.md) — Workshop question capture context (§2.3)
- [CLC Questions Synthesis](../../docs/ge-integration/clc-questions-synthesis.md) — Question framework design
