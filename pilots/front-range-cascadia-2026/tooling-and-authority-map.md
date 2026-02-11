# Tooling and Field Authority Map

## Tool Roles
- GitHub: human authoring, review, collaboration, and public discoverability.
- KOI-net: optional transport for signed event federation and provenance exchange.
- Non-KOI node stacks (including Opal-based flows): valid peers through adapter gateways.
- Opal: translation and orchestration adapter only (no canonical persistence role).
- Murmurations: publish-only profile for discovery metadata in phase 1.
- Obsidian Sync: not used as federation transport in this pilot.

## KOI Optionality
KOI is not mandatory for participation in the knowledge commoning protocol.

### Participation modes
1. KOI-native node
- Emits and consumes KOI NEW/UPDATE/FORGET events.
- Uses gateway translation to transport-neutral contract.

2. Non-KOI node
- Emits and consumes transport-neutral change objects directly.
- Can remain GitHub-native/Opal-native without KOI runtime.

## Transport-Neutral Contract
All cross-network interoperability normalizes to a canonical `CommonsChange` object containing:
- `change_id`, `entity_id`, `entity_type`, `change_type`
- `payload`
- `source_system` (`koi`, `github`, `opal`, `other`)
- `provenance`
- `consent`
- `mapping_context`

## Dual-Canonical Authority Policy

### GitHub authoritative fields
- `title`
- `summary`
- markdown narrative body
- editorial tags and labels
- human curation notes

### Protocol/provenance authoritative fields (KOI or gateway)
- stable IDs (`rid` or equivalent cross-network ID)
- signature and event metadata
- source node metadata
- consent status
- provenance chain
- cross-reference IDs

### Shared fields (manual conflict path)
- `entity_type`
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
