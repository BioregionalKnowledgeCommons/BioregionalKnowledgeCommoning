# CLC Questions Synthesis

**Date:** 2026-03-14
**Status:** Working draft
**Source:** Deep reading of [CLC White Paper](https://cosmolocal.credit) + BKC architecture analysis
**Depends on:** [clc-integration-strategy.md](./clc-integration-strategy.md), [commitment-pooling-foundations.md](../foundations/commitment-pooling-foundations.md)

---

## Purpose

Formalized Q&A from CLC whitepaper analysis. Each section: question, BKC's working answer, concrete integration point, and open questions. Designed to be shareable with the Grassroots Economics team for alignment.

**Canonical source hierarchy:**
- `CLC_whitepaper_notes.md` (pilots/celo-hackathon-2026/) = raw notebook / thinking-in-progress
- This document = canonical refined synthesis with authoritative working answers
- `vision.md` (pilots/celo-hackathon-2026/) = sprint-facing framing that references this synthesis

---

## 1. BKC + CLC Layering

**Question:** How do BKC and CLC relate architecturally? Are they competing systems?

**Working answer:** They are complementary layers, not competing implementations. BKC provides off-chain curation and routing intelligence. CLC provides on-chain settlement and execution. The three-layer stack:

| Layer | System | Role |
|-------|--------|------|
| **Knowledge and curation** | BKC | Place-based memory, steward identity, proof, governance membrane, routing intelligence |
| **Planning semantics** | Future (ValueFlows/hREA) + [Intent Publication](./intent-publication.md) | Intents, plans, recipes, dependencies, process logic. The intent publication proposal partially fills this layer with typed WANT/OFFER/CONDITIONAL intents and agent-mediated matching — bridging the gap between BKC curation and CLC settlement without requiring full VF/hREA. |
| **Settlement and execution** | CPP/CLC | Pooled redeemable commitments, liquidity, routing, multi-hop settlement |

Not every BKC commitment becomes pooled. BKC holds the wider field — intents, offers, needs, proofs, social context, ecological knowledge. Commitment pools hold the curated subset that pool stewards consider mature, redeemable, and bounded enough for settlement.

**Integration point:** BKC's routing scorer outputs semantic pool suggestions (bioregion fit, tag overlap, capacity). CLC's `SwapRouter` executes multi-hop `Hop[]` paths. BKC selects *which* sequences to quote; CLC executes the settlement.

**Open questions:**
- What is the minimum metadata CLC pools need from BKC to make routing decisions?
- Should BKC maintain a shadow of CLC pool state (liquidity depth, swap volume) for routing?

---

## 2. Confederation Strategy

**Question:** Should BKC/Cascadia join the CLC DAO, fork the protocol, or build its own network profile?

**Working answer:** These aren't mutually exclusive, and the answer changes over time:

- **Near-term:** Designed toward CPP compatibility. Study CLC's token graph, quoter models, and registry patterns. Build the semantic-to-contract translation layer.
- **Medium-term:** Integrate with CLC DAO as a participant or portfolio profile. Use shared routing and liquidity infrastructure while maintaining BKC's governance membrane.
- **Long-term:** If Cascadia develops enough volume, governance needs, and routing preferences, evolve into an independent but interoperable network profile within CLC's confederation architecture.

CLC §5.2a directly addresses this: "CLC is designed as a confederation protocol: many independent networks can run their own registries, routers, and policy layers, while still routing to one another when they share compatible vouchers and standards." AGPL licensing ensures improvements to shared plumbing remain shareable. The "why not just fork?" question has a clear answer — forking is encouraged, and compatibility is rewarded with routing access.

**Integration point:** BKC's KOI-net federation (domain events, edge approval, handshake deferral) maps to CLC's confederation mechanics (multi-profile discovery, reciprocal routing, mutual allowlists). Both use consent-gated peer trust.

**Open questions:**
- At what volume/complexity threshold does an independent network profile become worth the infrastructure overhead?
- What does "CPP-compatible" mean concretely for BKC's routing scorer output format?

---

## 3. Portfolio Pools as Bioregional Financing

**Question:** Do CLC portfolio pools map to bioregional financing? Is being a liquidity provider the same as underwriting a local network of projects?

**Working answer:** The mapping is strong. Bioregional financing aims to invest in ecosystems and networks rather than isolated projects. CLC portfolio pools are curated pools of commitments "aligned to a mission domain (e.g. ecosystem support services, humanitarian support, health & wellness)" — exactly the portfolio approach bioregional financiers describe.

Landscape groups are proto-portfolio pools:
- **Place-based** — scoped to a watershed, bioregion, or landscape
- **Steward-curated** — listing policy defined by local stewards who know the community
- **Ecologically scoped** — commitments aligned to restoration, food systems, care, or watershed work
- **Portfolio-directed** — liquidity providers target real-world outcomes without requiring a single central issuer

Being a liquidity provider to a portfolio pool is a form of bioregional financing — not extractive VC, but underwriting settlement capacity, confidence, and resilience for a mission-aligned local portfolio.

**Integration point:** BKC pool stewards define listing policy. BKC routing scorer recommends commitments for pools. CLC portfolio pool infrastructure handles liquidity, routing, and settlement. BKC proof packs provide the accountability layer funders need.

**Open questions:**
- What listing policy templates would landscape group stewards actually use?
- How does portfolio pool liquidity provision interact with TBFF threshold-based flow funding?

---

## 4. Proof Packs as Attestation Layer

**Question:** Can BKC proof packs become the attestation layer CLC portfolio pools use for listings, haircuts, and insurance qualification?

**Working answer:** CLC §7.3.2 defines two attestation patterns for portfolio pools:

- **Attestation Certificates** — a verifier issues an attestation that a voucher issuer meets stated criteria. Pools use attestations to whitelist listings, adjust haircuts, widen/narrow limits, or qualify for insurance.
- **Audit/Verification Service Vouchers** — redeemable tokens representing verification services.

BKC proof packs already contain: evidence chain, peer attestations, state transitions, content hashes, Regen Ledger anchor, and verification instructions. This maps directly to Attestation Certificates — with the advantage that BKC proof packs are archivable, content-addressed, and independently verifiable.

Potential uses in CLC context:
- **Listings** — proof pack demonstrates commitment has been verified, informing pool steward listing decisions
- **Haircuts** — commitments with strong proof histories get favorable terms; unproven commitments get wider haircuts
- **Insurance** — proof pack history contributes to risk assessment for CLC insurance fund participation
- **Routing** — proof-backed commitments could receive routing preference (higher settlement probability)

**Integration point:** `GET /claims/{rid}/proof-pack` returns the archivable JSON artifact. Format alignment with CLC attestation certificate schema is needed — specific fields, signing format, and registry lookup.

**Open questions:**
- What is the minimum attestation format CLC pools accept?
- Does CLC have a registry for attestation providers? Would BKC nodes register as attestation providers?
- How should proof pack content hashes relate to CLC's on-chain audit trail?

---

## 5. Multi-Objective Routing

**Question:** CLC optimizes for settlement velocity. What else should routing optimize for in a bioregional context?

**Working answer:** CLC's stated north star is "maximize the velocity of settlement of outstanding commitments while preserving care, fairness, and resilience." BKC adds contextual factors that make routing ecologically and socially relevant, not just economically efficient:

| Routing factor | Source | Status |
|---------------|--------|--------|
| **Bioregion proximity** | BKC knowledge graph (entity relationships) | Live in scorer |
| **Taxonomy overlap** | BKC ontology (semantic tag matching) | Live in scorer |
| **Timeframe alignment** | BKC commitment metadata (validity windows) | Live in scorer |
| **Capacity fit** | BKC pool metadata (remaining capacity) | Live in scorer |
| **Ecological urgency** | Community mapping, steward assessment | Not yet modeled |
| **Reciprocity** | Historical fulfillment patterns between communities | Not yet modeled |
| **Carrying capacity** | Bioregional limits on extraction/commitment | Not yet modeled |
| **Seasonal fit** | Time-dependent appropriateness of commitment fulfillment | Not yet modeled |

The key insight: CLC routes by token-pair adjacency across pool graphs. BKC routes by semantic fit across knowledge graphs. Combined, they provide multi-objective routing — economic efficiency *and* ecological/social relevance.

**Integration point:** BKC scorer output + CLC `SwapRouter.quoteExactInput()` = combined score. The scorer ranks pools by semantic fit; the router quotes viable `Hop[]` paths; the agent presents options ranked by both dimensions.

**Open questions:**
- How should routing objectives be weighted? Fixed weights, steward-configured, or community-governed?
- Can CLC's batch netting / rebalancing layer incorporate BKC routing preferences? **Partially answered:** The [intent publication proposal](./intent-publication.md) describes how user intents become "virtual edges" in the clearing graph, allowing batch netting to optimize for user needs (not just pool inventory). This is the mechanism by which BKC routing preferences enter the netting layer.
- How do missing factors (urgency, reciprocity, carrying capacity) get modeled — ontology extension, scoring plugin, or community input?

---

## 6. Time-Aware Planning

**Question:** How should commitment routing handle seasonality, dependency sequencing, and future settlement windows?

**Working answer:** BKC already has validity windows and timeframe scoring in the routing scorer. But the current model is relatively simple — a commitment has a start date and end date, and the scorer checks alignment. Richer time-awareness is needed:

- **Seasonal routing** — mycoremediation commitments route differently in spring vs. winter; native plant nursery output has growing seasons
- **Dependency sequencing** — "agroforestry management" depends on land access, tools, collaborators, nursery stock. Some commitments can't be fulfilled until prerequisites are met.
- **Cascade scheduling** — a series of related commitments could be scheduled to execute in sequence, maximizing cumulative value

CLC has relevant primitives: expiry flags on GiftableTokens, per-epoch caps on swaps, batch netting with standing constraints. But these are enforcement mechanisms, not planning tools.

This points toward the planning semantics layer (ValueFlows/hREA) between BKC and CLC:
- BKC = what exists, who stewards it, what's been proven
- ValueFlows = intents → plans → recipes → processes → dependencies
- CLC = pooled settlement, routing, liquidity

**Integration point:** BKC's commitment dependency graph (the `depends_on` predicate, migration 067) is the foundation. Extending this with temporal constraints, sequencing rules, and cascade logic is the path toward richer planning.

**Open questions:**
- Is seasonal routing a scorer weight (simple) or a constraint (hard block on out-of-season fulfillment)?
- How do dependency chains interact with pool activation thresholds?
- When does the planning layer warrant its own protocol (VF/hREA), vs. extending BKC's existing dependency graph?

---

## 7. Playground / Onboarding Pathway

**Question:** How do people get from mapping workshops to live commitment pools?

**Working answer:** The pathway is progressive formalization — from low-stakes social practice to high-stakes digital infrastructure:

| Stage | Medium | Stakes | Infrastructure |
|-------|--------|--------|---------------|
| **Paper mapping** | Sticky notes, large paper maps, conversation | Low — social only | None |
| **Digital commitments** | `/commons/commit` templates, structured forms | Low — recorded but not pooled | BKC knowledge graph |
| **Steward curation** | Pool stewards review, pledge, and verify | Medium — peer accountability | BKC governance membrane |
| **Test pools** | Sandbox pools with no real liquidity | Medium — practicing real operations | BKC pool state machine |
| **Live pools** | Activated pools with flow funding or liquidity | High — real economic activity | BKC + TBFF settlement |
| **CLC-compatible pools** | On-chain SwapPools with tokenized commitments | High — on-chain and cross-community | BKC + CLC infrastructure |

Landscape group programs with upcoming mapping and flow-funding phases provide a near-term deployment window for the early stages of this pathway. The `/commons/commit` form already supports preset templates (Restoration, Equipment Loan, Mycoremediation) designed for workshop use.

**Integration point:** The transition from "test pool" to "live pool" is the TBFF threshold policy — auto/semi/manual bands based on settlement amounts. The transition from "live pool" to "CLC-compatible pool" is the decision ladder (see §10).

**Open questions:**
- What `/commons/commit` templates work best for in-person workshop contexts?
- Should test pools use a separate "playground" environment, or sandbox mode within the live system?
- How do we handle the social transition when sandbox commitments become real?

---

## 8. Composability and ValueFlows

**Question:** Where does ValueFlows / hREA fit in the BKC + CLC stack?

**Working answer:** Not now — but the architectural question is important for the longer arc.

CLC is strong on redeemable commitments, pools, routing, and settlement. It's less strong on modeling dependencies, prerequisites, recipes, workflows, and staged development. Example: "I commit agroforestry management services" depends on land access, tools, collaborators, nursery stock, financing, and timing. CLC doesn't model these dependencies.

BKC has a basic dependency graph (`depends_on` predicate) but doesn't model intents, plans, recipes, or process logic. ValueFlows / hREA fills this gap:

```
BKC (knowledge + curation)
  → ValueFlows/hREA (intents → plans → recipes → processes)
    → CPP/CLC (pooled settlement + routing)
```

This is also relevant to the Coasys/Holochain work in the broader ecosystem — hREA runs on Holochain, and Coasys provides a framework for social coordination that could complement BKC's federation model.

**Integration point:** BKC's commitment schema could evolve to include VF-compatible fields (intent, plan, recipe references). But this is post-hackathon architectural research, not sprint scope.

**Open questions:**
- Is the VF/hREA layer a separate service, or does it extend BKC's ontology?
- How does VF's agent/process/resource model map to BKC's entity types?
- Is there active VF/hREA work in the Celo ecosystem that could be partnered with?

---

## 9. Community Mapping Protocol Expansion

**Question:** What should community mapping workshops capture beyond needs and offers?

**Working answer:** Current mapping workshops focus on needs and available resources. For commitment pooling, they should expand to capture:

- **Offers** — what can this person/organization concretely provide? → maps to OFFER intents in the [intent publication proposal](./intent-publication.md)
- **Capacities** — at what scale, frequency, and quality?
- **Intents** — what might someone commit to if conditions are right? → maps to CONDITIONAL intents (threshold activation)
- **Needs / Gaps** — what is missing in this landscape? → maps to WANT intents
- **Dependencies** — what prerequisites must be met?
- **Stewarding entities** — who is accountable for curation and governance?
- **Candidate pools** — what natural clusters of commitments emerge?
- **Priorities and objectives** — what does this landscape most need?
- **Seasonal patterns** — when are different commitments most appropriate?

This bridges bioregional commoning practice and commitment pooling infrastructure. The mapping workshop becomes the intake funnel for the entire pipeline: mapping → commitments → routing → curation → pools → settlement → proof → learning.

**Integration point:** `/commons/commit` templates should match workshop mapping categories. Entity types from mapping (Person, Organization, Project, Commitment, CommitmentPool) already exist in the BKC ontology.

**Open questions:**
- What facilitation guides or templates help workshop participants think in terms of commitments and pools?
- How do workshop facilitators handle the gap between expressed intent and actual commitment?
- Should mapping outputs go directly into BKC, or through a review/curation step?

---

## 10. Decision Ladder: TBFF to Pool to CLC

**Question:** When does support stay as TBFF flow funding? When does it seed a portfolio pool? When does a pool become CLC-compatible?

**Working answer:** This is a progressive commitment ladder — each stage adds infrastructure, governance, and accountability:

| Stage | Trigger | Settlement |
|-------|---------|------------|
| **TBFF flow funding** | Hub cultivator decision, threshold bands | BKC-native (evidence → claim → proof pack) |
| **Curated portfolio pool** | Multiple commitments from identified stewards, activation threshold met | BKC-native + pool state machine |
| **CLC-compatible pool** | Tokenizable commitments, viable `Hop[]` paths, on-chain settlement adds value | CLC on-chain (SwapPool) + BKC write-back |
| **Confederation profile** | Multiple CLC pools, own routing preferences, sovereign governance needs | Routable across CLC confederation |

Key decision criteria at each transition:

- **TBFF → Pool:** Do multiple commitments cluster around a landscape or theme? Is there a steward willing to curate? Are commitments concrete enough for peer accountability?
- **Pool → CLC:** Are commitments redeemable (labor, goods, services — not knowledge curation)? Does cross-community routing add value? Is GiftableToken representation meaningful? Do viable `Hop[]` paths exist on the CLC token graph?
- **CLC → Confederation:** Does Cascadia need its own fee policy, insurance scope, and compliance hooks? Is there enough volume to justify independent infrastructure?

**Integration point:** TBFF threshold policy (auto/semi/manual bands) is live. Pool state machine (PROPOSED → VERIFIED → ACTIVE) is live. CLC integration (Phase 1-3 in clc-integration-strategy.md) is the post-hackathon roadmap.

**Open questions:**
- What pool activation threshold triggers the transition from "collection of commitments" to "active pool"?
- How many active pools with tokenizable commitments would justify a Cascadia network profile?
- What's the minimum CLC integration needed to test the Pool → CLC transition? (Alfajores testnet?)

---

## References

- [CLC White Paper](https://cosmolocal.credit) — CPP core primitive (Ch 1), routing as service (§5.2), confederation (§5.2a), portfolio pools (§7.3.2)
- [CLC Integration Strategy](./clc-integration-strategy.md) — Three-phase technical roadmap
- [Compatibility Memo](./compatibility-memo.md) — BKC ↔ GE ↔ CLC concept mapping
- [Commitment Pooling Foundations](../foundations/commitment-pooling-foundations.md) — Lifecycle, governance, and protocol design
- [Intent Publication & Agent-Mediated Routing](./intent-publication.md) — Async intent layer proposal
- [Will Ruddick, "A Physics of Intention"](https://willruddick.substack.com/p/a-physics-of-intention) — Commitments as measurable system primitives
- [Regenerate Cascadia Hub Cultivator](https://regeneratecascadia.org/hub-cultivator/) — Landscape group training program
- [Sarafu Dune Dashboard](https://dune.com/grassrootseconomics/sarafu-network) — Live network metrics
