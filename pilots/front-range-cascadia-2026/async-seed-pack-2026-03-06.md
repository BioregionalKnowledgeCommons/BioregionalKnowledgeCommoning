# Async Seed Pack - 2026-03-06

## Purpose

This is an async seed for the bioregional swarm group.

I will be traveling and will not be present live, so this is meant to leave behind something concrete without imposing on Boulder or Front Range planning. It is also not written from a Boulder-local perspective. My grounded stewardship context is Cascadia, especially the Salish Sea, Greater Victoria, and Cowichan Valley.

What I can offer is a working reference implementation for inter-bioregional knowledge commoning.

## Verified Federation Snapshot

Verified on Friday, March 6, 2026. Four nodes are live and healthy in a federated knowledge graph:

- Salish Sea (coordinator)
- Front Range (peer node)
- Greater Victoria (leaf node)
- Cowichan Valley (leaf node)

Each node runs its own database and identity. Nodes exchange knowledge via signed envelopes with cryptographic verification. A governance membrane at the coordinator gates which nodes can join and what knowledge flows between them.

## Front Range Node

Front Range is already real infrastructure, not just a plan. It is searchable and contains real entities including: Front Range (Bioregion), Boulder (Location), Boulder Watershed Initiative (Project), South Platte River Watershed (Location), South Platte Water Conservation (Practice), Colorado River Basin (Concept), Colorado River Basin Watershed Data Aggregator (Project).

Browse and search all nodes: https://salishsee.life/commons

## How Knowledge Moves Between Bioregions

The core capability is a pipeline that turns local knowledge into shared, discoverable artifacts:

1. Local interviews, transcripts, or field notes get imported into a node
2. An extraction pipeline pulls out structured artifacts: practices (what people actually do), patterns (what recurs across places), and protocols (how to reproduce what works)
3. A human steward reviews extracted artifacts and sets consent tiers (public, community-only, or private)
4. Approved artifacts are published to the local knowledge graph
5. Federation carries approved artifacts to other nodes via signed events
6. Other bioregions can now search, discover, compare, and build on those artifacts

Community-only knowledge stays local. It never leaves the node, never appears in public search or chat, never federates. The consent boundary is enforced by the database, not by policy alone.

This means a practice documented in the Salish Sea can become discoverable in the Front Range graph, but only after human review, consent classification, and governed publication.

## What the Salish Sea Infrastructure Can Offer

What already exists and can be reused across bioregions:

- live federated knowledge graph across 4 nodes
- the practice-to-pattern-to-protocol extraction pipeline described above
- a governance membrane for staged and stewarded knowledge crossing
- graph-grounded search and chat
- an ingest path for structured knowledge packets
- a working ontology and relationship vocabulary
- a graph-first model for bioregional mapping

This is enough to support cross-bioregional learning now without forcing everyone onto the same stack.

## Ontology Position

The current shared ontology should be treated as a bridge ontology, not a universal worldview ontology.

Practical position:

- use the current bridge ontology for interoperability
- preserve local terms and local ontologies when they do not map cleanly
- let extensions emerge from repeated practice and review
- never force local concepts into false equivalence just to make the graph tidy

This means ontological commoning happens through governed mappings, extensions, and review, not through premature standardization.

## Graph First, Views as Projections

The map is not the model.

The canonical layer should be a knowledge graph with an ontology-aware data model. Different interfaces are projections over that same substrate:

- geographic map projection
- graph / discourse projection
- table / ops projection
- narrative / knowledge-garden projection

This keeps place, practice, evidence, and protocol knowledge in one shared semantic structure instead of scattering it across separate tools with incompatible schemas.

## Why Start with Mapping

Mapping is the first shared practice because it answers the questions that every later layer depends on:

- who is already here
- what is already happening
- what problems need attention
- what practices are already working
- what indicators matter locally
- what should remain local or consent-gated

Once that is mapped in a graph-native way, later layers become much easier:

- pattern mining
- cross-bioregion comparison
- matchmaking
- commitment pooling
- flow funding
- quadratic funding
- evidence-linked allocation

## Why Interviews Matter

Interviews are not just content collection. They are one of the main ways to surface local terms, local governance concepts, actual practices, recurring patterns, tensions between ontologies, and questions that deserve shared protocol support.

The extraction pipeline described above makes interviews first-class graph inputs:

`recording -> transcript -> QA -> extraction -> review -> governed publication -> searchable graph -> federation`

## Three Async Collaboration Seams

### 1. Mapping Packet Exchange

Contribute one packet describing:

- a place or bioregion
- one organization
- one active project or practice
- one key problem or question
- one indicator worth tracking

Available:

- graph-first mapping model
- shared relationship vocabulary
- ingest profile and examples

### 2. Interview Packet Exchange

Contribute one interview transcript or structured interview summary with clear consent metadata.

Available:

- interview-to-graph MVP spec
- extraction and mapping review approach
- graph-native publication target

### 3. Indicator Overlay

Contribute one small ecological or social indicator set tied to a watershed, place, or bioregion.

Available:

- existing Front Range and Salish Sea examples
- graph structure for linking indicator data to places, practices, questions, and evidence

## Low-Friction Next Steps

Any collaborator could do one of these asynchronously:

1. Send one mapping packet using the bridge profile.
2. Send one interview packet with consent metadata.
3. Propose one local ontology term that does not map cleanly and should remain local for now.
4. Contribute one small indicator set tied to a place and a problem.
5. Compare one local practice against an existing Cascadia or Front Range practice.

## What This Is Not

This is not:

- a claim to know Boulder from the inside
- a request that anyone adopt this stack
- a request to standardize away local differences
- a claim that one ontology should govern all bioregional knowledge

It is an offer to share working infrastructure and a graph-native method for commoning knowledge across places without flattening those places.

## Relevant Artifacts

Core docs in this repo:

- `docs/foundations/bioregional-mapping-model-v0.1.md`
- `docs/foundations/bioregional-mapping-intake-contract-v0.1.md`
- `docs/foundations/interview-to-graph-mvp-v0.1.md`
- `docs/foundations/ontology-commoning-ops-v0.1.md`
- `docs/foundations/ontology-commoning-framework.md`
- `docs/foundations/transcription-and-processing-pipeline.md`
- `pilots/front-range-cascadia-2026/mapping-first-collaboration-proposal-2026-03-06.md`

Runtime / integration references:

- `Octo/docs/integration/summarizer-ingest-contract.md`
- `pilots/front-range-cascadia-2026/partner-quickstart.md`
- `https://salishsee.life/commons`

## Success Condition for Next Week

This seed did its job if, by next week, at least one outside collaborator can do one of the following without another architecture meeting:

- submit a graph-compatible mapping packet
- contribute an interview packet for processing
- propose a local ontology term plus mapping status
- identify a concrete comparison between their bioregion and Cascadia or Front Range
