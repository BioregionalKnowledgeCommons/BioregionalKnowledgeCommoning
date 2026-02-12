# Tooling and Field Authority Map

## Tool Roles
- GitHub: human authoring, review, collaboration, and public discoverability.
- KOI-net: optional transport for signed event federation and provenance exchange.
- Non-KOI stacks (including Opal-based flows): valid peers through adapter gateways.
- Opal: translation and orchestration adapter role, not canonical persistence.
- Murmurations: publish-only profile for discovery metadata in phase 1.
- Obsidian Sync: not used as federation transport in this pilot.

## Participation Profiles
| Profile | Role in this pilot | Required output |
|---|---|---|
| Non-KOI Node | Front Range baseline path | Meta-protocol compatible artifacts (event and/or snapshot) |
| KOI Full Node | Cascadia + Salish Sea path | KOI events plus translation to/from reference profile |
| KOI Gateway/Partial | Optional hybrid path | Adapter-mediated translation between local stack and reference profile |

KOI is optional for protocol participation.

## Meta-Protocol Commitments (Canonical)
Any cross-network artifact must include:
- what is shared (`payload`)
- who attests (`attestations`)
- who can use/how (`rights_and_consent`)

## CommonsChange Reference Profile (Pilot Implementation)
Canonical profile fields:
- `change_id`, `artifact_id`, `mode`, `change_type`
- `payload`, `attestations`, `rights_and_consent`
- `published_at`, `local_type`, `canonical_type`, `mapping_context`

Non-canonical adapter metadata:
- transport details (for example KOI endpoint references)
- source stack identifiers
- signature mechanism details

## Dual-Canonical Authority Policy

### GitHub Authoritative Fields
- `title`
- `summary`
- markdown narrative body
- editorial tags and labels
- human curation notes

### Protocol/Provenance Authoritative Fields
- stable IDs (`rid` or equivalent cross-network ID)
- signature and event metadata
- source node metadata
- consent status
- provenance chain
- cross-reference IDs

### Shared Fields (Manual Conflict Path)
- `canonical_type`
- canonical slug
- `bioregion`

## Merge Rules
1. GitHub-authoritative fields cannot be overwritten by protocol exports.
2. Protocol/provenance authoritative fields cannot be overridden by direct GitHub edits.
3. Shared-field conflicts are queued for manual review.
4. Every merge/rejection records actor, timestamp, source, before/after, and rationale.

## Conflict Severity
- High: consent/provenance mismatch, stable-ID mismatch, type mismatch.
- Medium: canonical slug or bioregion mismatch.
- Low: non-authoritative annotation differences.
