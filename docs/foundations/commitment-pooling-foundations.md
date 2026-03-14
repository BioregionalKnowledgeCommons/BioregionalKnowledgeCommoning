# Commitment Pooling Foundations

**Layer:** Pattern Language + Capital Coordination
**Status:** Draft v0.1 — 2026-03-03
**Author:** Darren Zal
**Source context:** Grassroots Economics Sarafu network; CLC DAO specification; Will Ruddick Substack

---

## Overview

Commitment pooling is the missing economic primitive for bioregional coordination. Where knowledge commoning makes *what we know* legible and routable across communities, commitment pooling makes *what we can offer and do* legible and poolable.

This document establishes the philosophical foundations, technical model, integration seams, and governance guidance for adding commitment pooling as a first-class layer in the Bioregional Knowledge Commons.

---

## 1. Why Commitment Pooling — and Why Now

BKC was named for *knowledge* commoning, but the deeper vision — articulated across the three-plane architecture — is about **economic and ecological coordination at bioregional scale**. The Knowledge Plane (live) and Coordination Plane (A2A, Clawsmos) are operational. The Capital Plane remains thin: currently only TBFF evidence-to-allocation bridging and planned Hypercerts.

Commitment pooling fills this gap without adding financialization. It inverts conventional finance: rather than allocating scarce currency *to* communities, communities make their **capacity and obligations legible** *as* a pooled commons. Value arises from trusted redeemability, not external price signals.

**The operational precedent is real.** The Sarafu Network (Grassroots Economics, Kenya, deployed on Celo mainnet since July 2023) has 26,367 users, 188 active commitment pools, 745 active vouchers, and $320,692 in swap volume ([Dune dashboard](https://dune.com/grassrootseconomics/sarafu-network)). Over 1,200 acres restored and 84% positive income impact in pilot regions. This is not speculative — commitment pooling is a practiced economic technology.

---

## 2. Philosophical Pillars

### 2.1 Axiology: Value as Trusted Capacity

Commitment pooling grounds value in **trusted capacity to deliver**, not market price. A commitment to "10 hours of watershed monitoring" has value because the community trusts the pledger. Price emerges from verified redeemability, not speculation.

This aligns with BKC's knowledge ontology: both knowledge commons and commitment pools value things by their *verified, contextual trustworthiness* — not by external market signals.

### 2.2 Ontology: Commitments as First-Class Entities

Commitments are not side-effects of economic activity — they are the primary unit. A pledge has states, proofs, and provenance. BKC's entity model extends naturally: `Commitment` and `CommitmentPool` join `Evidence` and `Claim` as first-class knowledge graph entities with lifecycle states and ECDSA-signed federation.

The knowledge-economy homology is exact: BKC is *already* a commitment pool for knowledge curation. Members pledge to curate, attest, and maintain knowledge. Extending to economic commitments is the same pattern at a different layer.

### 2.3 Epistemology: Verification Builds Shared Knowledge

Community verification of commitments builds shared knowledge of *who can offer what*. Will Ruddick calls this the "mycelial network" of commitment pooling — exactly the same metaphor used for BKC's knowledge commons network. Vouching for a commitment pledge is epistemically identical to attesting to a knowledge entity: both build the community's knowledge graph.

### 2.4 Praxis: The Commitment Lifecycle

The operative sequence is:

```
Pledge → Verify → Pool → Circulate → Redeem → Prove with Evidence
```

Each step is an observable event, storable in the knowledge graph, and raisable to federation via KOI-net commitment events. This is the same pipeline as the web ingest pipeline: observe → extract → verify → store → federate.

---

## 3. Technical Model

### 3.1 Three Tiers (Sarafu / CLC DAO architecture)

**Tier 1 — Individual Level:** A Person or Organization issues a commitment pledge (analogous to a Community Asset Voucher / CAV): "I commit to X hours of Y service." Stored as a `Commitment` entity with `PROPOSED` state.

**Tier 2 — Pool Federation:** Multiple commitments aggregate into a `CommitmentPool`. When a threshold of pledges are verified, the pool activates. Credits (abstracted commitment capacity) route multi-hop across pools via trust links. This is the CLC model (deployed on Celo mainnet), turning the "long tail of real obligations" — labor, land stewardship, knowledge curation — into routable economic signals.

**Tier 3 — Ecosystem Governance:** DAO or governing body sets safety rules, routing standards, and insurance. In BKC's model, this maps to the existing commons governance membrane (decision audit log, steward approval flows, policy governance).

### 3.2 State Machine

```
PROPOSED ──steward review──▶ VERIFIED ──pool threshold──▶ ACTIVE
    │                            │                           │
    ▼                            ▼                           ▼
REJECTED                     WITHDRAWN               EVIDENCE_LINKED
                                                           │
                                                    ──Evidence──▶ REDEEMED
                                                           │
                                                        DISPUTED──▶ RESOLVED
```

Every state transition is recorded in `commitment_state_log` (insert-only, mirrors `koi_commons_decisions` audit pattern).

### 3.3 Demurrage (Optional)

A 2% monthly decay on unredeemed commitment capacity encourages use, returns unused capacity to community reserves, and prevents hoarding. BKC's implementation: configurable per-pool via `demurrage_rate_monthly`. **Default is 0** (disabled) — appropriate for early-stage bioregional pilots where coordination rhythms are still forming. Bioregions should activate demurrage only when pool cycles are well-established.

### 3.4 Entity Types and Predicates

New ontology additions (see `Octo/ontology/bkc-ontology.jsonld` v1.1.0):

| Entity Type | Description | Analogous To |
|---|---|---|
| `Commitment` | Formal pledge to deliver goods, labor, or service | CAV in Sarafu |
| `CommitmentPool` | Aggregation of commitments by a community | Sarafu pool |
| `CommitmentAction` | A recorded act of partial or full fulfillment | Mweria cycle entry |

New predicates:

| Predicate | From → To | Meaning |
|---|---|---|
| `pledges_commitment` | Person/Org → Commitment | Who made the pledge |
| `aggregates_commitments` | CommitmentPool → Commitment | Pool contains pledge |
| `proves_commitment` | Evidence → Commitment | Evidence verifies fulfillment |
| `redeems_via` | Commitment → Evidence | Path from pledge to proof |
| `governs_pool` | Organization/Bioregion → CommitmentPool | Pool stewardship |
| `disputes` | Person/Org → Commitment | Formal dispute entry |

---

## 4. Integration Seams

### 4.1 TBFF Bridge (extend)

The existing TBFF Evidence write-back loop creates `Evidence` entities from capital flow decisions. New seam: Evidence entities can now reference which `Commitment` pledge they fulfill via `proves_commitment`. A single TBFF allocation can prove multiple commitment pledges.

### 4.2 owockibot (extend, C1)

CommitmentPool activation thresholds become owockibot trigger events. Instead of pure Evidence triggers: "Pool X has reached 80% verified pledge threshold" → owockibot proposes allocation (≤$500 auto) or escalates to multisig. This makes commitment pooling the *trigger* for capital flow, not just a parallel system.

### 4.3 co-op.us Task Pipeline (extend, C1)

Task completion → Evidence entity → `proves_commitment` → EVIDENCE_LINKED state. Task bounties become commitment offers: the worker pledges delivery, the pool activates when threshold met, co-op.us task completion writes Evidence, commitment is redeemed.

### 4.4 KOI-net Federation (C2)

New KOI-net event types for cross-node commitment exchange:

```
commitment.proposed   — pledge submitted at a leaf node
commitment.verified   — steward approved at origin node
commitment.pooled     — commitment joined a pool
commitment.redeemed   — Evidence linked, commitment fulfilled
```

All events use the existing ECDSA-signed envelope format. Federated pools aggregate commitments across bioregion boundaries for meta-regional coordination.

### 4.5 Grassroots Economics / Sarafu (C2 — external)

Phase 1 (now): Reference model study. This document.
Phase 2 (C1): Protocol compatibility analysis — CIC Stack ↔ KOI-net event format.
Phase 3 (C2): CLC DAO bridge spike — route BKC commitment events into CLC's multi-hop routing layer.

The CLC DAO's Nondominium governance model maps cleanly to BKC structure:
- **General Members** (distributed oversight) → BKC community/bioregion members
- **Service Providers** (day-to-day operations) → BKC stewards
- **Guardians** (conflict arbitration) → Pilot charter signatories (Front Range + Cascadia)

---

## 5. Governance Guidance

### 5.1 Sangat-Grade Requirements

Indy Johar's framework for commitment infrastructure requires three properties:

| Property | BKC Implementation |
|---|---|
| **Commitment** (durable obligation) | `commitments` table with insert-only state log |
| **Memory** (shared contestable provenance) | `commitment_state_log` + CAT receipt chain + KOI-net events |
| **Contestability** (legible, revisable governance) | `disputes` predicate + DISPUTED → RESOLVED transition + commons governance membrane |

BKC already has all three architecturally. Commitment pooling is the economic manifestation of infrastructure that's already there.

### 5.2 Consent and Rights

Commitment pledges carry consent implications. Before deploying a commitment pool:

1. **Pledger consent:** Pledger must understand the pool activation conditions, demurrage policy (if any), and redemption process.
2. **Dispute rights:** Any party can invoke the `disputes` predicate to formally contest a commitment. Dispute resolution follows the commons governance membrane.
3. **Data class:** Commitment data (pledger identity, offer details) carries `sensitive` data class by default. Cross-node federation of individual commitment details requires explicit steward opt-in.

### 5.3 Pattern Language Alignment

Commitment pooling instantiates existing BKC patterns:

- **Participation Pattern:** Commit to deliver, not just observe. Pool participation is contribution.
- **Consent Boundary Pattern:** Pool membership and data sharing require explicit pledger consent at each scope.
- **Emergent Bridging Pattern:** Individual bioregion pools aggregate into meta-regional pools via trust links.
- **Holonic Nesting Pattern:** Leaf-node pools (bioregion scale) nest into coordinator pools (meta-regional scale), mirroring the KOI-net federation topology.

### 5.4 Adoption Pathway (30/60/90 days post-C0)

**30 days (C0 — done):** Commitment entity types in ontology. Registry API live. Stewards can create pledges and verify them via governance membrane.

**60 days (C1):** Pool mechanics live. Threshold activation. TBFF threshold policy extended to include commitment activation gates. First pilot pool created (target: Regenerate Cascadia or co-op.us).

**90 days (C2):** Cross-node pool aggregation via KOI-net. Hypercerts minted from REDEEMED commitments. GE protocol compatibility analysis complete.

---

## 6. Why This Isn't Just ReFi

Commitment pooling is often misread as another tokenization scheme. It is the opposite.

ReFi tokenizes *future value* (speculative). Commitment pooling makes *prior obligations* (capacity, labor, stewardship already being performed) legible as economic signals. The Sarafu network's 84% positive income impact and 1,200 acres restored demonstrate real-world grounding in actual community labor and ecological work, not speculation.

The Grassroots Economics philosophy is explicit: "changing the world's economic systems will not be affordable within the world's current economic system." Commitment pooling is lived practice, not a grant-funded project. BKC bioregional stewards should become commitment pool *practitioners*, not just administrators of a system.

**Cosmo-local intelligence** (Ruddick): "Type I civilization requires better coordination, not just more tech." BKC's multi-node federation, A2A discovery, and ontology-grounded RAG are coordination infrastructure. Commitment pools are how that coordination becomes economically generative — locally rooted, globally interoperable.

---

## 7. Three Orthogonal Operations: Create, Pledge, Verify

Commitment pooling governance rests on three independent operations that compose freely. This decomposition draws on Will Ruddick's three-layer model (individual → pool → ecosystem) and the SPROUT License's peer-curation principles.

### 7.1 Create — Self-Sovereign Promise Issuance

Anyone can make a promise. A Person or Organization creates a commitment with typed offers, wants, limits, and routing metadata. No gatekeeper reviews creation — the commitment enters the graph in `PROPOSED` state and is immediately visible (subject to visibility scope).

**Principle:** Commitments are self-sovereign. The right to promise is not granted by a pool or a steward. This mirrors CAV issuance in the Sarafu model: a community voucher is issued by its creator, not approved into existence.

**Visibility scope applies regardless of state.** A `node_private` commitment is invisible to unauthorized consumers whether it is PROPOSED, VERIFIED, ACTIVE, or REDEEMED. Visibility is orthogonal to lifecycle state.

### 7.2 Pledge — Peer-Curated Pool Acceptance

Pool stewards curate which commitments belong in their pool via `POST /pools/{rid}/pledge`. Pledging is a curation act: "this commitment fits our pool's purpose and bioregion." It is not approval or verification — a PROPOSED commitment can be pledged before anyone has verified it.

**Principle:** The question is not "is this commitment allowed?" but "which pools accept it?" This follows the SPROUT License (§3.5) peer-curation model: inclusion is earned through relevance and steward judgment, not central approval.

Declining a pledge is implicit — the commitment is simply not pledged to that pool. In hackathon MVP, the system is single-pool. Multi-pool pledging (a commitment in multiple pools simultaneously) is a post-hackathon extension.

### 7.3 Verify — Trust Attestation Through Witnessed Follow-Through

Verification is an independent trust signal: a steward or peer attests that the pledger can deliver. `PATCH /commitments/{rid}/state` (PROPOSED → VERIFIED) records who verified and when.

**Principle:** Trust emerges from witnessed follow-through, not pre-approval. A commitment can be VERIFIED without being in any pool (verified but uncurated), or pledged to a pool without being verified (curated but unverified). Verification and curation serve different social functions — conflating them creates bottlenecks.

### 7.4 Orthogonality

The three operations are independent along every axis:

| | Create | Pledge | Verify |
|---|---|---|---|
| **Actor** | Pledger (self-sovereign) | Pool steward (peer curator) | Steward or peer (trust attester) |
| **Gate** | None | Pool governance | Community trust |
| **Can happen without the others** | Yes | Yes (commitment can be pledged while PROPOSED) | Yes (commitment can be verified without any pool) |
| **Reversible** | No (append-only; can WITHDRAW) | Yes (remove from pool) | No (append-only audit trail) |

This decomposition prevents a single steward from becoming a gatekeeper to the entire lifecycle. Each operation has its own authority, its own social contract, and its own audit trail.

### 7.5 Forkability as Safety Valve

If a pool's curation standards diverge from community values, any steward can fork the pool: create a new pool and pledge the commitments they trust into it. The original commitments are unaffected (they exist independently of any pool). This is the antidote to possessive stewardship — authority over a pool is earned by curation quality, not granted by position.

Forkability is only meaningful when commitments exist independently of pools. The three-operation decomposition makes this possible: because Create is self-sovereign and Pledge is a separate curation act, commitments survive pool governance failures.

### 7.6 Runtime Note

The current runtime is single-pool MVP. Multi-pool pledging, cross-pool routing, and federated pool forking are post-hackathon extensions (C1/C2). The governance model is designed for the multi-pool future even though the hackathon implementation is simpler.

---

## 8. References

- Grassroots Economics: [grassrootseconomics.org](https://grassrootseconomics.org)
- Sarafu Network documentation: [docs.grassrootseconomics.org](https://docs.grassrootseconomics.org)
- CLC DAO: [Celo forum post](https://forum.celo.org/t/introducing-clc-dao-credit-routing-for-the-long-tail-of-real-world-commitments-on-celo/12910)
- Indy Johar, "Sangat-grade infrastructure": Dark Matter Labs research (2025)
- Will Ruddick, "Touching the Knowledge Commons": [Substack](https://grassrootseconomics.substack.com)
- BKC ontology: `Octo/ontology/bkc-ontology.jsonld` (v1.1.0)
- Commitment API: `Octo/koi-processor/api/routers/commitment_router.py`
- DB migrations: `056_commitment_registry.sql`, `057_commitment_pools.sql`
- Roadmap: `docs/roadmap/semantic-roadmap.json` (C-series nodes)
