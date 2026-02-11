# Tooling and Field Authority Map

## Tool Roles
- GitHub: human authoring, review, collaboration, and discoverability.
- KOI-net: signed event federation, provenance, cross-node synchronization.
- Opal: translation adapter only (no canonical persistence role).
- Murmurations: publish-only profile for discovery metadata.
- Obsidian Sync: not used in this pilot.

## Dual-Canonical Authority Policy

### GitHub authoritative fields
- `title`
- `summary`
- markdown narrative body
- editorial tags and labels
- human curation notes

### KOI authoritative fields
- `rid`
- event signature fields
- event timestamps
- source node metadata
- consent status
- provenance chain
- cross-reference IDs

### Shared fields (manual conflict path)
- `entity_type`
- canonical slug
- `bioregion`

## Merge Rules
1. If field authority is GitHub, KOI export cannot overwrite it.
2. If field authority is KOI, GitHub edits to that field are rejected and routed to conflict handling.
3. Conflicts on shared fields go to manual review queue.
4. Every merge/rejection records: actor, timestamp, source, before/after, and rationale.

## Conflict Severity
- High: consent/provenance mismatch, RID mismatch, type mismatch.
- Medium: canonical slug or bioregion mismatch.
- Low: non-authoritative annotation differences.
