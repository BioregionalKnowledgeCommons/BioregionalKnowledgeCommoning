# Bioregional Mapping Intake Contract v0.1

## Purpose

Define the minimum semantic packet for graph-first bioregional mapping while staying compatible with the current BKC ingest surface.

This is a docs-level contract. It does not introduce a new runtime endpoint.

## Important Constraint

The current BKC `/ingest` endpoint directly accepts only a transport subset:

- `document_rid`
- `source`
- `content`
- `entities`
- `relationships`

This contract defines the richer canonical packet that collaborators should produce. An adapter or operator can then map the supported subset into `/ingest` while preserving the remaining metadata in a sidecar, source record, or review artifact.

## Canonical Packet Shape

```json
{
  "document_rid": "source:type:id",
  "source": "pipeline-or-team-slug",
  "published_at": "2026-03-06T00:00:00Z",
  "content": "Optional plain-text summary",
  "mapping_context": "who_is_here",
  "rights_and_consent": {
    "consent_tier": "public",
    "share_scope": "cross_bioregion",
    "allowed_uses": ["research", "mapping"],
    "reviewer": "Person Name"
  },
  "source_ontology": "local-ontology-slug",
  "entities": [],
  "relationships": []
}
```

## Required Top-Level Fields

| Field | Required | Notes |
|---|---|---|
| `document_rid` | Yes | Stable packet identifier |
| `source` | Yes | Pipeline or contributor identifier |
| `published_at` | Yes | Packet timestamp |
| `mapping_context` | Yes | One of the mapping lenses below |
| `rights_and_consent` | Yes | Required for publication and sharing |
| `entities` | Yes | Entities in the packet |
| `relationships` | Yes | Relationship bundle |
| `content` | No | Human-readable summary |
| `source_ontology` | No | Local schema or source-layer vocabulary identifier |

## Allowed Mapping Contexts

- `who_is_here`
- `what_is_happening`
- `what_needs_attention`
- `what_indicators_matter`
- `what_practices_exist`
- `what_patterns_might_be_emerging`
- `what_should_not_cross_boundaries`

## rights_and_consent Shape

```json
{
  "consent_tier": "public|restricted|private|community_only",
  "share_scope": "local|bioregion|cross_bioregion",
  "allowed_uses": ["research", "mapping", "governance", "learning"],
  "reviewer": "Person Name",
  "usage_notes": "Optional constraints or context"
}
```

### Consent Tier Enforcement

Consent tiers are enforced at the database level via `visibility_scope` and `node_private`:

| Tier | Effect |
|---|---|
| `public` | Entities visible in public search, chat, API, and federation |
| `restricted` | Same technical treatment as public; governance constraints apply at the human layer |
| `community_only` | Entities have `node_private = true` — hidden from all public API endpoints, chat, search, and federation. Accessible to node operators only |
| `private` | Same technical enforcement as `community_only` — hidden from all public paths |

Packets with `consent_tier: "community_only"` or `"private"` will have their entities registered with `visibility_scope: "node_private"`, ensuring the consent boundary is enforced by infrastructure, not policy alone.
```

## Entity Shape

```json
{
  "name": "South Platte River Watershed",
  "type": "Location",
  "context": "Urban-watershed context for Front Range water stewardship",
  "confidence": 0.93,
  "local_type": "Watershed",
  "canonical_type": "Location",
  "source_ontology": "front-range-water-v0",
  "mapping_status": "equivalent",
  "mapping_notes": "Watershed kept as local subtype of Location in the bridge layer"
}
```

## Required Entity Fields

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | Display or canonical label |
| `type` | Yes | Current bridge-compatible type |
| `context` | No | Disambiguation helper |
| `confidence` | No | Extraction or author confidence |
| `local_type` | No | Source-layer type if different |
| `canonical_type` | No | Proposed bridge-layer type |
| `source_ontology` | No | Origin schema or vocabulary |
| `mapping_status` | No | Current mapping decision status |
| `mapping_notes` | No | Human-readable rationale |

## Relationship Shape

```json
{
  "subject": "South Platte Water Conservation",
  "predicate": "located_in",
  "object": "Front Range",
  "confidence": 0.95,
  "mapping_notes": "Bridge-compatible relation"
}
```

## Allowed Mapping Status Values

- `equivalent`
- `narrower`
- `broader`
- `related`
- `unmapped`
- `proposed_extension`

## Current Bridge-Compatible Types

Use the current shared bridge layer where possible:

- `Person`
- `Organization`
- `Project`
- `Location`
- `Concept`
- `Meeting`
- `Practice`
- `Pattern`
- `CaseStudy`
- `Bioregion`
- `Protocol`
- `Playbook`
- `Question`
- `Claim`
- `Evidence`

## Current Bridge-Compatible Relations

Use the existing bridge-compatible relations where possible:

- `located_in`
- `has_project`
- `practiced_in`
- `documents`
- `aggregates_into`
- `suggests`
- `about`
- `supports`
- `opposes`
- `informs`
- `generates`
- `implemented_by`
- `broader`
- `narrower`
- `related_to`
- `builds_on`
- `inspired_by`

## Transport to Current `/ingest`

When using the current BKC transport, send only the supported subset:

```json
{
  "document_rid": "source:type:id",
  "source": "pipeline-or-team-slug",
  "content": "Optional plain-text summary",
  "entities": [
    {
      "name": "South Platte River Watershed",
      "type": "Location",
      "context": "Urban-watershed context for Front Range water stewardship",
      "confidence": 0.93
    }
  ],
  "relationships": [
    {
      "subject": "South Platte Water Conservation",
      "predicate": "located_in",
      "object": "Front Range",
      "confidence": 0.95
    }
  ]
}
```

The richer fields should be preserved outside the current endpoint until a richer ingest surface exists.

## Example A: Front Range Mapping Packet

```json
{
  "document_rid": "front-range-mapping:packet:south-platte-001",
  "source": "front-range-mapping",
  "published_at": "2026-03-06T00:00:00Z",
  "mapping_context": "what_is_happening",
  "rights_and_consent": {
    "consent_tier": "public",
    "share_scope": "cross_bioregion",
    "allowed_uses": ["mapping", "research"],
    "reviewer": "Darren Zal"
  },
  "source_ontology": "front-range-water-v0",
  "content": "South Platte watershed stewardship and related Front Range practices.",
  "entities": [
    {
      "name": "Front Range",
      "type": "Bioregion",
      "mapping_status": "equivalent"
    },
    {
      "name": "South Platte River Watershed",
      "type": "Location",
      "local_type": "Watershed",
      "canonical_type": "Location",
      "mapping_status": "equivalent"
    },
    {
      "name": "South Platte Water Conservation",
      "type": "Practice",
      "mapping_status": "equivalent"
    }
  ],
  "relationships": [
    {
      "subject": "South Platte Water Conservation",
      "predicate": "located_in",
      "object": "Front Range"
    }
  ]
}
```

## Example B: Salish Sea Mapping Packet

```json
{
  "document_rid": "salish-sea-mapping:packet:vlg-001",
  "source": "salish-sea-mapping",
  "published_at": "2026-03-06T00:00:00Z",
  "mapping_context": "who_is_here",
  "rights_and_consent": {
    "consent_tier": "public",
    "share_scope": "cross_bioregion",
    "allowed_uses": ["mapping", "learning"],
    "reviewer": "Darren Zal"
  },
  "source_ontology": "salish-sea-civic-v0",
  "entities": [
    {
      "name": "Salish Sea",
      "type": "Bioregion",
      "mapping_status": "equivalent"
    },
    {
      "name": "Victoria Landscape Group",
      "type": "Organization",
      "mapping_status": "equivalent"
    },
    {
      "name": "Landscape Hub Cultivator",
      "type": "Project",
      "mapping_status": "equivalent"
    }
  ],
  "relationships": [
    {
      "subject": "Victoria Landscape Group",
      "predicate": "has_project",
      "object": "Landscape Hub Cultivator"
    }
  ]
}
```

## Example C: Local Concept Preserved Without Forced Mapping

```json
{
  "document_rid": "example:packet:local-term-001",
  "source": "example-biome-team",
  "published_at": "2026-03-06T00:00:00Z",
  "mapping_context": "what_should_not_cross_boundaries",
  "rights_and_consent": {
    "consent_tier": "restricted",
    "share_scope": "local",
    "allowed_uses": ["review"],
    "reviewer": "Local Steward"
  },
  "source_ontology": "example-local-governance-v0",
  "entities": [
    {
      "name": "Custodian Circle",
      "type": "Concept",
      "local_type": "CustodianCircle",
      "canonical_type": null,
      "mapping_status": "unmapped",
      "mapping_notes": "Keep local until ontology review; do not flatten into Organization or Protocol"
    }
  ],
  "relationships": []
}
```
