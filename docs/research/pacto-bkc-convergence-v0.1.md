# PACTO–BKC Convergence Document v0.1

**Status:** Draft — for comment on [regen-network/pacto-framework#6](https://github.com/regen-network/pacto-framework/issues/6)
**Date:** 2026-03-10
**Author:** Darren Zal
**Framing:** BKC as adjacent precedent and concrete convergence substrate

## Context

This document responds to Greg Landua's [PACTO framework issue #6](https://github.com/regen-network/pacto-framework/issues/6), which proposes using BKC/Octo's interview-to-graph work as reference implementation input for the PACTO agentic implementation blueprint.

Greg's issue identifies five implementation gaps in the current PACTO framework and asks how existing systems like BKC can inform the formalization. This document maps BKC's current infrastructure to each gap honestly — distinguishing what is **implemented and live**, what is **designed but not yet deployed**, and what is **not yet addressed**.

BKC is not "the" reference implementation for PACTO. It is an adjacent precedent — a working system that has encountered many of the same challenges PACTO aims to solve and has made concrete engineering choices that may inform PACTO's design.

## Infrastructure Summary

**Live (as of March 10, 2026):**
- 4 federated KOI nodes (Octo/Salish Sea, Front Range, Greater Victoria, Cowichan Valley)
- ~1,005 entities across 25 types, connected by 39 predicate types
- Claims Engine V1: 49 claims, BLAKE2b-256 content hashing, MsgAnchor to Regen testnet
- Federation membrane governance (S0): edge-approval gating, ECDSA-signed envelopes
- Interview-commoning plugin: 8 tools, consent-aware extraction, 3 artifact types
- Knowledge ingest pipeline: URL→entity extraction, web content curation, steward review
- Visibility scope enforcement: 24 query sites filtered for node_private entities

**Designed (ready for implementation):**
- Claims Engine V2: four-role attestation model, policy gates, MsgAttest on-chain
- Data classification matrix (v0.1): entity-type-level consent/publication policy
- PACTO workflow object schemas (proposed in this document)

**Not yet addressed:**
- DAO DAO integration beyond role mapping
- Cross-node mapping consensus protocol
- T2 (restricted) access control enforcement

---

## Gap-by-Gap Mapping

### Gap 1: Workflow Objects Lack Formal Machine-Readability

**Greg's concern:** Current implementations describe workflow stages conceptually but don't provide explicit machine-readable contracts for agents to operate on.

#### What BKC has implemented

**Interview-commoning plugin** (live, 8 tools): The `session_finalize` tool produces three formal artifact types from interview sessions:

| Artifact Type | Fields | Machine-Readable | In Production |
|--------------|--------|-------------------|---------------|
| **PracticePacket** | name, description, context, bioregion, source_interview, confidence | JSON with typed fields | Yes |
| **PatternCandidatePacket** | name, description, instances, conditions, context | JSON with typed fields | Yes |
| **ProtocolCandidatePacket** | name, description, steps, governance_context, participants | JSON with typed fields | Yes |

These are machine-readable in the sense that agents (OpenClaw tools) produce and consume them via structured JSON. However, they are **not yet PACTO-compatible schemas** — they use BKC's internal type system, not PACTO's proposed workflow object contracts.

**Mapping intake contract** (v0.1, designed): Defines a richer canonical packet shape that includes consent fields:

```json
{
  "document_rid": "stable-id",
  "mapping_context": "who_is_here | what_is_happening | ...",
  "rights_and_consent": {
    "consent_tier": "public | restricted | community_only | private",
    "share_scope": "local | bioregion | cross_bioregion",
    "allowed_uses": ["..."],
    "reviewer": "Name"
  },
  "entities": [...],
  "relationships": [...]
}
```

This contract is designed but the adapter layer to translate external sources into this shape is not yet built.

**Interview-to-graph MVP** (v0.1, designed): Describes a 7-stage pipeline (Intake → Transcript → QA/Redaction → Extraction → Ontology Review → Governed Ingest → Publication) with explicit gates at stages A, C, E, and G. The broader design includes additional artifact types beyond what the live plugin currently produces:
- Question, Claim, Evidence, Decision, NextAction (designed, not in live plugin)

#### Convergence path

BKC's existing artifact types can serve as **concrete examples** for PACTO's workflow object formalization:

| PACTO Proposed Object | BKC Equivalent | Status |
|----------------------|----------------|--------|
| AssemblyIntakeRecord | Interview intake (Stage A metadata) | Designed (interview-to-graph-mvp) |
| ReviewedTranscript | QA'd transcript (Stage C output) | Designed |
| ExtractionBundle | PracticePacket + PatternCandidate + ProtocolCandidate | **Live** |
| MappingReviewPacket | Ontology review output (Stage E) | Designed |
| GovernedIngestPayload | `/ingest` request body | **Live** |
| EndorsementRecord | ClaimAttestation (V2 Phase 1) | **Live** (CRUD deployed) |

**Proposed next step:** Define PACTO-compatible JSON schemas for these objects, filed as a PR to `pacto-framework` in `core/workflows/`. BKC would then build thin adapters between its internal types and PACTO schemas, enabling cross-project interoperability without forcing either system to adopt the other's type system.

---

### Gap 2: Governance and Legitimacy Are Under-Formalized

**Greg's concern:** Reference implementations emphasize data pipelines over participatory authority. PACTO requires explicit mechanisms for who validates meaning, who approves mappings, who records disagreements.

#### What BKC has implemented

**Federation membrane governance (S0)** — live, deployed to all nodes:
- Edge-approval gating: nodes must be explicitly approved before receiving any federated data
- Unknown handshake deferral: new nodes are held in a pending state until an admin approves
- Edge rejection: `POST /edges/reject` permanently blocks a node
- Admin CLI: `admin-edges.sh` for real-time edge management

This addresses **data flow governance** (who can see what) but not **meaning governance** (who validates that a Pattern is correctly extracted from an interview).

**Claims attestation layer (V2 Phase 1)** — live:
- `POST /claims/{rid}/attestations`: Identity-bound attestation with verdict (approved/rejected/needs_info), rationale, and evidence references
- Non-self-attestation guard: claimant cannot attest to their own claim
- Stable RID: same reviewer + claim always produces the same attestation record (UPSERT safe)

This provides a **formal record of who reviewed what and what they decided**, which directly addresses PACTO's concern about generating "durable community endorsement evidence."

**Visibility scope system** — live:
- 4-tier classification (public, restricted, community_only, node_private)
- `deriveVisibilityScope()` in the interview plugin applies consent during review
- 24 query sites enforce node_private filtering

#### What's designed but not deployed

**Attestation policy gates (V2 Phase 2)**: Hard preconditions on state transitions:
- `peer_reviewed` requires ≥1 approved attestation from non-claimant
- `verified` requires ≥2 approved attestations
- Grandfathering for pre-V2 claims

**CommonsChange reference profile**: Defines a serialization format with explicit attestation fields:
```yaml
attestations:
  - actor_id: string
    actor_role: author | contributor | reviewer | system
    attested_at: datetime
    evidence_ref: string
```

#### What's not addressed

- **DAO DAO role mapping**: BKC has a `reviewer_uri` FK (extensible to on-chain addresses) but no integration with DAO DAO proposal/approval workflows
- **Ontology disagreement recording**: The interview-to-graph MVP design includes a `mapping_status` field (equivalent, narrower, broader, related, unmapped, proposed_extension) but this is not yet formalized as a governance record
- **Cross-node meaning consensus**: No protocol for resolving conflicting entity interpretations between nodes

#### Convergence path

BKC's attestation layer provides a concrete mechanism that PACTO's governance formalization can build on. The key insight: **attestations are governance artifacts, not just verification checkboxes**. Each attestation records who reviewed, what they concluded, why, and what evidence they examined.

Proposed minimal seam: DAO DAO roles → BKC steward roles. The `reviewer_uri` FK in `claim_attestations` is already extensible to on-chain addresses (regen1...). When DAO DAO integration lands, this FK becomes the bridge — a reviewer's on-chain role in a SubDAO determines their authority to attest within the BKC system.

---

### Gap 3: Evidence-Trail Architecture Needs Strengthening

**Greg's concern:** Provenance intuitions exist but PACTO requires a rigorous formal model spanning source capture → transcription → synthesis → review → correction → endorsement → agreement → publication.

#### What BKC has implemented

**Claims Engine V1 lifecycle** — live (49 claims):

```
self_reported → peer_reviewed → verified → ledger_anchored
                                              ↕ withdrawn
```

Each state transition is recorded in an **append-only `claim_state_log`**:
- `from_state`, `to_state`, `actor`, `reason`, `metadata`, `created_at`
- No deletions, no updates — insert-only audit trail
- Evidence linking is logged: `POST /claims/{rid}/evidence` records the URI in metadata

**Proof pack** (new, as of this document): A synthesized verification artifact assembled from:
- `GET /claims/{rid}` — claim data + linked evidence entities
- `GET /claims/{rid}/history` — full claim_state_log entries
- Anchor fields: `content_hash` (BLAKE2b-256), `ledger_iri`, `tx_hash`, `ledger_timestamp`
- Attestation records: reviewer verdicts with rationale

One proof pack per anchored claim — archivable, verifiable, self-contained.

**Content-addressable RIDs**: Claims, attestations, and entities all use deterministic RID generation from content hashing. Same content always produces the same identifier.

#### The convergence

PACTO's evidence trail ≈ BKC's claim lifecycle + attestation records + on-chain anchoring.

| PACTO Evidence Trail Stage | BKC Equivalent | Status |
|---------------------------|----------------|--------|
| Source capture | Interview intake / document ingest | **Live** |
| Transcription | MacWhisper / Otter integration | **Live** |
| AI synthesis | `session_finalize` extraction | **Live** |
| Community feedback | Attestation verdicts (approved/rejected/needs_info) | **Live** |
| Refinement | Claim versioning (`supersedes_rid`) | **Live** |
| Formal agreement | `ledger_anchored` state + proof pack | **Live** |
| On-chain publication | MsgAnchor broadcast (testnet) | **Live** |

The claim_state_log provides the kind of rigorous, append-only provenance chain PACTO describes. Each transition records provenance sufficient to reconstruct the full decision path from initial assertion to on-chain anchoring.

---

### Gap 4: Regen Ledger Integration Remains Implicit

**Greg's concern:** No explicit articulation of content hashing pathways, IRI generation, data module anchoring procedures, attestation flows, or linking workflow artifacts to on-chain references.

#### What BKC has implemented — explicitly

**Content hashing** (live):
- Algorithm: BLAKE2b-256 (32-byte digest)
- Input: Canonical JSON of claim fields (sorted keys, deterministic serialization)
- Fields included: `claim_rid`, `entity_uri`, `claimant_uri`, `statement`, `claim_type`, `verification`, `metadata`
- Output: hex-encoded hash → `claims.content_hash`

**IRI derivation** (live):
- Tool: `regen q data convert-hash-to-iri` CLI
- Input: BLAKE2b-256 hash (base64-encoded) with `digest_algorithm: DIGEST_ALGORITHM_BLAKE2B_256`, `file_extension: json`
- Output: `regen:113...` IRI stored as `claims.ledger_iri`

**MsgAnchor broadcast** (live, testnet):
- Command: `regen tx data anchor <iri>` via CLI
- Chain: `regen-upgrade` (testnet)
- Confirmation: 6 attempts × 5s polling, then reconcile endpoint for timeouts
- Fields persisted: `tx_hash`, `ledger_iri`, `ledger_timestamp`

**Verification** (live):
- On-chain query: `GET /regen/data/v2/anchor-by-iri/{iri}` via REST API
- Reconcile endpoint: `POST /claims/{rid}/reconcile` checks tx status and finalizes state

**Honest note:** This is testnet anchoring. The `claims-service` key uses `keyring-backend test`. Mainnet deployment requires funded accounts and production key management. The anchoring proves the integration path works end-to-end, but it is not production-grade.

#### What's designed (V2)

**MsgAttest** (Phase 3, designed): On-chain attestation using `ContentHash.Graph` instead of `ContentHash.Raw`. Each attestation would:
1. Serialize to canonical JSON-LD
2. Hash with BLAKE2b-256
3. Broadcast `MsgAttest` with `attestor_address` (regen1...)
4. Record `attest_tx_hash`, `graph_iri`, `attest_timestamp`

**Per-reviewer key delegation** (designed): `cosmos.authz` for delegating attestation authority from a DAO to individual reviewers.

#### Convergence path

BKC's implementation provides the **most concrete Regen Ledger integration** of any project in this space. The content hashing → IRI derivation → MsgAnchor → verification flow is fully operational. PACTO's blueprint can reference this as a working example of the anchoring pipeline, with clear extension points for MsgAttest and ContentHash.Graph.

---

### Gap 5: DAO DAO Governance Integration Is Missing

**Greg's concern:** PACTO should formalize review roles, proposal workflows, endorsement mechanisms, SubDAO handling, and publication approval chains.

#### What BKC has — honestly, the least

**Steward roles** (live, minimal):
- `commons_memberships` table: per-node steward authorization
- WebAuthn passkey authentication: stewards identified by passkey, not on-chain address
- Protected routes: `/commons/decide`, `/commons/resolve-merges` require steward auth

**Reviewer identity** (V2 Phase 1, live):
- `reviewer_uri` FK in `claim_attestations`: links reviewer to entity_registry
- This is a database-level identity, not an on-chain identity

#### What's designed

**Role mapping** (conceptual):
- DAO DAO roles → BKC steward roles
- `reviewer_uri` extensible to on-chain addresses (regen1...)
- `attestor_address` field in V2 Phase 3 designed for this purpose

#### What's not addressed

- DAO DAO proposal workflows for ontology decisions
- SubDAO structure for bioregional governance
- On-chain publication approval chains
- Cross-DAO authorization for inter-bioregion attestation

#### Honest assessment

This is the weakest convergence point. BKC has identity infrastructure (entity_registry, steward auth, reviewer URIs) that could bridge to DAO DAO, but the integration is not designed in detail. The `reviewer_uri → attestor_address` path is the most concrete seam, and it only works because BKC's attestation model was designed with on-chain identity as a future extension.

**Proposed minimal seam:** Rather than designing a full DAO DAO integration, define a narrow interface:
1. DAO DAO publishes a list of authorized reviewers (regen1... addresses + roles)
2. BKC maps these to `reviewer_uri` entries in entity_registry
3. Attestation policy gates reference DAO DAO roles (e.g., "verified requires ≥1 approved attestation from a reviewer with DAO DAO 'senior-reviewer' role")

This is achievable without deep DAO DAO integration and preserves BKC's database-level governance while adding on-chain authorization.

---

## Summary: What's Real vs. What's Designed

| Component | Status | Confidence |
|-----------|--------|-----------|
| 4-node KOI federation | **Live** | High — deployed, tested, membrane governance operational |
| Interview extraction (3 artifact types) | **Live** | High — used in practice |
| Claims lifecycle (49 claims) | **Live** | High — V1 complete, V2 Phase 1 deployed |
| Testnet anchoring (MsgAnchor) | **Live** | Medium — testnet only, not mainnet |
| Attestation CRUD | **Live** | High — UPSERT safe, non-self-attestation guard |
| Visibility scope enforcement | **Live** | High — 24 query sites filtered |
| Attestation policy gates | **Designed** | High — spec complete, implementation straightforward |
| MsgAttest on-chain | **Designed** | Medium — depends on regen-ledger data module stability |
| DAO DAO integration | **Conceptual** | Low — narrow seam identified, no detailed design |
| Cross-node meaning consensus | **Not addressed** | N/A |

## Proposed Next Steps

1. **Workflow object schemas** — Define PACTO-compatible JSON schemas for the 6 workflow objects (AssemblyIntakeRecord through EndorsementRecord). File as PR to `pacto-framework` in `core/workflows/`. Contingent on Greg's response to this document.

2. **Evidence trail alignment** — Map BKC's claim_state_log entries to PACTO's evidence trail stages. Identify where BKC's log is richer (attestation metadata) and where PACTO's model adds stages BKC hasn't formalized (community assembly, feedback cycles).

3. **Minimal DAO DAO seam** — Define the reviewer-role interface between DAO DAO and BKC's attestation layer. Start with a simple JSON mapping file, not a full integration.

4. **Joint testnet demo** — Run PACTO's 6-step loop (assembly → capture → synthesis → feedback → refinement → agreement) through BKC's infrastructure, anchoring the final agreement artifact on Regen testnet. This would prove convergence concretely.

---

## Key Resources

- [BKC interview-to-graph MVP](../foundations/interview-to-graph-mvp-v0.1.md)
- [Bioregional mapping intake contract](../foundations/bioregional-mapping-intake-contract-v0.1.md)
- [CommonsChange reference profile](../foundations/commonschange-reference-profile-v0.1.md)
- [Claims Engine V1](https://github.com/gaiaaiagent/koi-processor/blob/regen-prod/docs/claims-engine-v1.md)
- [Claims Engine V2 Attestations](https://github.com/gaiaaiagent/koi-processor/blob/regen-prod/docs/claims-engine-v2-attestations.md)
- [Federation membrane governance](../foundations/koi-federation-operations-runbook.md)
- [Data classification matrix](../foundations/data-classification-matrix-v0.1.md)
