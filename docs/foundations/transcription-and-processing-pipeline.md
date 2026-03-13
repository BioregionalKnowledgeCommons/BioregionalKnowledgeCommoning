# Transcription and Processing Pipeline

## Purpose
Support the BKC Practices and Patterns effort by enabling consent-aware interview transcription, processing, and ontology mapping.

## Pipeline
1. Intake
- Register interview metadata and consent policy before processing.

2. Transcription
- Produce timestamped transcript with speaker attribution.

3. QA
- Human pass for correction and redaction where required.

4. Extraction
- Extract entities, practices, patterns, claims, and evidence.

5. Mapping
- Create ontology mapping proposals and route to review.

6. Publication
- Publish only consent-permitted outputs (public or restricted tiers as configured).
- `community_only` outputs are written to the local graph with `node_private = true` — accessible to node operators but hidden from public API, chat, search, and federation.

7. Audit
- Maintain traceability from recording -> transcript -> extraction -> mapping -> publication.

## Required Metadata
- source/interview ID
- participants and roles
- consent tier: `public`, `restricted`, `community_only`, or `private`
- usage constraints
- processing timestamps
- reviewer identity

### Consent Tier Definitions

| Tier | Meaning | Technical enforcement |
|---|---|---|
| `public` | Open to all — searchable, federable, published on Quartz | `visibility_scope = "public"`, `node_private = false` |
| `restricted` | Shared with attribution — same technical treatment as public, governance constraints apply at the human layer | `visibility_scope = "public"`, `node_private = false` |
| `community_only` | Local graph only — hidden from all public search, chat, API, and federation endpoints | `visibility_scope = "node_private"`, `node_private = true`, no `koi_rid` assigned |
| `private` | Never published — stays in workspace as working material | `visibility_scope = "node_private"`, `node_private = true`, no `koi_rid` assigned |

The consent boundary is enforced at the database level: `community_only` and `private` entities have `node_private = true` in `entity_registry`, which excludes them from every public query path. This is not policy-only — the infrastructure enforces it.

## Acceptance Criteria (Pilot)
- At least one interview transcript processed end-to-end.
- Consent metadata validated at intake and before publication.
- Mapping approvals recorded with rationale.
- Export pipeline blocks artifacts missing consent metadata.
