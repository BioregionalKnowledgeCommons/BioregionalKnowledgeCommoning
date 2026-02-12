# Node Participation Profiles

## Purpose
Define practical participation choices for bioregions while keeping KOI optional.

Profiles are operational guidance. They are not status tiers.

## Profile Overview
| Profile | Typical Stack | Interop Path | Complexity |
|---|---|---|---|
| Non-KOI Node | GitHub/Notion/Obsidian/DB + adapter | Meta-protocol + reference profile serialization | Low to medium |
| KOI Full Node | KOI runtime + signed events | Native KOI + profile translation where needed | Medium to high |
| KOI Gateway/Partial | Existing system + KOI edge gateway | Gateway emits/ingests profile artifacts | Medium |

## Profile A: Non-KOI Node
### Minimum Capabilities
- Publish machine-readable artifacts at L1.
- Provide rights/consent and attestation metadata.
- Support event or snapshot mode.

### Recommended Capabilities
- Adapter export to CommonsChange profile.
- Mapping queue for local_type to canonical_type proposals.
- Audit log for outbound publications.

### Best For
- Teams prioritizing rapid setup and low ops overhead.
- Communities already invested in non-KOI workflows.

## Profile B: KOI Full Node
### Minimum Capabilities
- Run KOI endpoints and key management.
- Exchange signed events.
- Maintain peer registry and edge policies.

### Recommended Capabilities
- Translation gateway for non-KOI peers.
- Strict-mode progression plan.
- Dedicated observability for delivery/confirm loops.

### Best For
- Teams needing native event-driven federation and signed-envelope workflows.
- Coordinators with higher operational capacity.

## Profile C: KOI Gateway/Partial
### Minimum Capabilities
- Maintain local system of record.
- Run gateway to translate local artifacts to profile-compatible exchange.
- Enforce consent boundary checks before federation publication.

### Recommended Capabilities
- Support both event and snapshot exports.
- Backpressure and retry logic.
- Conflict queue for shared fields.

### Best For
- Bioregions that want KOI edge compatibility without full KOI runtime replacement.

## Selection Guidance
Choose by constraints, not ideology:
1. If governance and data workflows are still early, start with Non-KOI.
2. If you need native signed-event federation now, use KOI Full.
3. If you have mature local systems and need bridge interoperability, use KOI Gateway/Partial.

## Migration Paths
- Non-KOI -> KOI Gateway/Partial: add gateway first.
- KOI Gateway/Partial -> KOI Full: move core publication to KOI runtime.
- KOI Full -> mixed profile: keep KOI core, add adapter for profile diversity.

## Governance Prerequisite (All Profiles)
Before cross-node publication:
- define consent tiers
- define steward authority
- define reclassification/revocation workflow
