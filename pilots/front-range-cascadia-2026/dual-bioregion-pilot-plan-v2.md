# Dual Bioregion Pilot Plan v2

## Summary
This version updates v1 to support equal triad governance (Darren, Benjamin, Shawn), KOI-optional participation, and explicit ontology commoning + transcription/mapping integration aligned with the BKC project proposal.

This pilot now explicitly validates a 3-layer architecture:
1. Pattern language (human/commoning)
2. Meta-protocol (thin interop invariants)
3. Reference profile (`CommonsChange`) as one implementation path

## Inputs and Alignment
- OpenCivics PRD note: https://hackmd.io/@QDX_mTmlTSmHf6-gudIFPQ/BJ2r8EtPZe
- Darren response: https://hackmd.io/@DarrenZal/BJRqZjYPbl
- Bioregional Knowledge Commons Summary: https://darrenzal.github.io/Quartz/BioregionalKnowledgeCommonsSummary
- BKC proposal source: https://docs.google.com/document/d/1_6GVoM1D7vmI6q4oqIxkqleo1afVS73LBThbXDBdMME/edit?tab=t.oioon0fguaet

## Scope
### In
- Cross-bioregion exchange of `Practice`, `Pattern`, `CaseStudy`, `Organization`, `Bioregion`.
- Cascadia deployed as live full node.
- Front Range participation without mandatory KOI runtime.
- Dual-canonical operations with field authority map.
- Transport-neutral interoperability using meta-protocol invariants.
- `CommonsChange` reference profile for implementation.
- Event and snapshot publication compatibility.
- Ontology commoning workflow with human-approved mappings.
- Interview transcription -> processing -> mapping -> publication pathway.
- Opal as adapter/translation layer.
- Murmurations profile publishing.

### Out
- Obsidian Sync federation transport.
- Full Murmurations protocol integration.
- Auto-applying ontology mapping changes without human approval.
- Universal consent/licensing vocabulary standardization.

## Governance Model
- Co-stewards on equal footing: Darren, Benjamin, Shawn.
- Major architecture/governance decisions: 2-of-3 approval.
- Weekly rotating facilitator across co-stewards.

## Architecture

### Topology
```text
[Front Range Non-KOI Node]
          <--> [Adapter Gateway] <--> [Salish Sea / Octo KOI Node]
          <--> [Adapter Gateway] <--> [Cascadia KOI Node]
```

### Core Interop Commitments
All cross-network artifacts must include:
- what is shared (`payload` or payload reference)
- who attests (`attestations`/provenance)
- who can use/how (`rights_and_consent`)

### Reference Profile (CommonsChange)
- `change_id`, `artifact_id`, `mode`, `change_type`
- `payload`, `attestations`, `rights_and_consent`
- `published_at`, `local_type`, `canonical_type`, `mapping_context`
- adapter-specific metadata is non-canonical

### API Surfaces
- `POST /interop/changes/ingest`
- `GET /interop/changes/poll`
- `POST /interop/changes/ack`
- `POST /interop/translate/koi-to-commons`
- `POST /interop/translate/commons-to-koi`
- `POST /interop/translate/nonkoi-to-commons`
- `GET /interop/conflicts`
- `POST /interop/conflicts/{id}/resolve`

## Pilot Hypotheses
1. A thin meta-protocol is sufficient for KOI and non-KOI interop in pilot scope.
2. Snapshot-mode participants can interoperate without native event runtimes.
3. Preserving `local_type` for unmapped concepts improves ontological plurality without blocking exchange.
4. Consent-aware boundaries can be enforced across adapters and KOI nodes.

## Ontology Commoning Track
- Add schema profiling + mapping proposal workflows.
- Human-reviewed mapping approvals only.
- Preserve source-layer representations even when unmapped.
- Record rationale and provenance for every approved/rejected mapping.

## BKC Integration Track (Transcription + Mapping)
1. Intake and consent capture.
2. Transcript generation with speaker attribution and timestamps.
3. Human QA correction pass.
4. Entity/practice/pattern extraction.
5. Ontology mapping review and approval.
6. Consent-aware publication/export.

## 8-Week Execution Plan
1. Week 1: governance updates, layer alignment, consent slot definitions.
2. Week 2: adapter gateway skeleton and KOI/non-KOI translation stubs.
3. Week 3: Front Range non-KOI connector + first event and snapshot tests.
4. Week 4: transcription intake + QA workflow MVP.
5. Week 5: ontology mapping review queue + approval logging.
6. Week 6: cross-bioregion exchange run (Front Range <-> Salish/Cascadia).
7. Week 7: hardening, monitoring, conflict and consent alerting.
8. Week 8: public demo + retrospective + phase-next decisions.

## Test Matrix
1. Front Range non-KOI changes interoperate with KOI nodes through gateway.
2. KOI-to-commons and non-KOI-to-commons translation preserves IDs/provenance.
3. Snapshot-mode export is accepted and queryable by KOI-connected peers.
4. Consent policy violations block export and raise alerts.
5. Shared field conflicts route to manual queue and require explicit resolution.
6. Mapping proposals cannot be published without human approval.
7. Unmapped `local_type` artifacts are preserved and surfaced for mapping review.
8. Transcript artifacts without consent metadata are rejected.
9. p95 propagation latency remains under 120s in pilot runs.

## Assumptions
- 8-week pilot remains feasible with triad co-steward coordination.
- Front Range chooses non-KOI primary stack in phase 1.
- Cascadia and Salish Sea remain KOI-enabled.
- Opal remains adapter role, not canonical data store.
- `CommonsChange` is an optional reference profile, not universal protocol.

## Supersession
This plan supersedes `pilots/front-range-cascadia-2026/dual-bioregion-pilot-plan-v1.md`.
