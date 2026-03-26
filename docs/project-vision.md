---
doc_id: bkc.project-vision
doc_kind: vision
status: active
depends_on: []
primary_for:
  - project-vision
  - design-principles
---

# BKC Project Vision

**Internal canonical reference.** For external-facing positioning, see [bioregional-swarm-telos.md](./bioregional-swarm-telos.md) and [bioregional-ai-swarms-positioning.md](./bioregional-ai-swarms-positioning.md).

## What we are building

The Bioregional Knowledge Commons (BKC) is federated infrastructure for bioregional knowledge sovereignty. It enables communities to maintain their own knowledge gardens — structured collections of entities, relationships, evidence, and commitments — and selectively share across bioregional boundaries without centralizing control.

BKC sits within a three-plane architecture for bioregional AI:

| Plane | Function | Examples |
|-------|----------|----------|
| **Knowledge** | Structured memory, evidence, provenance | BKC (KOI protocol, knowledge graphs, entity resolution) |
| **Capital** | Resource flows, commitment pooling, redistribution | GE integration, TBFF, commitment vouchers |
| **Coordination** | Real-time agent collaboration, task routing | A2A protocol, agent swarms |

No single project builds all three planes. BKC owns the knowledge plane and connects to capital and coordination planes through protocol-level integration, not monolithic coupling.

## Why federation, not aggregation

Bioregions are nested. The Greater Victoria landscape group sits within the Salish Sea bioregion, which sits within Cascadia. Knowledge commons should mirror this structure — each node sovereign, each connection chosen.

The alternative — a central knowledge graph that aggregates everything — violates the principle that communities should control what they share, with whom, and under what terms. Federation preserves this by design: each node maintains its own database, identity, and governance. Nodes exchange signed events via the KOI protocol. What travels between nodes is signals, not commands.

This is the cosmolocal principle applied to knowledge infrastructure: light protocols and ontologies shared globally, heavy relationships and governance held locally.

## Design principles

### 1. Protocol, not platform
BKC defines interoperability commitments, not a mandatory stack. The [meta-protocol](./foundations/knowledge-commoning-meta-protocol-v0.1.md) specifies three invariants — what is shared, who attests, who can use it and how — without prescribing KOI, GitHub, or any particular transport. Conformance is graduated (L0 declaration → L1 machine-readable → L2 bidirectional), so adoption never requires all-or-nothing commitment.

### 2. Sovereignty-preserving federation
Every node runs its own KOI deployment with its own database, vault, and identity. Edge-approval governance means nodes explicitly authorize which peers can poll, fetch, or broadcast. Unknown handshakes are deferred, not accepted. The [federation overview](./foundations/federation-overview.md) documents the full protocol and membrane governance model.

### 3. Consent-first data flow
Visibility scoping (public, authorized, node_private) is enforced at the query layer, not as an afterthought. The [data classification matrix](./foundations/data-classification-matrix-v0.1.md) reconciles 34 query sites across 15 public endpoints. Interview artifacts carry consent metadata from the moment of capture.

### 4. Bounded authority
The same pattern recurs at every layer:
- **Knowledge layer**: Steward approval gates what enters the commons (staged → approved → ingested)
- **Capital layer**: Small allocations automated (< $500), larger ones require multisig review
- **Commitment layer**: Commitments verified through evidence before advancement

Authority is always scoped, never unbounded. Governance membranes are structural, not decorative.

### 5. Living system economics
The commitment economy operates through four metabolic functions:
- **Provisioning** (pooling): Commitments aggregate into pools
- **Redistribution** (TBFF): Threshold-based flow funding redistributes value toward need
- **Activation** (network growth): Community practices (workshops, mapping sessions) are the primary growth driver; flow funding supplements but does not replace them
- **Repair** (immune system): Dispute resolution, forkability, and the sufficiency floor — participation in this economy does not cost you your wellbeing

See [commitment-economy-vision.md](./foundations/commitment-economy-vision.md) for the full economic architecture.

### 6. Holonic structure
Nodes nest: leaf nodes (Greater Victoria, Cowichan Valley) within coordinators (Salish Sea) within meta-coordinators (Cascadia). Each level has appropriate scope — local nodes hold dense local relationships, coordinators hold cross-boundary patterns, meta-coordinators hold protocol-level coherence. This mirrors how bioregions actually organize.

## What BKC is not

- **Not a blockchain.** On-chain anchoring (Regen Ledger, Celo EAS) provides proof of existence for claims. The knowledge graph itself lives in PostgreSQL + pgvector.
- **Not a social network.** BKC tracks entities, relationships, evidence, and commitments — not user profiles, feeds, or social graphs.
- **Not a centralized platform.** No single server holds all data. Each node is independent. Federation is opt-in.
- **Not a universal ontology.** The BKC ontology (25 types, 39 predicates) is one reference profile among potentially many. The meta-protocol deliberately avoids mandating a single schema.

## Relationship to other docs

This doc provides the internal canonical vision. Other docs serve different audiences and purposes:

- **[bioregional-swarm-telos.md](./bioregional-swarm-telos.md)**: Coalition-facing framing for partners and build day participants. Includes live status indicators and specific integration seams.
- **[bioregional-ai-swarms-positioning.md](./bioregional-ai-swarms-positioning.md)**: One-pager for Telegram/external sharing. Includes comparison matrix against other projects.
- **[federated-memory-architecture.md](./foundations/federated-memory-architecture.md)**: Canonical technical architecture for the knowledge and retrieval layers.
- **[commitment-economy-vision.md](./foundations/commitment-economy-vision.md)**: Economic architecture for the capital layer, synthesizing Ruddick, CLC, Johar, and RC/KE.
- **[knowledge-commoning-meta-protocol-v0.1.md](./foundations/knowledge-commoning-meta-protocol-v0.1.md)**: Minimum interoperability commitments across all implementations.
