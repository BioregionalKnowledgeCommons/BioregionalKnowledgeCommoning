# Commitment Economy Vision

**Layer:** Pattern Language + Capital Coordination + Philosophy
**Status:** Draft v0.1 — 2026-03-22
**Author:** Darren Zal
**Source context:** Will Ruddick / Grassroots Economics, Cosmo-Local Credit (CLC) white paper, Kinship Earth / Regenerate Cascadia BioFi, BKC foundations, Mycopunks TBFF protocol
**Companion doc:** [commitment-economy-design.md](./commitment-economy-design.md) (technical spec, on-chain architecture)

---

## 1. The Economy as Ecosystem

A commitment economy is not financial infrastructure. It is an economic ecology.

Will Ruddick:
> "At this level, the architecture of coordination begins to feel like and resemble life itself — mycelial, distributed, sensitive to feedback and relationship."

> "The emergent phenomena of a network of pools is a very important topic! You can think of the long tail of pooling being that we all express our agreements and the network of overlapping pools is the fully intangible un-ownable commons."

Maturana and Varela:
> "Living systems are cognitive systems, and living as a process is a process of cognition."

The analogy is more than metaphor. A network of commitment pools behaves like a living system: it senses its environment (mapping workshops, interviews, observations), makes meaning (routing scores reflect what the network values), cares (stewards decide whose needs are prioritized), commits (concrete promises with typed offers and limits), coordinates (settlement, redistribution, multi-hop routing), and learns (evidence of fulfillment updates the network's understanding of what works).

But living systems also get sick. They face parasites, cascading failures, resource depletion. An economic ecology that only describes growth and circulation is incomplete. It needs an immune system — mechanisms that detect harm, limit damage, and enable recovery.

This document describes four metabolic functions that together make a complete commitment economy: provisioning, redistribution, activation, and repair.

---

## 2. Four Metabolic Functions

### 2.1 Provisioning — Commitment Pooling

Making capacity legible and routable. People issue vouchers backed by productive capacity — labor, goods, services, knowledge, stewardship. Pools curate and value these individual vouchers, making them collectively liquid. Cycle clearing and netting across commitments reduces dependence on external currency.

This is the circulatory system: what the economy can offer, made visible and matchable.

See [commitment-pooling-foundations.md](./commitment-pooling-foundations.md) for the full technical model, state machine, and three orthogonal operations (create, pledge, verify).

### 2.2 Redistribution — Threshold-Based Flow Funding

Ensuring sufficiency. Each participant declares a needs threshold and a comfort level. Overflow above comfort routes to those below threshold. External funding (grants, stablecoins) enters through TBFF and flows to where it's needed most.

This is the watershed: capital flows like water from abundance to need, governed by trust relationships and ecological context.

See [flow-funding-foundations.md](./flow-funding-foundations.md) for the TBFF algorithm, Hub Cultivator model, and two-track integration.

### 2.3 Activation — Network Growth

How new participants join and existing participants deepen their engagement. The primary activation mechanism is **community practices that make commitments legible** — mapping workshops where people articulate offers and needs, rotational labor circles (Mweria, Meitheal), potlucks, assemblies, school projects, any gathering where people express what they can do for each other and what they need.

Will Ruddick:
> "If you want a simple on-ramp: host a potluck with vouchers as thank-you notes that can be swapped later. You'll feel the protocol 'click' the first time the circle redeems those notes into real help."

The commitment economy starts when people formalize what they can offer and what they need — not when capital arrives. For Regenerate Cascadia, the bioregional mapping workshops (Phase 2, March–June 2026) ARE the primary activation: landscape groups mapping offers, needs, watershed indicators, and project portfolios.

Flow funding supplements activation by providing external capital that covers what the internal commitment economy can't yet close — the gap at each level of the fractal structure. But it is one channel among many. Other activation paths include: rotational labor practices that build trust through repeated collaboration, community assemblies that surface offers and needs through structured dialogue, and the circulation of commitments itself (more offers → more matches → more participants).

**Speculative mechanism for Cascadia to explore**: When demurrage IS activated for a pool (see §3), could the decayed value flow to a Commons Activation Fund that stewards direct toward projects below their activation threshold? This would combine the "community fund" pattern with TBFF-like threshold logic — a dual track where some flows algorithmically to nodes below threshold and some is steward-directed. This is experimental, not a proven design.

### 2.4 Repair and Protection — The Immune System

Limits, insurance, disputes, forkability, consent boundaries, and bounded autonomy. This is the function that both CLC and BKC center but that economic vision documents often leave implicit.

CLC (Chapter 6) builds downside protection at three levels:
- **Protocol-level**: Trade limits and inventory enforcement — cannot swap what the vault does not hold. Immutable receipts for every action.
- **Network-level**: Loss waterfall — issuer/guarantor bonds → pool reserves → network insurance → policy-capped haircuts → clawbacks for fraud. Insurance reserve is the first waterfall priority, before operations or liquidity mandates (Appendix B).
- **Governance-level**: Timelocked parameter changes with notice-to-cure and appeal paths. Emergency actions require incident reporting and automatic sunset review.

BKC adds:
- **Consent boundaries**: `node_private` visibility scope, 34 query sites filtered across 15 public endpoints. Communities control what's visible to the network.
- **Disputes**: `disputes` predicate with DISPUTED → RESOLVED transition in the commitment state machine. Any party can formally contest a commitment.
- **Forkability**: Any steward can fork a pool — take the commitments they trust and create a new pool with different governance. Authority over a pool is earned by curation quality, not granted by position.
- **Bounded autonomy**: Small capital allocations can be automated; larger ones require human review. Capital allocation decisions reference knowledge entity RIDs. All allocation outcomes are logged as Evidence entities with provenance.

Will Ruddick:
> "Where coercion enslaves, pooling frees. Where coercion extracts, pooling regenerates. Where coercion erases memory, pooling deepens it."

Protection and repair are not overhead — they are what makes the economy safe enough for people to participate without risking their wellbeing.

---

## 3. Demurrage: A Seasonal Tool, Not a Standing Engine

Will Ruddick's thinking on demurrage has evolved significantly. Early implementations used a standing 2% monthly decay on all vouchers. Current writing moves in a different direction:

> "Demurrage often becomes a burden inside pools because it silently changes commitments held in the pool on a schedule rather than by agreement. In practice, it means any credit line given (collateralized by vouchers as debt in a pool) will automatically disappear over time, granting more credit access to the holder as old obligations melt away. That might be the right medicine after a shock. But as a standing automated rule it expands credit without checking whether capacity has returned. Make sure you really want that in your pool."

> "The commitment pool functions make demurrage and bonding curves feel a bit antiquated. There is often no need to keep them locked in. Keep them on the shelf and reach for them when a specific season calls for them - briefly, with a reason people can understand."

> "If you can't explain a rule in one breath, it probably shouldn't run all year."

The key insight: a voucher's true worth is its **swap-ability** — its ability to travel through the group to someone who wants it and back to an issuer who can fulfill it. If a voucher moves and is redeemed, it's valuable. If it gets stuck, no timer fixes that. Stewardship does.

### What This Means for Design

Pool nourishment comes primarily from:
- **Swap fees**: Tiny transaction fees that feed the shared pot transparently
- **Periodic share-outs**: Deliberate distributions based on steward decisions
- **Steward-set limits**: Boundaries that protect the commons — how much of any one promise the pool will accept

Demurrage stays as a **configurable option** (`demurrage_rate_monthly`, default 0) — a tool on the shelf, reached for when a specific season calls for it. Activated briefly, with a reason people can understand, and deactivated when the need passes.

> "Demurrage forgives by calendar, not by capacity. Pools forgive by conversation, evidence, and season."

### Speculative: Commons Activation Fund

When demurrage IS activated for a specific pool, where should the decayed value flow? One possibility worth exploring in the Cascadia context:

A **Commons Activation Fund** that directs resources toward projects below their activation threshold — the minimum resource level needed to become a viable participant in the commitment economy. Two tracks from the same fund:
- **Algorithmic track**: Decayed tokens auto-route toward nodes below their activation threshold (like TBFF but for network growth)
- **Steward track**: A portion is directed by Flow Funders toward activation opportunities that require relational judgment

This would create a positive feedback loop: more circulation → more fees (and occasionally demurrage) → more activation capacity → more participants → more circulation. But this is a hypothesis to test, not a proven mechanism. The proven activation path is flow funding through trusted stewards.

---

## 4. Making Needs Compositional

The existing [commitment-economy-design.md](./commitment-economy-design.md) already defines the system as commitment pooling (supply & exchange) plus TBFF (needs-based redistribution). During the hackathon sprint, we added `declaration_type: need`, `fiat_only`, `need_category`, and `monthly_amount_usd` to the commitment data model, enabling the AI agent to extract both offers and needs from mapping workshop conversations.

The sharper claim is not that needs are missing, but that they are **not yet compositional**. The data fields exist, but they don't yet feed through the full system:

**Pool governance**: Does a pool track its aggregate needs gap? Can stewards see "this pool has 40 hours of restoration offers but zero soil-testing equipment"? Can they see which needs are fiat-only (requiring real dollars) versus substitutable (could be met through in-kind exchange)?

**Routing scorer**: Does a commitment that fills an unmet need score higher than one that adds to existing surplus? Currently the scorer weighs bioregion proximity, taxonomy overlap, timeframe alignment, capacity fit, and governance compatibility — but it doesn't yet incorporate the demand signal from declared needs.

**Activation decisions**: When a node is below its needs threshold, what mechanism brings resources to it? Flow funding is the primary answer. But the needs data should inform flow funding decisions — stewards should be able to query "which landscape groups have the largest unmet needs gap?"

**Evidence loop**: When a need is met (Evidence entity linked to a fulfilled commitment), does the routing scorer learn from that fulfillment? Does the pool's aggregate needs gap update? Does the network's understanding of what's needed improve?

Making needs compositional means wiring them through this full cycle — not adding a new layer, but connecting what's already there.

Will Ruddick:
> "A care network is only as stable as the food, water, and repair capacity beneath it. If a watershed fails, care hours get consumed by hauling and coping. If soil is depleted, households face higher volatility, even if coordination is perfect."

> "Context matters. Stay humble: first, meeting basic needs; second, growing along a unique path; third, helping others from abundance."

The sufficiency floor is the contract: participation in this economy does not cost you your wellbeing. TBFF handles redistribution; flow funding handles activation; but the sufficiency floor is the principle that all mechanisms serve.

---

## 5. Composability — How Commitments Click Together

Will Ruddick:
> "Composability here means that commitments from many actors and held in many pools can click together without special deals or centralization. When two pools recognize the same kind of commitment (like a formal voucher) a swap can route across them. Each hop checks the same four things, so safety is local yet preserved hop-by-hop. The effect is like the forest: a polycentric mesh where resources find their place through small, rule-consistent moves. This is what we mean by cosmo-local."

Composability in BKC operates at multiple layers:

### Exchange Composability (implemented)

Multi-hop routing across pools. CLC's `Hop[]` paths compute input/output amounts across multiple SwapPools. Each hop enforces the same four functions — curation, valuation, limitation, exchange — so safety is local yet preserved end-to-end. CLC's "cycle surfacing" (Chapter 5) shows that obligation networks contain cycles that can be processed simultaneously, reducing need for external liquidity. BKC currently implements routing scorer v0 (single-pool MVP with scored suggestions). Multi-hop `Hop[]` path construction and cross-pool settlement are planned for C1.

### Governance Composability (partially implemented)

The three orthogonal operations — create, pledge, verify — already compose freely. A commitment can be created (self-sovereign), pledged to multiple pools (peer-curated), and verified by any peer (trust-attested), in any order or combination. These operations are independent along every axis: actor, gate, reversibility.

Ruddick extends this with Steiner's threefold governance model — Cultural stewards (gift flows and learning), Rights stewards (fair access and agreements), Economic stewards (real supplies and settlements). When pools overlap, their membranes translate across value systems: "we seed with Gift, settle via Payment, open Loan where coverage holds, and return surplus and failures alike to Gift for renewal." BKC's consent boundaries and federation governance are partially this already.

### Production Composability (future — BKC architectural extension)

Commitments can do more than exchange — they can chain into production sequences. "I'll deliver processed timber if someone commits raw logs and milling time." This requires conditional commitments, dependency tracking, and process recipes.

BKC has a basic dependency graph (`depends_on` predicate, migration 067) but doesn't yet model intents, plans, recipes, or process logic. ValueFlows/hREA provides the mature formal model for this layer — Intents/Commitments as the resource map, ProcessSpecifications as production recipes, Processes with linked input/output Commitments as conditional production.

This sits in the planning semantics layer between BKC and CLC (documented in [clc-questions-synthesis.md §8](../ge-integration/clc-questions-synthesis.md)):

```
BKC (knowledge + curation)
  → ValueFlows/hREA (intents → plans → recipes → processes)
    → CPP/CLC (pooled settlement + routing)
```

Production composability is our architectural extension consistent with Will's composability framework — his text directly supports interface interoperability, pooled legibility, and multilateral pools as the grammar that makes composability possible. The production layer extends that grammar to cover dependencies, sequences, and conditional outputs.

### The Pool as Shared Bowl

Ruddick draws a crucial distinction between bilateral chains and multilateral pools:

> "We often think of contribution as inherently bilateral: a promise to a particular person, a return from a particular source. But in a living pool, the relationships are multilateral. I don't give to you alone — I give to us. You don't take from me — you draw from us."

Composability ultimately rests on this: a pool is a shared bowl where resources are offered and borrowed as one. Chains (cycles of sequential commitments) show how commitments flow through networks, but pools show how they aggregate into collective liquidity. Both matter — but the pool is the center.

---

## 6. The Learning Loop

Will Ruddick describes intelligence as a metabolic cycle:

> "Sensing: attend to bodies, places, data, testimonies. Meaning-making: form shared models of what's happening and what matters. Caring: surface feelings, needs, limits, trade-offs; include objections as information. Committing: make promises that can be held to, with clear success criteria and constraints. Coordinating: align roles, resources, and timing to fulfill the promises. Learning again: compare intent with outcome; update models, rules, and trust."

> "In metabolic terms, intelligence routes attention, care, and trust so that life can keep flourishing."

### How the Loop Maps to BKC

| Step | BKC Mechanism | What Happens |
|------|--------------|--------------|
| **Sensing** | Mapping workshops, interviews, observations | Human experiences become knowledge graph entities |
| **Meaning-making** | Routing scorer | Each commitment modifies the landscape for future commitments (stigmergic intelligence) |
| **Caring** | Pool governance | Stewards decide what matters, whose needs are prioritized, which commitments fit |
| **Committing** | Commitment entities | Typed offers, needs, and limits with state machine and audit trail |
| **Coordinating** | Settlement, TBFF, multi-hop routing | Matching supply to demand, redistributing from abundance to need |
| **Learning** | Evidence entities, KPIs | Fulfillment creates knowledge that feeds back into routing and governance |

### Stigmergic Intelligence

The routing scorer is a form of distributed intelligence. It's stigmergic — indirect coordination through environment modification. Each commitment placed in the network modifies the landscape:
- A pool that fills a need sends a signal that reduces routing scores for similar offers (capacity met)
- A pool with unmet needs increases routing scores for matching offers (demand signal)
- Cross-bioregion routing via `broader` edges enables network-wide supply/demand matching

No central planner decides what's needed. The network learns through its own activity. But this intelligence is bounded — it surfaces patterns for human stewards to act on, it doesn't make capital allocation decisions autonomously.

### CLC's KPI Framework (Advisory, Not Deterministic)

The CLC white paper (Chapter 14) defines concrete health indicators:
- **Fulfillment rate**: What proportion of commitments reach REDEEMED state?
- **Redemption latency**: How long from settlement to fulfillment?
- **Reserve adequacy**: Are pool reserves sufficient for the outstanding obligation stock?
- **Limit utilization**: How close are pools to their capacity boundaries?
- **Netting yield**: `(gross routed value − net external liquidity injected) / gross routed value`. Higher = more circular.
- **Well-being outcomes**: Basic-needs voucher redemption success (food, transport, health)

**Important nuance**: The CLC fee waterfall is deterministic *once policy is set* (Appendix B). But KPI-linked budgets are *advisory inputs* to timelocked policy edits (Chapter 7) — not deterministic triggers. Governance decisions are deliberate and human-reviewed. The learning loop feeds human judgment, not algorithmic adjustment.

### BKC's Contribution: Collective Learning Across Bioregions

The knowledge graph makes the learning step legible across bioregions. Evidence of fulfillment in Victoria is visible (subject to consent boundaries) to stewards in Front Range. Patterns that work in one landscape group can be surfaced as recommendations to others — with the situated-transfer metadata that §11 requires.

Progress is not about reducing interdependence — it's about shifting its quality. The goal is to reduce **unhealthy dependency** (on donor cycles, chokepoint suppliers, learning loops you don't control) while increasing **healthy interdependence** (reciprocal, visible, chosen, distributed). The netting yield — how much settlement is internal vs externally funded — measures reduced metabolic dependency on extractive systems, not reduced connection to the world. The knowledge graph tracks the stories behind the numbers: which dependencies were extractive and got replaced, which interdependencies are regenerative and got strengthened.

---

## 7. From Flow Funding to Commitment Economy — A Concrete Path for Regenerate Cascadia

### Phase 0: Where Regenerate Cascadia Is Now

Kinship Earth's flow funding model is trust-based, low-paperwork, and narrative-accountable:

> "No applications. No bureaucracy. Grounded in collaboration, solidarity, and trusting those who know their communities best to lead the way."

Regenerate Cascadia's Landscape Hub Cultivator program is entering its bioregional mapping and flow funding phase (Phase 2, March–June 2026). Current scale:
- **13 landscape groups** across Cascadia (10 in the current pilot cohort)
- **~40 landscape stewards** participated in Phase 1; 2–3 designated per group
- **$8,000 per landscape group** ($5,000 for mapping/planning + $3,000 for flow funding)
- **$30,000 total flow funding** across the 10 pilot groups; **$80,000 total support** including mapping
- **681+ members**, **30 connected organizations**

The flow funding governance is deliberately plural. As the RC site describes: "Some groups may invite applications for a series of micro-grants. Others may convene a local committee to identify and nominate projects." The common thread: "allocation decisions are made by community members who hold direct relationships with the people and places being supported."

The pilots "prioritize learning over immediate impact" — they are proof-of-concept for community-governed allocation.

**This is not a primitive version of commitment pooling that needs upgrading.** It is the trust infrastructure that makes commitment pooling possible. The relational knowledge that Flow Funders carry — who can deliver, who needs support, what's working — is the governance layer. Commitment pooling adds legibility to what they already know.

### Progressive Deepening

Each phase adds legibility without removing trust. Different landscape groups may transition at different paces and through different governance models — the situated-transfer pattern (§12) applies at every stage.

**Phase 1: Expressing commitments formally**

During mapping workshops (already happening in Phase 2 of the Hub Cultivator program), participants articulate what they can offer and what they need. Today these exist in conversation, worksheets, and strategy documents. In Phase 1, they become Commitment entities — structured, searchable, aggregatable.

A steward in Victoria can say "we need soil-testing equipment" and it becomes a declared need in the knowledge graph, visible to anyone with access. A nursery in Whatcom can say "we offer 500 native seedlings, April–September" and it becomes a typed offer with timeframe and capacity constraints.

This doesn't change the governance. Flow Funders still decide. But they can now see — in aggregate — what the network offers and what it needs.

**Phase 2: Commitments aggregate into pools**

Multiple commitments group into landscape-level pools. The Victoria Landscape Hub Restoration Pool, the Skagit Watershed Stewardship Pool, the South Willamette Agroforestry Pool. Each pool has stewards who curate which commitments belong.

Flow Funders now have visibility into aggregate capacity across their landscape: what's offered, what's needed, where the gaps are. The `broader` edge from Salish Sea to Cascadia means offers and needs are visible across bioregions — a nursery in one landscape group can see unmet need in another.

**Phase 3: Routing scorer as decision-support tool**

When a new commitment comes in, the system shows which pools need it most — scored by bioregion proximity, offer/need taxonomy overlap, timeframe alignment, and capacity fit. This is a recommendation, not a decision. Stewards review the suggestion and apply their relational knowledge.

Some landscape groups may adopt this eagerly. Others may prefer to continue with narrative accountability and manual coordination. Both are valid.

**Phase 4: TBFF supplements steward decisions**

For landscape groups ready for it, TBFF handles the mechanical part of redistribution — threshold overflow routing, needs-weighted allocation. Stewards set the thresholds and allocation preferences. The algorithm executes. Stewards retain override authority and review all settlements above a threshold band.

This is where the two tracks of flow funding converge: human-mediated (Hub Cultivator) and algorithmic (TBFF), both writing Evidence back to the knowledge graph.

**Phase 5: From extractive dependency to regenerative interdependence**

As internal circulation increases, unhealthy dependencies decrease — donor cycle dependency (waiting for the next grant), chokepoint vulnerability (reliance on single suppliers), and metabolic dependency (inability to meet basic needs locally). But healthy interdependence increases: more cross-bioregion routing, more reciprocal exchange, more federated learning. The netting yield tracks circularity. Commitment vouchers become exchangeable — first within pools, then across pools via swap routes. What used to require grant funding is increasingly met by internal commitment exchange — but the network is more connected, not more isolated.

Flow Funders have not been replaced. They have become pool stewards with better tools — aggregate visibility, routing recommendations, needs-gap analysis, evidence-based learning. Or they may have evolved in directions we can't yet predict. **This transition is a design hypothesis, not a sourced conclusion.** It's a proposal to explore with Regenerate Cascadia, Kinship Earth, and the landscape groups themselves.

---

## 8. Protection and Repair

An economy that people trust enough to participate in must be safe enough that participation doesn't cost them their wellbeing. Protection and repair are not overhead — they are the foundation.

### Limits That Protect the Commons

Will Ruddick:
> "There are clear limits so no one promises too much or tries to control everyone else. Think of a neighborhood resource pool where folks actually deliver the rides, meals, or repair hours they promised — and everyone has a cap on how much they can take on."

Limits are boundaries, not restrictions. Pool stewards set:
- How much of any one promise the pool will accept
- How much credit a person can draw before redeeming
- Seasonal adjustments based on real capacity (not formulas)

### The Loss Waterfall

CLC's fee waterfall (Appendix B) prioritizes safety:
1. **Insurance Reserve Target**: Top-up to risk-weighted target based on pool obligations, fulfillment rate, issuer concentration
2. **Core Operations**: Timelocked budget for legal, infrastructure, audits
3. **Liquidity Mandates**: Endowments to target pools/routers for settlement capacity
4. **Pooled Fees**: Remaining fees allocated to protocol operations, incentives, overflow reserve

Insurance comes first. Before operations, before growth, before anything else. This is the principle: protect the people in the system before optimizing the system.

### Graduated Response

Not every problem requires sanctions. CLC's governance model:
- **Notice-to-cure** before any enforcement action
- **Appeal paths** for contested decisions
- **Timelocked parameter changes** with public notice
- **Emergency actions** require incident reporting and automatic sunset review

BKC adds the **disputes predicate** — any party can formally contest a commitment, triggering a DISPUTED → RESOLVED transition that follows the commons governance membrane.

### Forkability as the Ultimate Safety Valve

If a pool's curation standards diverge from community values, any steward can fork the pool — take the commitments they trust and create a new pool with different governance. The original commitments survive (they exist independently of any pool). This is the antidote to possessive stewardship: you cannot capture a pool because the underlying commitments are not yours to hold.

Will Ruddick:
> "In a truly anti-fragile credit network: Fee credits, routing preference, and any network rewards must be gated by measurable redemption and fulfillment signals, not token price and not narrative momentum. If financial upside can grow while redemption quality decays, the network will drift toward speculation and enclosure."

### Consent as Boundary

Commitment data carries `sensitive` data class by default. Cross-node federation of individual commitment details requires explicit steward opt-in. The consent membrane (34 query sites filtered across 15 public endpoints) ensures that `node_private` commitments never leak.

Bounded autonomy for capital decisions: small allocations can be automated; larger ones require human review. Capital allocation decisions must reference knowledge entity RIDs, not just descriptions. All allocation outcomes are logged as Evidence entities with provenance. This is Pattern 8 (Evidence Loop) from BKC's AI swarms pattern language.

---

## 9. The Pattern Language

Core patterns for a commitment-based economy. Each pattern names a force, a solution, and a tradeoff.

### 9.1 Commitment as Currency
- **Force**: Communities have productive capacity (labor, goods, stewardship) but lack liquidity to exchange it.
- **Solution**: Value arises from trusted capacity to deliver, not from speculation or external price signals. A commitment to "10 hours of watershed monitoring" has value because the community trusts the pledger.
- **Tradeoff**: Requires trust infrastructure and verification — cannot be bootstrapped in the absence of social relationships.

### 9.2 Pool as Commons
- **Force**: Individual commitments are illiquid; collective pools create exchange capacity.
- **Solution**: Pools curate and aggregate individual vouchers, making them collectively liquid. Multi-hop routing across pools extends exchange range without centralization.
- **Tradeoff**: Pool governance requires active stewardship. Neglected pools degrade.

### 9.3 Threshold as Safety Net
- **Force**: Participants have different needs levels; market mechanisms alone don't ensure sufficiency.
- **Solution**: Every participant declares a needs threshold. Overflow above comfort routes to those below threshold. The economy has a floor.
- **Tradeoff**: Requires honest needs declaration and periodic reassessment. Threshold-gaming is possible.

### 9.4 Demurrage as Seasonal Tool
- **Force**: Idle capacity can accumulate, reducing circulation and creating stale pools.
- **Solution**: Demurrage is available as a reversible, steward-activated tool — reached for when a specific season calls for it, deactivated when the need passes. Not a standing tax.
- **Tradeoff**: If left on as automation, it becomes a burden that expands credit without checking capacity. Use briefly, with a reason people can understand.

### 9.5 Routing as Intelligence
- **Force**: Commitments need to find their way to the right pools without manual matchmaking.
- **Solution**: Transparent, deterministic multi-factor scoring. Each commitment modifies the landscape for future commitments (stigmergic). No black-box ML.
- **Tradeoff**: Routing is recommendation, not allocation. Stewards must review suggestions.

### 9.6 Evidence as Learning
- **Force**: Without feedback, the economy can't learn from its own activity.
- **Solution**: Every fulfillment creates an Evidence entity that updates the network's understanding. Proof of delivery, ecological outcomes, wellbeing impacts — all stored in the knowledge graph and available (subject to consent) for cross-bioregion learning.
- **Tradeoff**: Evidence collection adds overhead. Must balance rigor with usability.

### 9.7 Fork as Exit
- **Force**: Governance can be captured; stewards can become gatekeepers.
- **Solution**: Any steward can fork a pool. Commitments exist independently of pools. Authority is earned by curation quality, not position.
- **Tradeoff**: Forks can fragment liquidity. The community must weigh governance integrity against pool depth.

### 9.8 Federation as Scale
- **Force**: Single-bioregion economies are limited; centralized coordination is fragile.
- **Solution**: Each bioregion is autonomous with its own database, governance, and identity. Nodes exchange events via signed envelopes. `broader` edges enable cross-bioregion routing. Network effects without control.
- **Tradeoff**: Federation requires consent negotiation and edge approval. Not all data should travel.

### 9.9 Dependency Quality as Progress
- **Force**: Conventional metrics (transaction volume, token price) can grow while the real economy stagnates. But simplistic "less dependency" metrics can accidentally incentivize isolation over connection.
- **Solution**: Progress means reducing four types of unhealthy dependency while strengthening healthy interdependence:
  - Reduce **donor cycle dependency** — external cash that suppresses internal exchange (Ruddick: "Gridlock, round two. Now reinforced with a dependency on the donor cycle.")
  - Reduce **chokepoint vulnerability** — reliance on foreign inputs only one source controls
  - Reduce **learning-loop dependency** — outsourcing representational infrastructure you don't shape (Johar: "That dependency is the structural risk.")
  - Reduce **metabolic dependency** — inability to meet basic needs through local production capacity
  - Increase **healthy interdependence** — reciprocal flow, visible exchange, chosen connection, distributed adaptive capacity, cosmo-local coherence
  - The netting yield — `(gross routed value − net external liquidity injected) / gross routed value` — measures circularity: a proxy for reduced metabolic dependency, not for autonomy.
- **Tradeoff**: This is slower and harder to measure than simple import substitution. Requires distinguishing which dependencies are extractive (replace them) from which are regenerative (strengthen them).

### 9.10 Stewardship over Automation
- **Force**: Algorithmic mechanisms are tempting because they scale; but they remove context.
- **Solution**: Human judgment guides mechanisms. Algorithms handle mechanical redistribution; stewards handle relational decisions. Capital decisions above threshold require human review. Boundary crossing requires consent.
- **Tradeoff**: Slower, more labor-intensive than full automation. But more trustworthy and adaptable.

### 9.11 Situated Transfer
- **Force**: Patterns that work in one bioregion may appear relevant in another, but abstractions travel faster than the conditions that made them work.
- **Solution**: Recommend patterns only with explicit context packets: source practices, ecological and governance preconditions, rights/consent constraints, contraindications, and required local adaptation. Keep descriptive pattern matches distinct from prescriptive protocol recommendations.
- **Tradeoff**: More metadata to maintain. Slower recommendation loops. But prevents cargo-cult adoption and extractive reuse.

---

## 10. Convergence with CLC

The Commitment Pooling Protocol (CPP) as specified by CLC provides the economic primitives. BKC provides the knowledge commons substrate. Together they create the full loop.

### Mapping to CLC's Four Interfaces

| CLC Interface | BKC Implementation | What It Does |
|--------------|-------------------|--------------|
| **Curation** | Governance membrane + three orthogonal operations (create/pledge/verify) | Stewards curate which commitments belong in which pools |
| **Valuation** | Routing scorer + steward-set limits and relations | Community signals what's valued; scoring is transparent, not automated pricing |
| **Limitation** | TBFF threshold bands + pool capacity limits + consent boundaries | Safety boundaries that protect participants and the commons |
| **Exchange** | Settlement execution + multi-hop routing + swap pools | Moving value where it's needed and back home to be fulfilled |

### What BKC Adds

- **Knowledge substrate**: Evidence entities, knowledge graph, entity resolution — the learning loop needs a memory, and the knowledge graph is that memory.
- **Consent boundaries**: CLC assumes cooperative participants; BKC's membrane handles adversarial cases (data leakage, unauthorized access, visibility scope).
- **Federation**: CLC describes confederation as mesh of overlapping curations. BKC implements it: 4 nodes, signed envelopes, KOI-net protocol, consent-gated edge approval.
- **Situated transfer**: CLC is a protocol spec; BKC's pattern language provides the preconditions, misfit signals, and adaptation guidance for communities adopting it.

### Where We Align, Where We Diverge

**Aligned**: Value from trusted capacity (not speculation). Downside protection as first priority. Steward governance over algorithmic control. Forkability as safety valve. Dependency quality (reducing extractive dependency, strengthening regenerative interdependence) as progress metric.

**Divergent emphasis**: CLC's design centers on the economic mechanism (fee waterfall, voting escrow, sCLC token). BKC's design centers on the knowledge and consent layers (evidence graph, visibility scope, pattern language). Neither is complete without the other. CLC provides the plumbing; BKC provides the intelligence and governance.

---

## 11. Decentralized Intelligence with Bounded Autonomy

### The Agent as Participant, Facilitator, and Learner

In the hackathon demo, the AI agent participates as an economic actor — registering its own offers (transcription, extraction, routing, attestation services) and needs (audio data, community feedback, governance templates). Its commitments are verified and minted as VCV, demonstrating that infrastructure providers are first-class participants in the commitment economy.

But the agent's more important role is as a facilitator of the network's own intelligence:
- **Extraction**: Listening to mapping workshop conversations and structuring commitments from natural language
- **Routing**: Scoring how well commitments fit available pools, surfacing recommendations for steward review
- **Pattern recognition**: Identifying gaps (which needs are consistently unmet?), trends (which types of commitments have the highest fulfillment rate?), and opportunities (which cross-bioregion matches would fill capacity gaps?)

### Stigmergic Coordination

Each commitment placed in the network modifies the landscape for future commitments. A pool that fills a need reduces demand signals for similar offers. A pool with unmet needs amplifies demand signals for matching offers. The network learns through its own activity — no central planner required.

This is stigmergy: indirect coordination through environment modification. The same mechanism that allows ant colonies to find food paths and fungal networks to route nutrients. Simple protocols invite emergence.

### Sympoietic Learning

The network creates itself through its own activity. Evidence of fulfillment in one bioregion becomes knowledge available to stewards in another (subject to consent). Patterns that work propagate — with situated-transfer metadata that ensures they're adapted, not copied.

Will Ruddick:
> "We are a murmuration. A moving body of cells, people, traditions, cultures... breathing together, swarming not in chaos but in deep, responsive coordination."

### Bounded Autonomy as Constraint

BKC's pattern language (Evidence Loop, Pattern 8) constrains the agent:
- Capital allocation decisions must be **evidence-grounded** (reference knowledge entity RIDs)
- Small allocations can be automated; **larger ones require human multisig**
- Cross-bioregion commitment routing needs **explicit consent**
- All allocation outcomes are **logged as Evidence** with provenance

The intelligence is distributed — in the routing scorer, in the evidence graph, in the steward network, in the mapping workshops. The agent surfaces what the network is already doing. It does not control.

---

## 12. Situated Transfer Metadata

This document practices what it preaches. The patterns and mechanisms described here were developed in specific contexts with specific conditions. They should not be adopted wholesale.

### Source Practices

| Source | Scale | Status |
|--------|-------|--------|
| **Sarafu Network** (Grassroots Economics, Celo mainnet) | 26,367 users, 188 active pools, 745 vouchers, $320K swap volume, 1,200+ acres restored | Production since July 2023 |
| **Kinship Earth Flow Funding** | 10 landscape groups in pilot, $30K flow funding | Phase 2 pilot (2026) |
| **Regenerate Cascadia Hub Cultivator** | 13 landscape groups, ~40 stewards, $80K total support | Phase 2 pilot (2026) |
| **Mycopunks TBFF** | 5 participants, $32K simulated scenario | Experimental (2025–2026) |
| **CLC DAO** | Whitepaper spec | Pre-deployment design |
| **BKC Commitment Routing** | 4 nodes, 23 verified commitments, 33,400 VCV minted | Hackathon demo (March 2026) |

### Preconditions

For a bioregion to adopt these patterns:
- **Active stewardship team**: 3+ dedicated members with existing trust relationships
- **Trust infrastructure exists**: People know each other. Flow funding or equivalent relational capital allocation is already happening.
- **Basic knowledge graph operational**: Entity resolution, evidence storage, federation capability
- **Consent membrane in place**: Visibility scope, edge approval, data classification
- **Community is in mapping/assessment phase**: They have identified what they can offer and what they need, even informally

### Misfit Signals

Do not adopt these patterns if:
- There is no local steward network (commitment pooling requires governance)
- Trust relationships haven't been established (the technology adds legibility, not trust)
- The community is not yet in a mapping or assessment phase (commitments need grounding in real capacity)
- There is pressure to adopt quickly (each phase of the transition needs time to establish rhythms)

### Contraindications

- **Imposing commitment structure before trust exists**: Commitment pooling amplifies existing trust; it does not create trust from nothing
- **Automating before human rhythms are established**: TBFF supplements steward decisions; it does not replace them. Activate algorithmic redistribution only after manual redistribution patterns are well understood.
- **Treating demurrage as default**: Demurrage is a seasonal tool. Activating it without a specific reason creates a burden, not a benefit.
- **Copying governance models across contexts**: The plural governance of RC's pilot (micro-grants, local committees, narrative accountability) reflects real diversity. Each landscape group should design its own governance.

### Local Adaptation Required

- Demurrage activation criteria (if any)
- Routing scorer weights (which factors matter most locally?)
- TBFF threshold levels (what constitutes sufficiency in this bioregion?)
- Governance model (which of the three orthogonal operations — create, pledge, verify — are gated, and by whom?)
- Consent boundaries (what commitment data is visible to whom?)
- Phase transition timing (when is the landscape group ready for the next phase?)

---

## References

- Will Ruddick, collected posts (Substack + grassrootseconomics.org)
- Cosmo-Local Credit white paper, Chapters 6, 7, 14, Appendix B
- BKC foundations: [commitment-pooling-foundations.md](./commitment-pooling-foundations.md), [flow-funding-foundations.md](./flow-funding-foundations.md), [commitment-economy-design.md](./commitment-economy-design.md)
- BKC pattern languages: [pattern-language-for-bioregional-knowledge-commoning-v0.1.md](./pattern-language-for-bioregional-knowledge-commoning-v0.1.md), [bioregional-ai-swarms-pattern-language.md](./bioregional-ai-swarms-pattern-language.md)
- Kinship Earth: [kinshipearth.org/flow-funding](https://www.kinshipearth.org/flow-funding)
- Regenerate Cascadia: [regeneratecascadia.org/hub-cultivator](https://regeneratecascadia.org/hub-cultivator/), [regeneratecascadia.org/biofi/flow-funding-pilots](https://regeneratecascadia.org/biofi/flow-funding-pilots/)
- Humberto Maturana & Francisco Varela, *The Tree of Knowledge*
