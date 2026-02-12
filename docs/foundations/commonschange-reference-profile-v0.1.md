# CommonsChange Reference Profile v0.1

## Purpose
Provide one implementable profile for interoperability under the Knowledge Commoning Meta-Protocol.

This is a reference profile, not a mandatory standard.

## Position in Stack
- Pattern Language: defines recurring social/interop design patterns.
- Meta-Protocol: defines minimum invariant commitments.
- CommonsChange: concrete serialization for implementation teams.

## Canonical CommonsChange Shape
```yaml
change_id: string
artifact_id: string
mode: event|snapshot
change_type: create|update|delete|snapshot_replace|snapshot_append
payload:
  content: object|string|null
  content_ref: string|null
attestations:
  - actor_id: string
    actor_role: author|contributor|reviewer|system
    attested_at: datetime
    evidence_ref: string|null
rights_and_consent:
  policy_ref: string|null
  consent_tier: string
  allowed_uses: [string]
  restricted_uses: [string]
  steward_authority: string
published_at: datetime
local_type: string|null
canonical_type: string|null
mapping_context: object|null
```

## Canonical Field Rules
- `change_id` required for idempotency and audit.
- `artifact_id` required to track continuity across updates/snapshots.
- `mode` required to disambiguate event vs snapshot semantics.
- `attestations` required, at least one attestation.
- `rights_and_consent` required.
- `local_type` optional but strongly recommended.
- `canonical_type` optional.

If a concept cannot be mapped to shared vocabulary:
- keep `local_type`
- set `canonical_type` to null
- include mapping note in `mapping_context`.

## Adapter Metadata (Non-Canonical)
Implementation-specific data must be carried in adapter metadata, not canonical core.

Example:
```yaml
adapter_metadata:
  transport: koi
  source_system: octo
  source_endpoint: /koi-net/events/poll
  signature_alg: ECDSA-P256
```

This prevents stack leakage into the canonical contract.

## Event and Snapshot Semantics

### Event Mode
- `change_type` values: `create|update|delete`
- expected ordering and dedupe behavior defined by adapter implementation.

### Snapshot Mode
- `change_type` values: `snapshot_replace|snapshot_append`
- snapshots must include clear publication timestamp and scope descriptor.

## Example: Non-KOI Snapshot Publisher
```yaml
change_id: "fr-2026-03-01-snapshot-001"
artifact_id: "front-range-practices-catalog"
mode: snapshot
change_type: snapshot_replace
payload:
  content_ref: "https://example.org/catalogs/practices-2026-03-01.json"
attestations:
  - actor_id: "front-range-team"
    actor_role: reviewer
    attested_at: "2026-03-01T10:00:00Z"
rights_and_consent:
  consent_tier: "public"
  allowed_uses: ["discover", "reference"]
  restricted_uses: ["derivative_without_review"]
  steward_authority: "front-range-stewards"
published_at: "2026-03-01T10:00:00Z"
local_type: "practice_catalog"
canonical_type: "Practice"
```

## Example: KOI Event Adapter Output
```yaml
change_id: "koi-event-abc123"
artifact_id: "orn:koi-net.practice:salmon-restoration+..."
mode: event
change_type: update
payload:
  content_ref: "koi://bundles/orn:koi-net.practice:salmon-restoration+..."
attestations:
  - actor_id: "orn:koi-net.node:octo-salish-sea+..."
    actor_role: system
    attested_at: "2026-03-02T08:10:00Z"
rights_and_consent:
  consent_tier: "restricted"
  allowed_uses: ["internal-learning"]
  restricted_uses: ["public-export"]
  steward_authority: "salish-sea-stewards"
published_at: "2026-03-02T08:10:00Z"
local_type: "Practice"
canonical_type: "Practice"
adapter_metadata:
  transport: koi
  source_endpoint: "/koi-net/events/poll"
```

## Validation Checklist
- Required fields present.
- At least one attestation present.
- Rights/consent block present.
- Event/snapshot semantics align with mode.
- Unmapped concepts preserved (not dropped).

## Versioning
- Version: `v0.1`
- Breaking changes require profile version increment and migration notes.
