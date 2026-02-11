# Dual Bioregion Pilot Plan v2

## Summary
This version updates v1 to support equal triad governance (Darren, Benjamin, Shawn), KOI-optional participation, and explicit ontology commoning + transcription/mapping integration aligned with the BKC project proposal.

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
- Transport-neutral interoperability contract (`CommonsChange`).
- Ontology commoning workflow with human-approved mappings.
- Interview transcription -> processing -> mapping -> publication pathway.
- Opal as adapter/translation layer.
- Murmurations profile publishing.

### Out
- Obsidian Sync federation transport.
- Full Murmurations protocol integration.
- Auto-applying ontology mapping changes without human approval.

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

### Core Contract
All interoperability normalizes into `CommonsChange`:
- `change_id`, `entity_id`, `entity_type`, `change_type`
- `payload`, `source_system`
- `provenance`, `consent`, `mapping_context`

### API Surfaces
- `POST /interop/changes/ingest`
- `GET /interop/changes/poll`
- `POST /interop/changes/ack`
- `POST /interop/translate/koi-to-commons`
- `POST /interop/translate/commons-to-koi`
- `POST /interop/translate/nonkoi-to-commons`
- `GET /interop/conflicts`
- `POST /interop/conflicts/{id}/resolve`

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
1. Week 1: governance updates, contract definitions, consent taxonomy.
2. Week 2: adapter gateway skeleton and KOI/non-KOI translation stubs.
3. Week 3: Front Range non-KOI connector + first data flow tests.
4. Week 4: transcription intake + QA workflow MVP.
5. Week 5: ontology mapping review queue + approval logging.
6. Week 6: cross-bioregion exchange run (Front Range <-> Salish/Cascadia).
7. Week 7: hardening, monitoring, conflict and consent alerting.
8. Week 8: public demo + retrospective + phase-next decisions.

## Test Matrix
1. Front Range non-KOI changes interoperate with KOI nodes through gateway.
2. KOI-to-commons and nonKoi-to-commons translation preserves IDs/provenance.
3. Consent policy violations block export and raise alerts.
4. Shared field conflicts route to manual queue and require explicit resolution.
5. Mapping proposals cannot be published without human approval.
6. Transcript artifacts without consent metadata are rejected.
7. p95 propagation latency remains under 120s in pilot runs.

## Assumptions
- 8-week pilot remains feasible with triad co-steward coordination.
- Front Range chooses non-KOI primary stack in phase 1.
- Cascadia and Salish Sea remain KOI-enabled.
- Opal remains adapter role, not canonical data store.

## Supersession
This plan supersedes `pilots/front-range-cascadia-2026/dual-bioregion-pilot-plan-v1.md`.
