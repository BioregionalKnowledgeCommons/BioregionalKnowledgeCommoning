# Bioregional Mapping Model v0.1

## Purpose

Define the canonical semantic model for bioregional mapping work in BKC.

This is a graph-first profile over the existing BKC / Octo bridge ontology. It is not a separate competing ontology.

## Relationship to the Current Octo Ontology

The bridge ontology currently implemented in `Octo/ontology/bkc-ontology.jsonld` is the shared interoperability layer for this model.

This document does three things:

1. selects the subset of that ontology needed for mapping-first collaboration
2. clarifies how local and domain ontologies relate to the shared bridge layer
3. defines how different interface views project from the same graph-native substrate

## Core Position

### 1. Graph first
The canonical layer is a knowledge graph with ontology-aware entities and relations.

### 2. Views are projections
Geographic maps, tables, discourse graphs, and narrative gardens are all projections over the same canonical graph.

### 3. Bridge ontology, not universal ontology
The BKC / Octo ontology is the shared bridge layer for interoperability, not the final ontology for all bioregional knowledge.

### 4. Stable kernel plus emergent extensions
Use a stable shared kernel for cross-bioregion exchange, while allowing local and domain ontologies to emerge through governed mappings and extensions.

## Stable Shared Kernel

The following classes form the required kernel for mapping-first work.

| Class | Role in mapping-first work | Status |
|---|---|---|
| `Bioregion` | Named ecological-cultural region | Required |
| `Location` | Place, watershed, city, monitoring site, basin, territory | Required |
| `Organization` | Stewarding group, institution, collective, agency | Required |
| `Project` | Coordinated initiative or body of work | Required |
| `Practice` | Local or place-based way of doing something | Required |
| `Pattern` | Cross-context generalization emerging from practices | Required |
| `Protocol` | Reusable coordination pattern | Required |
| `Playbook` | Local implementation of a protocol | Required |
| `Question` | Open inquiry worth tracking | Required |
| `Claim` | Assertion or conclusion | Required |
| `Evidence` | Data, observation, or supporting artifact | Required |
| `CaseStudy` | Documented real-world example | Optional but recommended |
| `Concept` | Shared term or domain concept | Required |
| `Meeting` | Coordination event or interview session | Optional but recommended |

## Required Relation Profile

These relations are sufficient for the mapping-first phase and are compatible with the current bridge ontology and BKC docs.

| Relation | Primary use |
|---|---|
| `located_in` | Place and scope grounding |
| `has_project` | Organization to project linkage |
| `practiced_in` | Practice to bioregion linkage |
| `documents` | Case study to practice or pattern linkage |
| `aggregates_into` | Practice to pattern emergence |
| `suggests` | Pattern to practice recommendation |
| `about` | Discourse grounding to domain entities |
| `supports` | Evidence or claim support linkage |
| `opposes` | Evidence or claim opposition linkage |
| `informs` | General learning loop linkage |
| `generates` | Question, meeting, or event output linkage |
| `implemented_by` | Protocol to playbook linkage |
| `broader` | Cross-scale hierarchy |
| `narrower` | Cross-scale hierarchy |
| `related_to` | Soft conceptual linkage |
| `builds_on` | Lineage or dependency |
| `inspired_by` | Conceptual inspiration |

## Mapping Lenses

A mapping packet should be able to answer one or more of these questions:

- `who_is_here`
- `what_is_happening`
- `what_needs_attention`
- `what_indicators_matter`
- `what_practices_exist`
- `what_patterns_might_be_emerging`
- `what_should_not_cross_boundaries`

These are mapping contexts, not ontology classes.

## Ontological Commoning Fields

The semantic model must allow the source layer to remain visible.

At minimum, mapped artifacts should be able to preserve:

- `source_ontology`
- `local_type`
- `canonical_type`
- `mapping_status`
- `mapping_notes`

Allowed mapping statuses:

- `equivalent`
- `narrower`
- `broader`
- `related`
- `unmapped`
- `proposed_extension`

## Projection Model

### 1. Geographic projection
Use when the primary task is spatial orientation.

Examples:
- watersheds
- bioregion extents
- monitoring stations
- project areas

The geographic view is a projection over graph entities and relations, not the canonical source of truth.

### 2. Graph / discourse projection
Use when the primary task is reasoning, comparison, or learning loops.

Examples:
- practice to pattern emergence
- question / claim / evidence structures
- organization and project relationships
- protocol and playbook lineage

### 3. Tabular / ops projection
Use when the primary task is coordination, audit, or review.

Examples:
- mapping packet review queue
- ontology mapping proposals
- indicator inventory
- project and steward registries

### 4. Narrative / knowledge-garden projection
Use when the primary task is public explanation, storytelling, or reflective synthesis.

Examples:
- Quartz essays
- case study pages
- project summaries
- cross-bioregion comparison notes

## Local and Domain Ontologies

This mapping model does not require each bioregion to collapse into the shared bridge ontology.

Local and domain ontologies may include concepts for:

- Indigenous governance and kinship terms
- watershed-specific stewardship concepts
- local legal or civic structures
- funding and commitment mechanisms
- interview and ethnographic categories

Cross-bioregion interoperability only requires that a bridge-compatible projection can be produced where consent allows.

## What This Model Avoids

This model avoids two bad defaults:

1. `GIS first` - where place geometry becomes the canonical structure and everything else is bolted on later
2. `one true ontology` - where a central schema erases local conceptual worlds

## Compatibility and Export

This model is compatible with:

- current KOI and BKC runtime structures
- future RDF / JSON-LD export
- future richer linked-data publication
- graph-backed map, table, and narrative interfaces

RDF publication is a future export target, not a requirement for initial collaboration.
