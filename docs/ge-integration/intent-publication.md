# Intent Publication & Agent-Mediated Routing

## Status: Proposal (Draft)

This document proposes an **intent publication layer** for the Commitment Pooling Protocol that enables asynchronous, agent-mediated routing — extending the current synchronous request-for-quote model to support standing offers, needs, and swap desires that persist across time.

Two independent lines of work converge here. In the DeFi world, "intent-centric architecture" has emerged as a major design pattern — projects like Anoma, UniswapX, and CoW Protocol let users declare desired outcomes while competitive solvers handle execution. Meanwhile, Will Ruddick's [Physics of Intention](https://willruddick.substack.com/p/a-physics-of-intention) frames declared commitments as measurable system primitives — intention as density, trust as mass, fulfilled promises as stabilizing force — and the CPP whitepaper already describes pool-level "rebalance intents" for batch netting. Neither tradition references the other, but they arrive at the same structural insight: **coordination improves when desires are declared, persisted, and matched by agents rather than executed imperatively by users.**

This proposal sits at the intersection: applying the architectural patterns of DeFi intents (gossip, solvers, standardized formats) to the richer intent vocabulary that community economies require (needs, offers, conditional commitments, mapping workshop outputs).

---

## 1. Motivation

The CPP whitepaper already describes **pool-level rebalance intents** (Chapters 5.2, 8.1): pools publish target inventory bands, caps, and routing preferences so clearing agents can search for multilateral cycles that rebalance inventory across the network. This is slated for v1.1 on the roadmap but is not yet formalized as a data structure or implemented in contracts or simulation — the simulator uses hardcoded pool config parameters rather than published intent objects.

This proposal **generalizes the intent concept** the whitepaper envisions for pools to also include **users and communities**, and proposes a concrete format and agent architecture for both. The motivation:

- **CPP routing is synchronous**: if no multi-hop path exists at query time, the desire evaporates. No signal persists. No one learns that the swap was wanted.
- **Pool stewards and LPs receive no demand signal** to inform listing, inventory, and liquidity decisions.
- **Unmet needs cannot participate in batch netting** — the clearing algorithm optimizes pool inventories without knowing what users actually want.
- **Mapping workshops and community assemblies produce offers and needs** that don't fit the swap form ("I have A, want B") — they need a richer intent vocabulary.

---

## 2. Intent Types

Intents should not be limited to the swap form ("I have A, want B"). Mapping workshops, community assemblies, and everyday economic life produce a richer set of signals:

### 2.1 Swap Intent

"I have 500 units of A and want B, at a rate no worse than X, within 7 days."

This is the direct extension of the current RFQ — but persisted as a standing order.

### 2.2 Want / Need Intent

"I need transport capacity (voucher class B). I am open to what I offer in return."

The user declares a **need** without specifying the input asset. The routing system (or agent) must discover what the user holds and find a viable path. This is the most natural form for mapping workshop outputs — a community says "we need X" without necessarily knowing what they'd swap for it.

### 2.3 Offer Intent

"I have 40 hours of ecological monitoring available (voucher class A). Open to offers."

The user declares **capacity** without specifying what they want in return. This makes surplus capacity visible to the network, enabling the routing system to match it with needs elsewhere.

### 2.4 Conditional Intent

"I would commit to providing B if at least 3 others in my landscape group also commit."

Conditional intents support **threshold activation** — commitments that only become active when enough participants join. This is relevant for collective action problems (e.g., a community water project that only makes sense at a minimum scale).

---

## 3. Intent Format (Sketch)

```
Intent {
  id:             unique identifier
  type:           SWAP | WANT | OFFER | CONDITIONAL
  issuer:         user or pool address
  token_in:       asset offered (optional for WANT type)
  token_out:      asset desired (optional for OFFER type)
  amount_range:   { min, max }
  rate_bounds:    { min_rate, max_rate } (optional)
  expiry:         timestamp or duration
  constraints:    {
    pool_allowlist:   [pool_ids]       (optional)
    pool_denylist:    [pool_ids]       (optional)
    max_hops:         int              (optional)
    max_fee_rate:     float            (optional)
    landscape_group:  string           (optional, for bioregional routing)
  }
  condition:      expression (for CONDITIONAL type)
  visibility:     PUBLIC | GROUP | PRIVATE
  criteria:       {                              (optional, for richer matching)
    question_set:   question_set_id              (ref to commons-governed question library)
    answers:        { question_id: answer }       (issuer's self-description)
    requirements:   { question_id: requirement }  (what the issuer wants in a match)
  }
  metadata:       {
    source:         "mapping_workshop" | "app" | "agent" | ...
    description:    human-readable description
    tags:           [string]
  }
}
```

---

## 4. Agent Roles

### 4.1 User Agent (Intent Manager)

Each user's agent:
- Holds **state about unfulfilled desires** across sessions.
- Monitors the network graph (pool inventories, listings, new pools, rebalancing activity).
- **Executes routes** when conditions change such that a path becomes viable.
- Manages intent lifecycle (creation, modification, expiry, fulfillment).

### 4.2 Clearing Agent (Extended)

The existing NOAM clearing algorithm finds cycles across pool inventories. With intent publication, the clearing agent can extend its graph to include **user intents as virtual edges**:

- A WANT intent for asset B creates a virtual "demand edge" at every pool that lists B.
- An OFFER intent for asset A creates a virtual "supply edge" at every pool that lists A.
- The cycle finder can now discover matches that include both pool rebalancing *and* user desires in the same cycle.

This means a user's unfulfilled need can be resolved as a side-effect of a batch netting run — the clearing agent routes inventory to where users need it, not just to where pools want it.

### 4.3 Matchmaker Agent

Operates across user agents:
- If Alice's agent publishes WANT(B) and Bob's agent publishes OFFER(B), the matchmaker discovers the potential match.
- Coordinates **intent-level netting**: matching desires before they become on-chain swaps.
- Still routes through pools (enforcing registry/limits/fee/inventory constraints), but pre-arranges counterparty discovery off-chain.

### 4.4 Demand Signal Aggregator

Aggregates unfulfilled intents into **market-making signals**:
- "40 users across 3 landscape groups need transport vouchers but no path exists."
- Pool stewards see this signal and can decide to list transport vouchers, seed inventory, or adjust their value index.
- LPs see where liquidity is needed and can direct capital to high-demand gaps.

This closes the feedback loop: **unmet needs shape network topology**, rather than users passively waiting for pools to happen to stock what they want.

---

## 5. Integration with Bioregional Mapping

### 5.1 Mapping Workshops as Intent Sources

The Regenerate Cascadia landscape mapping workshops (May–July 2026) produce structured outputs:
- **Relationships**: Who trusts whom, who works with whom.
- **Projects**: What regenerative work is happening in each landscape.
- **Gaps**: What capacity is missing — transport, food processing, ecological monitoring, etc.
- **Offers**: What people and projects can provide.

These map directly to intent types:
- Gaps → WANT intents
- Offers → OFFER intents
- Projects with interdependencies → CONDITIONAL intents
- Relationships → trust edges that inform routing preferences (pool allowlists)

### 5.2 From Mapping to Routing

The sensing → meaning → caring → committing → coordinating → learning spiral described in the [Commitment Economy Vision](https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning/blob/main/docs/foundations/commitment-economy-vision.md):

1. **Sensing** (mapping workshops): Produce raw offers, needs, relationships, gaps.
2. **Committing**: Structured as typed intents with state machines and audit trails.
3. **Coordinating**: Intents feed into the routing/clearing system. Agents discover paths across landscape groups.
4. **Learning**: Evidence of fulfillment (kept commitments, redeemed vouchers) feeds back into governance and the next mapping cycle.

### 5.3 Cross-Landscape Discovery

Ten landscape groups mapping simultaneously creates a **federated intent graph**. A need in one landscape might be fulfillable by capacity in another — but neither group would know without the routing layer. Agent-mediated intent matching across landscape groups is where commitment pooling's federation model meets bioregional knowledge commoning.

The `landscape_group` constraint in the intent format allows communities to control visibility:
- `PUBLIC`: Visible to all landscape groups (maximum routing opportunity).
- `GROUP`: Visible only within the issuer's landscape group (local-first).
- `PRIVATE`: Visible only to the issuer's agent (for background monitoring).

---

## 6. Privacy Considerations

Publishing "I want B" reveals information about the user's position and needs. Mitigations:

- **Visibility controls**: Intents can be PUBLIC, GROUP, or PRIVATE.
- **Bilateral reveal**: When intents carry criteria (§3), a stronger privacy mode is possible — parties only see each other when both satisfy the other's requirements. This follows [RegenCHOICE](https://wiki.simongrant.org/doku.php/ch:how_it_works)'s correspondence model: "you only get to see other people when you are interested in them *and* they in you." Sensitive criteria answers are never exposed to non-matching parties.
- **Progressive disclosure**: Even after a bilateral match, information is revealed in stages — criteria fit first, then details, then contact — with either party able to withdraw at any stage. See RegenCHOICE [Finding contacts](https://wiki.simongrant.org/doku.php/ch:finding_contacts).
- **Aggregation**: Demand signals can be published in aggregate ("N users want B") without revealing individual positions.
- **Agent-to-agent negotiation**: Matchmaker agents can discover bilateral matches without publishing intents to a public registry — using private set intersection or similar techniques.
- **Expiry**: Intents have bounded lifetimes and are garbage-collected.
- **Unanswered-question feedback**: When a match fails due to missing criteria answers, the system can surface *which* unanswered questions would improve matchability — without revealing who asked. This "iffit" mechanism (from RegenCHOICE [Processing](https://wiki.simongrant.org/doku.php/ch:processing)) helps users improve their intents iteratively without exposing the intent graph.

---

## 7. Relationship to Existing Protocol

This proposal **formalizes and generalizes** what the whitepaper already envisions:

- **Pool rebalance intents** (whitepaper Ch. 5.2, roadmap v1.1): Currently described but unimplemented. This proposal provides a concrete format that covers pool intents as a special case — a pool's rebalance intent is an OFFER/WANT intent where the issuer is a pool address rather than a user.
- **SwapPool / SwapRouter / Registry / Limiter / Quoter**: Unchanged. All routes discovered via intents still execute through pools with all existing constraints. Intent routing is an off-chain coordination layer.
- **NOAM Clearing**: Extended to include user intents as virtual edges in the clearing graph, alongside pool rebalance intents.

The intent layer is an **off-chain coordination service** that improves the inputs to on-chain execution, not a modification of the execution layer itself.

---

## 8. Related Work

### 8.1 Will Ruddick's "Physics of Intention"

Will Ruddick's [A Physics of Intention](https://willruddick.substack.com/p/a-physics-of-intention) develops a framework where declared commitments are measurable system primitives. Key concepts:

- **Intention density**: commitments made / fulfilled over time — a quantitative measure of a community's coordination capacity.
- **Trust as mass**: fulfilled promises generate stabilizing force; unfulfilled ones create voids.
- **Promises circulate**: commitments flow through a system like water — when circulation fails, "intention becomes control" (governance capture).
- **Relational memory**: trust heat maps, flow charts of vouchers, relational density overlays — the system learns from kept commitments.

This framework treats intents not as trade orders but as **expressions of care with observable fulfillment history**. Vouchers are "symbolic representations of intent within the commons." The CPP whitepaper operationalizes this: pools curate commitments, routers discover fulfillment paths, and the fee waterfall sustains the infrastructure.

Ruddick's work does not reference the DeFi intent discourse (Anoma, ERC-7683, etc.), and that discourse does not reference commitment pooling. The convergence is organic — both traditions independently arrived at the insight that **coordination improves when desires are declared, persisted, and matched by agents**. But they optimize for different things: DeFi intents optimize execution efficiency; Ruddick's intention physics optimizes relational density and care circulation.

### 8.2 RegenCHOICE (Simon Grant)

[RegenCHOICE](https://wiki.simongrant.org/doku.php/ch:index) is a bilateral matchmaking protocol conceived in 1993 by Simon Grant, designed to connect people based on mutual criteria satisfaction. It comes from a different tradition than either DeFi intents or commitment pooling — matchmaking, HR, and community connecting — but contributes three ideas directly applicable to this proposal:

**Bilateral correspondence.** Parties only see each other when both satisfy the other's requirements ([How it works](https://wiki.simongrant.org/doku.php/ch:how_it_works), [USPs](https://wiki.simongrant.org/doku.php/ch:regenchoice_usps)). This is a stronger privacy guarantee than one-sided discovery — you can't learn about someone's needs unless you also match theirs. Applied here: WANT and OFFER intents with criteria could use bilateral reveal as an optional privacy mode (§6).

**Commons-governed question library.** Communities of practice maintain structured question sets for their domain ([Question system](https://wiki.simongrant.org/doku.php/ch:question_system)). A network of organic agriculture organizations curates questions about knowledge and skills; a watershed group curates questions about ecological monitoring capacity. Applied here: landscape groups maintain criteria question sets that enrich WANT/OFFER matching beyond token types — "Do you have eDNA sampling experience?", "Are you available spring/summer?", "Can you work within the Salish Sea watershed?"

**Unanswered-question feedback (iffit).** When a match fails due to missing answers, the system surfaces which questions would improve matchability — without revealing who asked ([Processing](https://wiki.simongrant.org/doku.php/ch:processing)). Applied here: when a WANT intent goes unfulfilled, the system can tell the issuer "answering these 3 questions would connect you to potential matches" — improving intent quality iteratively.

RegenCHOICE also proposes a [federated network architecture](https://wiki.simongrant.org/doku.php/ch:network_notes) with hierarchical levels (belonging → community of practice → server → global), governed by sociocracy. This maps to BKC's KOI-net topology (leaf → coordinator → federation) and CLC's confederation model.

### 8.3 DeFi Intent-Centric Architecture

"Intent-centric architecture" has become a significant design pattern in crypto, driven by UX complexity, MEV extraction, and liquidity fragmentation. The core idea is shared with this proposal: **users declare desired end states, not execution steps**. But the application context differs.

**[Anoma](https://anoma.net/blog/an-introduction-to-intents-and-intent-centric-architectures)** is the most architecturally ambitious. It treats intents as the atomic unit of the entire system — not just for trading but for any on-chain/off-chain activity:

- **Intent gossip network**: P2P layer where intents propagate (like a mempool for desires rather than transactions).
- **Solvers**: Competitive agents who combine multiple intents into balanced transactions.
- **Counterparty discovery**: A first-class decentralized process, separated from settlement.

Anoma's solver/gossip/settlement separation maps well to our User Agent / Matchmaker / Clearing Agent roles. Their gossip network is a useful reference for intent registry architecture (Open Question #1).

**[ERC-7683](https://www.erc7683.org/)** (UniswapX / Across) is a cross-chain intent standard. Users sign a structured order ("swap X for Y across chains"), and competitive "fillers" bid in a Dutch auction to execute it. The standard unifies the filler network so the same solvers can serve multiple protocols. ERC-7683's intent format is a practical reference for our format sketch — though our intent types are richer (WANT, OFFER, CONDITIONAL have no ERC-7683 equivalent).

**[CoW Protocol](https://cow.fi)** uses batch auction-based intent matching with **coincidence-of-wants** matching where peer-to-peer trades bypass AMMs entirely. This is the closest DeFi analogue to our intent-level netting concept (§4.3).

### 8.4 Convergence and Divergence

| | DeFi Intents | Ruddick / CPP | RegenCHOICE | This Proposal |
|---|---|---|---|---|
| **Core question** | How do we execute trades efficiently? | How do we make commitments circulatable? | How do we find compatible people? | How do we make community needs and offers legible to routing? |
| **What is an intent?** | A signed order specifying desired end state | A declared commitment backed by time, energy, or resources | An enquiry: criteria answers + requirements | SWAP, WANT, OFFER, or CONDITIONAL — typed, with optional criteria |
| **Agents** | Competitive profit-maximizing solvers | Routers/clearing agents serving pool constraints | Processing servers checking bilateral fit | Matchmakers, demand signal aggregators, community-serving agents |
| **Matching** | Global permissionless solver market | Multilateral cycle-finding across pools | Bilateral correspondence — mutual satisfaction only | Federated, with bilateral reveal and community-sovereign visibility |
| **What gets optimized** | Price, MEV protection, cross-chain execution | Settlement velocity, intention density | Compatibility quality, minimal question burden | Coordination legibility — unmet needs shape network topology |
| **Privacy model** | Public mempool (intents visible to all solvers) | On-chain (inherently public) | Bilateral reveal + staged disclosure | PUBLIC / GROUP / PRIVATE + bilateral reveal mode |
| **Sources** | Wallet interactions, trading interfaces | Pool steward configuration | Structured question responses | Mapping workshops, community assemblies, everyday economic life |
| **Feedback** | Transaction settlement | Kept commitments build trust mass | Unanswered-question prompts (iffit) | Evidence of fulfillment + iffit feedback |

Four traditions, one structural insight: coordination improves when desires are declared, persisted, and matched by agents. DeFi intents contribute architectural patterns (gossip, solvers, standardized formats). Ruddick contributes the design center (intents as expressions of care, not trade orders). RegenCHOICE contributes the matching discipline (bilateral correspondence, criteria commons, progressive disclosure). This proposal synthesizes all three for community economies.

---

## 9. Open Questions

1. **Intent registry architecture**: Centralized service, gossip protocol (à la Anoma, §8.1), or per-landscape-group registries with federation?
2. **Incentives for clearing agents**: Should agents that fulfill intents earn a routing fee? How does this interact with the existing fee waterfall?
3. **Commitment vs. intent**: When does a WANT intent become a binding commitment? What are the state transitions?
4. **MEV / front-running**: If intents are public, can adversarial actors extract value by front-running fulfillment? CoW Protocol's batch auction approach (§8.3) is one mitigation pattern.
5. **Integration with flow funding**: Could WANT intents that represent basic needs be prioritized by the flow funding mechanism described in the commitment economy vision?
6. **Threshold activation UX**: How do conditional intents get presented to users in mapping workshops? What does the facilitation look like?
7. **ERC-7683 compatibility**: Should the intent format be designed to be bridgeable to ERC-7683 (§8.2) for cases where CPP pools interact with DeFi liquidity venues?

---

## 10. Next Steps

- [ ] Review with Will Ruddick and CLC protocol team
- [ ] Prototype intent format as part of the CLC simulation (extend NOAM with virtual edges)
- [ ] Design mapping workshop → intent pipeline for Regenerate Cascadia pilot (May–July 2026)
- [ ] Evaluate privacy-preserving matchmaking approaches
- [ ] Draft MCC extension for intent publication (Chapter 8.1.1 addendum)
