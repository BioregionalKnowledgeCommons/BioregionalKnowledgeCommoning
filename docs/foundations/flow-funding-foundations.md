# Flow Funding Foundations

**Layer:** Pattern Language + Capital Coordination
**Status:** Draft v0.1 — 2026-03-12
**Author:** Darren Zal
**Source context:** Kinship Earth / Bioregional Earth blog; Regenerate Cascadia BioFi program; Hub Cultivator pilot; MycoFi / Mycopunks TBFF protocol; Grassroots Economics / Sarafu heritage

---

## Overview

Flow funding is the capital allocation mechanism that makes bioregional coordination economically generative. Where commitment pooling (see [commitment-pooling-foundations.md](./commitment-pooling-foundations.md)) makes *what we can offer* legible and poolable, flow funding makes *how capital moves* trust-based, subsidiarity-respecting, and knowledge-graph-grounded.

Two versions of flow funding converge on the BKC knowledge graph:

1. **Bioregional Flow Funding** (Hub Cultivator / Regenerate Cascadia) — trust-based, human-mediated: a funder provides capital to a trusted Hub Cultivator who distributes smaller grants to ground-level projects.
2. **Threshold-Based Flow Funding (TBFF)** (MycoFi / Mycopunks) — algorithmic: each participant sets a maximum threshold, and overflow above that threshold redistributes according to weighted allocation preferences.

Both versions share a core insight: capital should flow like water through a watershed — from abundance to need, governed by trust relationships and ecological context, not institutional gatekeepers.

---

## 1. Why Flow Funding — and Why Now

BKC's Capital Plane has commitment pooling (C0 live) and claims engine integration (steel thread proven). The missing piece is the mechanism that actually moves capital through the system. Flow funding fills this gap with two complementary approaches:

- **Hub Cultivator** provides the trust infrastructure and governance scaffolding — who is trusted to allocate, what reporting looks like, how decisions are made at the most local level.
- **TBFF** provides the algorithmic mechanism — once trust relationships and thresholds are established, overflow redistribution happens automatically, with full on-chain provenance.

The BKC knowledge graph is the shared substrate: both versions read from it (evidence for decisions) and write back to it (decision receipts as Evidence entities with CAT receipt chains).

---

## 2. Two Versions Compared

| | Bioregional Flow Funding | TBFF |
|---|---|---|
| **Governance** | Trust-based, human steward decisions | Algorithmic, threshold overflow redistribution |
| **Core mechanism** | Funder → Hub Cultivator → small grants to projects | `x' = min(x, t) + P^T · max(0, x - t)` — iterate until convergence |
| **Financial infrastructure** | DAFs (Donor-Advised Funds) | Superfluid CFA streaming on Base |
| **Reporting** | 4 reflective questions (annual): *What inspired you? What surprised you? What challenged you? What moved you?* | On-chain settlement events with full balance snapshots |
| **Decision authority** | Hub Cultivator steward (human judgment) | Allocation preferences matrix (set by participants, executed by contract) |
| **Convergence** | Continuous relational process | Mathematical: typically 1–4 iterations |
| **Originators** | Kinship Earth, Earth Regeneration Fund, Regenerate Cascadia | MycoFi / Mycopunks collective |
| **Pilot scope** | 6 bioregions (Cascadia, Barichara, NE Forests, Tkaronto, Northern Andes, Ogallala) | 5 Mycopunks members (Victoria-based experiment) |
| **BKC integration** | Steward decision logging via `/ingest` → Evidence entities | Settlement evidence via dedicated endpoint → Evidence entities |

---

## 3. Philosophical Pillars

### 3.1 Trust as Infrastructure

Flow funding inverts conventional philanthropy. Rather than institutional due diligence filtering who receives funds, trust relationships *are* the infrastructure. As Kinship Earth articulates: "the very people who are most connected to their land and communities — the ones with the most knowledge and direct experience — are the least likely to receive funding" through traditional channels.

Hub Cultivators embody this: they are trusted community members who know the landscape, the projects, and the people. Their judgment is the allocation mechanism. TBFF formalizes trust into allocation preferences: each participant explicitly declares where their overflow should go, encoding trust relationships as weighted edges in a graph.

Both approaches build trust into the BKC knowledge graph as first-class data: Hub Cultivator decisions become Evidence entities; TBFF allocation preferences become queryable graph relationships.

### 3.2 Subsidiarity — Decisions at the Most Local Level

Capital allocation decisions should be made by the people closest to the work. The Hub Cultivator model embeds this directly — stewards allocate within their landscape, not from a central office. TBFF achieves the same through participant-set thresholds and preferences: each node in the network decides its own capacity limit and where excess should flow.

This mirrors BKC's holonic architecture: leaf nodes (bioregion scale) make local decisions; coordinators aggregate signals across boundaries. Capital flows follow the same nested pattern.

### 3.3 The Watershed Metaphor

Capital flows like water through a watershed. The TBFF protocol makes this explicit with its threshold mechanism: a "lake level" (maximum threshold) defines when a participant is "full," and overflow flows downhill to connected recipients. The Hub Cultivator model uses the same metaphor at landscape scale: capital enters through funders, flows through trusted cultivators, and irrigates ground-level projects.

Regenerate Cascadia's BioFi infrastructure maps directly: landscape-level regeneration teams → ecoregional coordination → bioregional aggregation. Capital flows through these nested governance channels "like water through a watershed."

### 3.4 Transparency Through Knowledge Graph, Not Metrics

Both versions reject metrics-heavy reporting in favor of knowledge-graph-grounded transparency. Hub Cultivator reporting asks four reflective questions — narrative, not numeric. TBFF transparency comes from on-chain settlement events — mathematically verifiable, not self-reported.

The BKC knowledge graph provides a third path: provenance-tracked Evidence entities linked to specific projects, decisions, and outcomes. Transparency emerges from the graph structure (who funded what, based on what evidence, with what result) rather than compliance reports.

---

## 4. Landscape Hub Cultivator Context

### 4.1 The Program

The Landscape Hub Cultivator (LHC) is a 2025–26 pilot program supporting up to 10 Regenerate Cascadia landscape groups across the Cascadia bioregion. It builds the governance infrastructure that makes bioregional flow funding operational.

**Phase 1 (first 6 months):** Groups develop place-based regeneration strategies — bioregional mapping, nested place scales, stewardship levels. Participants co-create project portfolios with budgets and storytelling materials.

**Phase 2 (second 6 months):** Core team development, fundraising strategies, governance models, community consent processes, bioregional carrying capacity assessment, and local funding ecosystem building.

### 4.2 Landscape Hub Features

Established hubs feature:
- Funded regeneration teams (minimum three dedicated stewards)
- Active local and bioregional fundraising participation
- Maintained project portfolios and regeneration strategies
- Watershed-scale monitoring and context-based indicators
- Participation in bioregional forums and financing facilities
- Experimental governance structures managing funding flows

### 4.3 Victoria Group

Darren Zal stewards the Victoria group in the Landscape Hub Cultivator program. This positions BKC as both the knowledge infrastructure *and* a direct participant in the flow funding pilot — not an external platform, but a practicing node in the network.

The Victoria group's participation means Hub Cultivator decisions can be immediately logged as Evidence entities in the BKC knowledge graph, creating the first real-world capital-loop proof.

### 4.4 Kinship Earth and the Six Bioregions

Kinship Earth / Earth Regeneration Fund launched flow funding in September 2024 across six pilot bioregions: Barichara, Cascadia, Forests of the NE, Greater Tkaronto Bioregion, Northern Andes, and Ogallala. Each bioregion has its own Hub Cultivator structure. Cascadia's implementation through Regenerate Cascadia is the most directly connected to BKC infrastructure.

Community-led conservation through this model proves "2.5 times more cost-effective" than traditional approaches, with "50% higher success rates" due to local knowledge and ownership.

---

## 5. TBFF Technical Model

### 5.1 The Algorithm

TBFF uses iterative threshold-based redistribution:

```
x^(k+1) = min(x^(k), t) + P^T · max(0, x^(k) - t)
```

Where:
- **x^(k)**: participant balance vector at iteration k
- **t**: maximum threshold vector (the "lake level" per participant)
- **P**: allocation preferences matrix (n×n, rows sum to 1.0)
- **P^T**: transpose — overflow *arrives at* recipients
- **min(x, t)**: cap each balance at threshold
- **max(0, x - t)**: compute overflow above threshold

**Plain English:** Cap each participant's balance at their threshold, distribute the overflow to their chosen recipients according to weighted preferences, repeat until no one is above threshold. Typically converges in 1–4 iterations. Total funds are conserved (no inflation, no leakage when weights sum to 1.0).

### 5.2 On-Chain Implementation

- **Chain:** Base Sepolia (testnet), targeting Base mainnet
- **Streaming:** Superfluid CFA v1 (Constant Flow Agreement) — continuous token streams, not discrete transfers
- **Contracts:** `TBFFMath.sol` (pure math library, WAD arithmetic) + `TBFFNetwork.sol` (on-chain controller with `settle()` function)
- **Gas profile:** ~4.2K per node (2 allocations each). 5 nodes ≈ 21K gas, 50 nodes ≈ 208K gas.
- **Flow rate:** `targetRate = overflow × weight / streamEpoch` (default 30-day epoch)

### 5.3 TypeScript Reference Engine

A mirror implementation in TypeScript (`tbff-protocol/web/src/lib/tbff/engine.ts`) provides:
- Identical algorithm for cross-validation against Solidity
- Browser simulator with real-time visualization
- Test suite (32 tests) covering linear chains, circular allocations, diamond graphs

### 5.4 Mycopunks Experiment

Five Mycopunks members (including Darren) experiment with TBFF in Victoria and beyond. The initial scenario: $32K across 5 participants, $8K max thresholds each. Christina starts above threshold, triggering immediate redistribution through the allocation graph.

---

## 6. Integration Architecture

### 6.1 Read Path — Knowledge Graph to Decisions

Both versions read from the BKC knowledge graph to inform allocation decisions:

- **Hub Cultivator:** Entity search + `/chat` for decision support. "What projects in Victoria need watershed monitoring support?" → Evidence-backed suggestions.
- **TBFF:** Participant thresholds and allocation preferences can reference BKC entities. A project's needs assessment (stored as Evidence) informs whether threshold should increase.

### 6.2 Write Path — Decisions to Knowledge Graph

Both versions write back to the knowledge graph as Evidence entities with CAT receipt chains:

**Hub Cultivator write-back:**
```
Steward decision → /ingest with hub-cultivator: prefix
  → Evidence entity (who, what, how much, rationale)
  → CAT receipt (entity_ingest type, chained to parent)
  → Knowledge graph (queryable, federable)
```

**TBFF write-back:**
```
settle() event → POST /claims/evidence-from-settlement
  → Evidence entity (settlement snapshot, balances, iterations)
  → CAT receipt (tbff_settlement type, chained)
  → Knowledge graph (queryable, federable)
```

### 6.3 Bridge — Commitment Pools

Commitment pooling (C0 live) is the bridge between flow funding versions:

- Hub Cultivator participants' pledges become commitment pool entries (`pledges_commitment` predicate)
- TBFF settlements can prove commitment fulfillment (`proves_commitment` predicate)
- Pool activation can be triggered by either human steward verification (Hub Cultivator) or cumulative TBFF settlement evidence exceeding a threshold (C1 planned)

```
Track 1: Hub Cultivator          Track 2: TBFF
(human-mediated, DAFs)           (algorithmic, Superfluid)
         \                          /
          \   Shared Infrastructure /
           \  (CAT receipt chain)  /
            \       |             /
             v      v            v
         BKC Knowledge Graph
        (Evidence + Receipts)
                 |
          Commitment Pools
         (C0 live, C1 planned)
```

---

## 7. Adoption Pathway

### Track 1 — Hub Cultivator (Immediate)

**Now:** Darren logs Victoria Hub Cultivator decisions as Evidence entities via `/ingest`. Each decision creates a receipt chain linking steward → project → amount → rationale.

**30 days:** Victoria Landscape Hub entities seeded in knowledge graph. Decision helper script wraps `/ingest` with Hub Cultivator conventions (deterministic RIDs, standard relationships).

**60 days:** When Kinship Earth's annual reflective questions come due, Evidence entities are already anchored with full provenance. Reporting becomes a graph query, not a form.

### Track 2 — TBFF (Experimental)

**Now:** TBFF protocol deployed on Base Sepolia with simulator. Mycopunks experiment with threshold settings and allocation preferences.

**30 days:** `POST /claims/evidence-from-settlement` endpoint bridges settlement events to BKC Evidence entities with receipt chains.

**60 days:** First real settlement cycle through knowledge graph. Settlement evidence linked to commitment pool entries.

### Convergence (C1+)

**90 days:** Commitment pool threshold gates activated by both human decisions and algorithmic settlements. Hub participants' pledges and TBFF settlements both contribute to pool activation conditions.

---

## 8. Relationship to Commitment Pooling

Flow funding and commitment pooling are complementary layers of the Capital Plane:

- **Commitment pooling** answers: *What can we offer?* Communities make capacity legible and poolable.
- **Flow funding** answers: *How does capital move?* Trust relationships and thresholds govern allocation.

The connection is direct: commitment pool entries represent pledged capacity; flow funding mechanisms allocate capital to fulfill those commitments. Evidence entities from flow funding decisions prove commitment fulfillment (`proves_commitment` predicate), advancing commitments through the state machine (VERIFIED → ACTIVE → EVIDENCE_LINKED → REDEEMED).

See [commitment-pooling-foundations.md](./commitment-pooling-foundations.md) for the commitment lifecycle, state machine, and Grassroots Economics heritage.

---

## 9. References

- Kinship Earth / Bioregional Earth: [bioregionalearth.org/blog/flow-funding](https://www.bioregionalearth.org/blog/flow-funding)
- Regenerate Cascadia BioFi: [regeneratecascadia.org/biofi/bioregional-funding/](https://regeneratecascadia.org/biofi/bioregional-funding/)
- Hub Cultivator program: [regeneratecascadia.org/hub-cultivator/](https://regeneratecascadia.org/hub-cultivator/)
- TBFF protocol: [github.com/LinuxIsCool/tbff-protocol](https://github.com/LinuxIsCool/tbff-protocol)
- Grassroots Economics / Sarafu: [grassrootseconomics.org](https://grassrootseconomics.org)
- BKC commitment pooling: [commitment-pooling-foundations.md](./commitment-pooling-foundations.md)
- BKC ontology: `Octo/ontology/bkc-ontology.jsonld` (v1.2.0)
- CAT receipt system: `koi-processor/api/cat_receipts.py`
