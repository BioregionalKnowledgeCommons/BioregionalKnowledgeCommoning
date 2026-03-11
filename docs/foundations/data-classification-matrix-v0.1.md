# Data Classification Matrix v0.1

**Status:** v0.1
**Date:** 2026-03-11 (updated from Draft 2026-03-10)
**Depends on:** S0 Federation Membrane Governance (deployed), Migration 062 (visibility_scope)

## Purpose

This document defines the data classification policy for the Bioregional Knowledge Commons. Every entity type, predicate, and ingest path has an associated classification that determines visibility, federation behavior, and consent requirements.

Classification must exist **before** new ingest paths open. This is a core value proposition of the BKC: consent-aware data governance is not an afterthought.

## Classification Tiers

| Tier | Label | Visibility | Federation | Example |
|------|-------|-----------|------------|---------|
| T1 | **Public** | All endpoints, search, chat, federation | Broadcast to all approved edges | Published practices, patterns, public organizations |
| T2 | **Restricted** | Authenticated endpoints only | Federation with consent flag | Community meeting notes, unpublished research |
| T3 | **Community Only** | Node-local, authenticated | Never federated | Interview transcripts, personal reflections, draft artifacts |
| T4 | **Node Private** | Node-local, admin only | Never federated | Raw audio, PII, consent-restricted data |

### Implementation Mapping

| Tier | `visibility_scope` (entity_rid_mappings) | `node_private` (entity_registry) | Federation eligible |
|------|------------------------------------------|----------------------------------|-------------------|
| T1 Public | `public` | `false` | Yes |
| T2 Restricted | `public` (+ access control layer) | `false` | Yes (with consent flag) |
| T3 Community Only | `node_private` | `true` (when all mappings are node_private) | No |
| T4 Node Private | `node_private` | `true` | No |

**Note:** T2 (Restricted) is not yet fully enforced — the access control layer for authenticated-only visibility is designed but not implemented. For now, T2 entities are treated as T1 (public) at the API level. This is an accepted gap for the current phase; T2 enforcement is a Horizon 3 item.

## Entity Type Classifications

### Default Classification by Entity Type

| Entity Type | Default Tier | Rationale | Override Allowed |
|-------------|-------------|-----------|-----------------|
| **Person** | T1 Public | Public figures, community members | Yes → T3/T4 for minors, at-risk |
| **Organization** | T1 Public | Generally public entities | Yes → T2 for emerging orgs |
| **Project** | T1 Public | Published projects | Yes → T2 for pre-launch |
| **Location** | T1 Public | Geographic features are public knowledge | Rarely |
| **Bioregion** | T1 Public | Bioregional boundaries are shared commons | No |
| **Concept** | T1 Public | Shared vocabulary | Rarely |
| **Meeting** | T2 Restricted | Contains discussion context | Yes → T3 for sensitive |
| **Practice** | T1 Public | Practices are meant to be shared | Yes → T2 for proprietary |
| **Pattern** | T1 Public | Patterns are distilled knowledge | Yes → T2 for emerging |
| **Protocol** | T1 Public | Protocols are shared agreements | Rarely |
| **CaseStudy** | T1 Public | Published case studies | Yes → T2 for draft |
| **Playbook** | T1 Public | Operational guides | Yes → T2 for internal |
| **Question** | T1 Public | Research questions | Yes → T3 for sensitive |
| **Claim** | T1 Public | Claims are public assertions | Yes → T2 before verification |
| **Evidence** | T2 Restricted | May contain sensitive source data | Yes → T3/T4 |
| **Commitment** | T2 Restricted | Financial/resource commitments | Yes → T1 after activation |
| **CommitmentPool** | T1 Public | Pool structure is public | Rarely |
| **CommitmentAction** | T2 Restricted | Individual actions may be sensitive | Yes → T1 after completion |
| **Outcome** | T1 Public | Roadmap outcomes are public | No |
| **Initiative** | T1 Public | Roadmap initiatives | No |
| **WorkItem** | T2 Restricted | Internal work tracking | Yes → T1 for milestones |
| **Milestone** | T1 Public | Public checkpoints | Rarely |
| **Decision** | T2 Restricted | Governance decisions | Yes → T1 after ratification |
| **Risk** | T3 Community Only | Risk assessments are sensitive | Yes → T2 for published |
| **Metric** | T1 Public | Measurement definitions | Rarely |

### Special Cases

**Interview Artifacts** (from interview-commoning plugin):
- **PracticePacket**: T2 Restricted (until reviewed and published → T1)
- **PatternCandidatePacket**: T2 Restricted (until reviewed → T1)
- **ProtocolCandidatePacket**: T2 Restricted (until reviewed → T1)
- **Raw transcript**: T4 Node Private (always — contains unredacted speech)
- **Redacted transcript**: T3 Community Only (reviewed but not for external)

**Transformed Evidence** (from steel thread):
- Evidence entities created from published artifacts: inherit the **most restrictive** tier of their source artifacts
- Evidence entities from external sources: T2 Restricted by default

## Predicate Classifications

| Predicate | Classification | Notes |
|-----------|---------------|-------|
| `affiliated_with` | T1 | Public organizational relationships |
| `attended` | T2 | Meeting attendance may be sensitive |
| `collaborates_with` | T1 | Public collaboration |
| `knows` | T2 | Personal relationships |
| `located_in` | T1 | Geographic containment |
| `broader` / `narrower` | T1 | Taxonomic hierarchy |
| `related_to` | T1 | General association |
| `supports` / `opposes` | T1 | Discourse relationships |
| `evidences_claim` | T1 | Evidence-claim linkage is public |
| `attests_claim` | T1 | Attestation is a public act |
| `makes_claim` | T1 | Claiming is a public act |
| `pledges_commitment` | T2 | Commitment details may be restricted |
| `aggregates_commitments` | T1 | Pool aggregation is public |
| `practiced_in` | T1 | Practice-place association |

## Ingest Path Classification Requirements

Every ingest path MUST specify the classification tier for entities it creates. The adapter is responsible for applying the correct `visibility_scope` parameter.

### Current Ingest Paths

| Path | Endpoint | Default Tier | Classification Source |
|------|----------|-------------|---------------------|
| Vault/MCP | `/register-entity` | T1 Public | `visibility_scope` param |
| Document ingest | `/ingest` | T1 Public | Implicit (source trust) |
| Web content | `/commons/ingest` | T1 Public | Quality gates + steward review |
| Interview plugin | `/ingest` | T2 Restricted | `deriveVisibilityScope()` in plugin |

### Planned Ingest Paths (Horizon 2-3)

| Path | Endpoint | Default Tier | Classification Source |
|------|----------|-------------|---------------------|
| Commons Engine | `/ingest` (via adapter) | T2 Restricted | Mapping intake contract `rights_and_consent.consent_tier` |
| Silvi SDK | `/ingest` (via adapter) | T1 Public | MRV data is public by nature |
| Watershed data | `/ingest` (via adapter) | T1 Public | Public environmental data |
| TBFF receipts | `/register-entity` | T2 Restricted | Financial data, restricted until verified |

### Adapter Requirements

Every new ingest adapter MUST:

1. **Declare default tier** in adapter configuration
2. **Map source consent fields** to BKC `visibility_scope` values
3. **Validate before write**: check that the declared tier matches the entity type's allowed override range
4. **Log classification decisions**: include `classification_tier` and `classification_source` in ingest receipt metadata

## Consent Leakage Prevention

### Verified Query Sites (from Migration 062)

**Reconciled 2026-03-11:** Exhaustive grep across all API files found **34 `WHERE NOT node_private` query sites across 15 public endpoints.** The original count of "24 across 13" undercounted: `/chat` contains 8+ separate queries (semantic search, keyword fallbacks, GraphRAG, graph traversal), `/web/ingest` contains 5 sub-queries for entity matching, and `/web/evaluate` + `/web/process` in `web_router.py` were not originally counted. Additionally, pre-check queries (SELECT node_private before rejecting) were not counted in the original tally.

**By endpoint (15 total):**

| # | Endpoint | File | Query Sites | Notes |
|---|----------|------|-------------|-------|
| 1 | `/entity-search` | personal_ingest_api.py | 2 | With/without type filter |
| 2 | `/entity/{uri}` | personal_ingest_api.py | 1 | Single entity detail |
| 3 | `/entity/resolve` (GET+POST) | personal_ingest_api.py | 2 | Pre-check node_private flag |
| 4 | `/entity/{uri}/mentioned-in` | personal_ingest_api.py | 1 | Rejects node_private entities |
| 5 | `/entities/mentioned-in` | personal_ingest_api.py | 1 | Batch filter |
| 6 | `/entity/{uri}/evidence` | personal_ingest_api.py | 1 | Rejects private entities early |
| 7 | `/relationships/{uri}` | personal_ingest_api.py | 3 | Entry check + 2 neighbor filters |
| 8 | `/stats` | personal_ingest_api.py | 3 | Total count + by-type + recent |
| 9 | `/graph-version` | personal_ingest_api.py | 1 | Entity count for hash |
| 10 | `/vault-entities` + `/vault-entity/{rid}` | personal_ingest_api.py | 3 | visibility_scope filter |
| 11 | `/web/ingest` | personal_ingest_api.py | 5 | Project/person/topic/generic/vault matching |
| 12 | `/chat` | personal_ingest_api.py | 8 | Semantic (×2) + keyword fallback (×3) + GraphRAG + graph traversal (×2) |
| 13 | `/web/evaluate` | web_router.py | 1 | Entity context for LLM |
| 14 | `/web/process` | web_router.py | 1 | Entity context for LLM |
| 15 | `/relationship-stats` | personal_ingest_api.py | 0 | Accepted residual: aggregate counts only |
| | **Total** | | **33 active + 1 residual** | |

### Accepted Residuals

- `/relationship-stats`: Returns aggregate counts only — no entity text/URIs leaked
- `koi_memory_chunks`: Interview artifacts don't enter this table; chat retrieval doesn't access node_private entities

### Verification Protocol

Before any new ingest path goes live:

1. Run consent leakage test: create a T4 (node_private) entity via the new path
2. Verify it does NOT appear in any of the 13 public endpoints above
3. Verify it does NOT appear in federation broadcasts
4. Document the test in the ingest path's adapter README

## Federation Classification Rules

Entities are eligible for federation broadcast only if:
1. `node_private = false` in entity_registry
2. Entity has a `koi_rid` assigned (federation identifier)
3. The target edge's `rid_types` includes the entity's type

Federation membrane (S0) provides additional gating:
- Unknown nodes must complete handshake before receiving any data
- Edge-approval gating: only approved edges receive broadcasts
- Admin can reject edges, preventing all data flow to a node

## Scope Note

**v0.1 acceptance criteria:** This document defines classification policy (entity types → tiers) and verifies consent leakage prevention (node_private entities invisible on all public endpoints). It does NOT implement T2 (Restricted) access control — T2 entities are currently treated as T1 (public) at the API level. T2 enforcement (authenticated-only visibility) is deferred to Horizon 3 (1C+). This is an accepted gap for trusted-node deployments.

## Versioning

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-03-11 | Query site count reconciled (34 across 15 endpoints). Consent leakage smoke test passed. Scope note added. Promoted from Draft. |
| 0.1-draft | 2026-03-10 | Initial classification matrix |

## Open Questions

1. **T2 enforcement timeline**: When do we implement authenticated-only visibility for T2 entities? Current treatment as T1 is acceptable for trusted-node deployments but not for public-facing APIs.
2. **Cross-node classification conflicts**: If Node A classifies an entity as T1 and Node B classifies it as T3, which wins in federation? Proposal: most restrictive wins (T3), but this needs governance discussion.
3. **Classification inheritance for derived entities**: When a Pattern is distilled from multiple Practices with different tiers, what tier does the Pattern get? Proposal: most restrictive source tier, with override allowed by reviewer.
