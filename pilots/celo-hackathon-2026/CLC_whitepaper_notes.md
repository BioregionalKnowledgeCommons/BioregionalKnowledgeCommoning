# CLC Whitepaper Notes (from reading /Users/darrenzal/projects/cosmo-local-credit/docs)

## Initial Resonance

Cosmo local credit is described almost like Visa / Mastercard for vouchers and obligations, but governed as a commons. That is interesting because I have also been describing my own project as a commons, but for bioregional knowledge.

## Key Quotes and Reflections

### Commitment-First Clearing

> "This is commitment-first clearing"

> "Commitment Pools are shared markets where people can swap redeemable commitments and settle them over time."

> "A 'commitment' can be any redeemable obligation"

> "The CLC DAO (a member-governed Decentralized Autonomous Organization (DAO) with transparent rules) is the network-level 'commons steward' that funds and governs the safety layer for many independent Commitment Pools, so commitment pooling can scale without becoming extractive or fragile. In practice, it becomes a credit routing + clearing layer across many issuers - so different communities and institutions can settle obligations with each other without needing one central bank-like operator."

> "Mission (North Star): maximize the velocity of settlement of outstanding commitments (how quickly listed promises become fulfilled) while preserving care, fairness, and resilience. (Metric: settlement velocity, fulfillment rate, redemption latency.)"

**Reflection**

I am curious about the timing and flow of settlement. Some commitments might have a preferred date of settlement in the future. Might there be algorithms that optimize the sequence of settlement through networks? Could there be ways of ordering settlements such that they maximize net positive value? Not sure, just thinking out loud.

### Bioregional Mesh Potential

> "When two pools list overlapping obligations, value can route across pools (multi-hop), and the network clears by netting flows and using shared liquidity and off-ramps (ways to convert to local currency/stables when needed) to reduce settlement delays. This is important because it turns fragmented obligations (thousands of small issuers) into a usable economic fabric - so people can pay, trade, and fulfill needs even when no single issuer is universally trusted or universally liquid."

**Reflection**

This seems useful for bioregionalism. Each local region could have its own knowledge commons and pools, and then they can be meshed together at larger scales.

### CPP as the Core Primitive

> "Commitment Pooling Protocol (CPP): The Core Primitive
> Mental model: A Commitment Pool is like a small, governed clearing house for community 'gift cards' (vouchers). People deposit vouchers or reserve assets, exchange them under published rules, and redeem them for real goods/services. The software enforces limits and keeps receipts so disputes and guarantees can be handled transparently. CLC connects many pools so vouchers can find redemption paths beyond a single community."

**Question**

In Sarafu, communities make their own commitment pools, but they are mostly not connected. So is the CLC DAO trying to be the mesh network that connects them?

> "CPP on Sarafu.Network today enables interoperability but lacks:
>
> a mechanism for LPs to inject liquidity across pools and access sCLC, and
> decentralized decision-making as the network scales.
> CLC DAO addresses both by introducing a network clearing house (the CLC Pool) and a governance token (CLC)"

### Use Cases Beyond Typical DEX Logic

> "Most decentralized exchanges (automated trading pools) rely on bilateral token pairs, continuous curves, and volatility-driven fees. CPP supports those use cases and enables low-frequency, high-impact coordination:
>
> Community savings (VSLAs),
> Production financing,
> Mutual credit and mutual aid,
> Insurance and guarantees,
> Lending against real output,
> Settlement of personal and institutional debts,
> Portfolio-directed liquidity (e.g. curated pools for ecosystem services, humanitarian support, and health & wellness)"

### Routing as a Service

> "5.2 Routing as a Service: Pathfinding + Rebalancing (Liquidity-Saving)
> In CLC Network, 'routing' is not only a user-facing convenience ('swap voucher A for voucher B'). It is also a network liquidity service that increases settlement velocity by improving how inventory is distributed across pools and by surfacing multilateral netting opportunities."

Two routing modes:

1. End-user routing (on-demand)
   Given `(token_in, token_out, amount, constraints)`, the router discovers a multi-hop path across CPs. A route is valid only if each hop clears: listing and registry checks, value index pricing, swap limiter windows and caps, fee rules, and outgoing inventory availability. Execution is atomic where possible; otherwise HTLC / escrow is used with explicit abort paths.
2. Pool rebalancing / batch netting (scheduled or threshold-triggered)
   Pools may opt-in to publish rebalance intents or standing constraints: target inventory bands by voucher class, maximum deviation vs. the pool's value index, per-epoch caps, and allow / deny routing preferences. Routers and clearing agents then search for multilateral cycles and chains that:
   - satisfy every hop's limits and inventories
   - reduce inventory imbalance across pools
   - maximize total offset value subject to policy constraints

These cycles are executed as batch routes, producing receipts per hop.

**Reflection**

This seems like a great offering of bioregional knowledge commons.

### Roadmap Notes

> "Roadmap (Indicative)
> v1: CLC token launch; CLC Pool; fee adapters; governance MVP (quorum + timelocks).
> v1.1: Router SDK & registry APIs; health dashboards; Insurance Fund policy v1; opt-in rebalance intents + batch netting (cycle-finding) MVP.
> v1.2: Cross-domain routing via HTLC/escrow; guarantor module; tiered limit presets.
> v2: Retail on/off-ramps (via regulated partners), personal micro-pools; compliance plugin marketplace; third-party audits of voucher classes.
> On-ramps: convert fiat -> approved stable cash-equivalents that can seed designated pools.
> Off-ramps: convert approved cash-equivalent stables -> fiat via an approved off-ramp list (bank transfer, e-money issuers, and card-issuing / payment processors on major card rails), with jurisdictional KYC / attestation and geofencing where required.
> Principle: the DAO and CPP pools do not operate fiat rails; ramps are provided by licensed third parties under local regulation."

### Conclusion Excerpt

> "CLC aligns mission-driven liquidity with durable, auditable settlement flows and explicit guardrails. By connecting local production, mutual aid, and lending through interoperable commitment pools (each with clear registries, value indices, swap limits, and accountable stewardship) CLC helps route real redeemable commitments at community scale without relying on opaque leverage. Participants can engage through governance and, where enabled by policy, sCLC provides time-bounded swap access to a defined portion of pooled fees, strengthening resilience through transparency, limits, and shared infrastructure."

## Raw Questions

### BKC + CLC

- CLC DAO is meant to help CPP implementations like Sarafu, right?
- Does it make sense for us to use BKC to build CPP implementations in bioregions that map to the BKCs, and then use the CLC DAO to weave them together?

### DAO vs Protocol vs Confederation

- Why would people join the DAO that CLC is setting up?
- Why would they not implement the protocol themselves?
- The code and ideas are open source, right?
- Is CLC meant to be one DAO, or a protocol / framework that anyone can implement?
- Would we be using the code to create our own DAO?
- I see CLC DAO has a token. Why wouldn't Cascadia just make its own CLC DAO with its own token?

From the whitepaper:

> "5.2a Confederation & Interoperability
> CLC is designed as a confederation protocol: many independent networks can run their own registries, routers, and policy layers, while still routing to one another when they share compatible vouchers and standards. This is not a hub-and-spoke monopoly; it is a mesh of overlapping curations."

Interoperability incentives:

- Any fork or network that remains CPP-compatible can route to CLC pools, and CLC routers can route to theirs, increasing settlement paths, inventory reach, and real-world fulfillment velocity for all parties.
- More interoperable networks means more routable paths, which means higher throughput and fee volume from real settlement activity, benefiting LP programs and routing services across the confederation.
- Open-source forkability reduces systemic risk: if any canonical registry or router becomes captured or degraded, communities can re-point or fork without bricking local economies.

Confederation mechanics:

- Multi-profile discovery and explicit user or pool choice of registry roots, or "network profiles"
- Reciprocal routing via mutual allowlists with risk parameters like caps, escrow requirements, and health-score thresholds
- Policy separation: each profile defines its own fee norms, insurance scope, and compliance hooks; routing across profiles must satisfy each hop's stated constraints and inventory

Related note:

> "AGPL + Fork Kit: Confederation rewards compatibility. Networks that fork and improve routers, registry tooling, bridge adapters, or observability can still route with CLC if they remain CPP-compatible - expanding settlement paths and strengthening the whole mesh. AGPL ensures improvements to the shared plumbing remain shareable across the confederation, reducing systemic risk and duplication."

### Bioregional Financing and Portfolio Pools

- In bioregional financing, we talk about stewarding portfolios and networks of projects. We aim to invest in ecosystems and networks rather than isolated things.
- Does this integrate well with commitment pooling?
- Would curated pools of commitments be examples of these portfolios of projects?
- Would being a liquidity provider for a CLC pool be part of the work of doing bioregional financing?
- Is this kind of like underwriting a local network of projects and businesses?

Does this idea of portfolios of projects map onto portfolio pools?

> "Portfolio Pools: Direct Seeding, Voted Allocations, and sCLC-Directed Liquidity (Examples)
>
> Commitment Pools can be curated as 'portfolio pools': pools that list redeemable commitments aligned to a mission domain (e.g. ecosystem support services, humanitarian support, health & wellness). Portfolio pools make it easy for liquidity providers to target real-world outcomes without requiring a single central issuer.
>
> There are three complementary ways to support a specific portfolio pool:
>
> A) Seed directly into the pool: deposit accepted assets or vouchers into the pool's Vault, increasing inventory and routing capacity, subject to listings, limits, and reserve policy.
>
> B) Vote allocations into the pool: propose and approve Liquidity Mandates (Waterfall allocations) that seed or backstop designated portfolio pools with time-bounded mandates and sunset / review.
>
> C) Stake CLC and direct sCLC swaps: when enabled for an epoch, stakers can exercise sCLC budget-exit swaps to reallocate a bounded portion of post-waterfall fee assets into specific portfolio pools, strengthening the pools they believe most improve settlement and mission outcomes. This is an accountability mechanism under caps and windows, not a claim on profits.
>
> Note: Portfolio pools remain sovereign. They can be canonical (discoverable via official registries and routers) or independent (discoverable via independent registries and routers), without changing the underlying CPP primitives."

And:

> "7.3.2 Curating Portfolio Pools (Including Certifications)
> Any steward (individual, cooperative, multisig, or DAO) can curate a portfolio pool: define a listing policy, publish a Value Index method, configure limiters, and require clear redemption proofs and fallback remedies. Portfolio pools can be specialized (ecosystem, humanitarian, health) or mixed.
>
> Certifications can be used to improve trust and reduce risk, but should be modeled as attestations that affect eligibility and risk treatment, not as profit tokens. Two safe patterns:
>
> A) Attestation Certificates (non-transferable or registry-bound): a verifier issues an attestation that a voucher issuer or project meets stated criteria. The pool uses attestations to whitelist listings, adjust haircuts, widen or narrow limits, or qualify for insurance participation.
>
> B) Audit / Verification Service Vouchers (redeemable commitments): a token represents a redeemable verification service. Pools or projects can purchase these vouchers to fund monitoring and strengthen integrity.
>
> In both cases, the economic claim remains the underlying redeemable commitment; certifications modify risk and eligibility rather than creating entitlement to fees, profits, or residual assets."

### Other Open Questions

- I am interested in the ability to create playgrounds where people can make commitments in a test environment, and where there would be a seamless transition between that test environment and the real deployment of commitments, pools, and financing.
- I am interested in the composability of commitments. For example, I might be a skilled manager of agroforestry, so I might want to commit to offer my services in that role, but there are requirements for that. I might need a physical location to work on, other people with other skills, and other prerequisites. Is this type of thinking and design included in the CLC and or Grassroots Economics projects?
- In our bioregional work we do mapping workshops where we gather people locally to map their needs, the needs of the community, and related capacities. I am thinking we could also include mapping commitments in these in-person events and potlucks so people could map lots of different things including what they want to commit to. This could feed into building commitment pools and the wider framework for helping local communities create commitments that can be pooled together through cosmo local credit commitment pools.
- I am familiar with ValueFlows and the Holochain implementation hREA. Does that have any interesting integration points for our project?

## Working Synthesis, Responses, and Guiding Questions

### 1. BKC, Pools, and CLC

CLC does seem to be trying to do exactly this: take CPP implementations like Sarafu and add the network-level mesh layer of routing, liquidity coordination, clearing, governance, and shared safety infrastructure.

One plausible path is:

- BKC helps bioregions map needs, offers, stewards, proofs, and commitments
- local or bioregional pools curate a subset of those commitments into actual commitment pools
- CLC-compatible routing helps weave those pools together across bioregions, regions, and domains

This suggests an important distinction:

- not every commitment in BKC needs to become a pooled or liquid commitment
- BKC can hold a much wider field of intents, commitments, offers, needs, proofs, and social context
- commitment pools would hold the subset that pool stewards consider mature, redeemable, and bounded enough to curate into pooled commitments

### 2. Commitment Lifecycle

Maybe a better framing is not "who is allowed to make commitments?" but "what are the stages a commitment can move through?"

- everyone should be able to create intents
- everyone should be able to make commitments
- commitments can optionally gather attestations, proofs, or steward feedback
- pool stewards decide which commitments to include in pools
- some pooled commitments may then become routable, financed, or settled through CPP / CLC style infrastructure
- after fulfillment or redemption, proofs, reputation, and learning can flow back into BKC

Related clarification:

- attestation does not need to be a prerequisite for a commitment to exist
- attestation may not even need to be a prerequisite for pool inclusion
- pool stewardship itself is the curation layer
- attestations and proofs could instead be useful signals to pool stewards and perhaps later to routing, limits, haircuts, insurance eligibility, or portfolio design

So maybe one useful design distinction is:

- commitment creation is open
- pool inclusion is curated
- attestation is optional but valuable as signal
- routing, financing, and insurance may use those signals more strongly than basic pool inclusion does

### 3. Pool Eligibility

On "what makes a commitment pool-eligible in a bioregion?" this probably should not be answered once globally by BKC. It seems more like each pool maintainer, steward, or DAO should define their own listing policy.

But this is still a very good guiding design question for BKC:

- what information should BKC help surface so pool stewards can make good curation decisions?
- redemption terms
- steward identity
- place or bioregional relevance
- supporting proofs
- dependency completeness
- risk flags
- social legitimacy or references

This feels important: BKC may not want to decide what is pool-eligible, but it can help make commitments legible enough that local pool stewards can decide.

### 4. DAO, Protocol, and Network Profile Strategy

CLC seems to be both:

- a canonical DAO or network with its own token and governance
- a confederation-compatible protocol family that others can fork, adapt, and interoperate with

So yes, Cascadia could eventually run its own CLC-compatible network profile or DAO, with its own stewardship, routing preferences, and maybe even token. The question is less "can we?" and more "when does it make sense?"

Near term, it may make more sense to stay open to integration with the CLC DAO if that helps with interoperability, alignment, and learning. Longer term, it may make sense for bioregions to have their own sovereign but interoperable profiles.

Good open strategic question:

- should BKC or Cascadia aim first to integrate with the CLC DAO as a participant, portfolio, or profile?
- or aim to become its own CLC-compatible network profile later, once enough bioregional commitments, pools, and stewards exist?

### 5. Portfolio Pools and Bioregional Financing

The portfolio pool language maps very strongly to bioregional financing. If we say we want to finance ecosystems, portfolios, and networks of projects rather than isolated projects, that sounds a lot like:

- curated pools of place-based commitments
- thematic pools for ecosystem restoration, food systems, housing, care, or watershed work
- liquidity providers effectively underwriting a living portfolio of commitments and relationships

So yes, being a liquidity provider to a pool could be part of bioregional financing. Not in the usual extractive VC sense, but more like underwriting liquidity, confidence, and settlement capacity for a mission-aligned local or bioregional portfolio.

Portfolio pools may be a particularly good bridge concept between:

- bioregional financing
- commons stewardship
- commitment pooling
- mission-directed liquidity

### 6. Proof Packs, Certifications, and Attestations

There is a potentially strong fit here with BKC proof packs:

- BKC proof packs could potentially become an attestation layer that pool stewards use when deciding listings
- later, they might help inform haircuts, limit settings, insurance qualification, or portfolio weighting
- but this is still a question, not something to assume too early

Important open question:

- can BKC proof packs become the attestation layer that CLC portfolio pools use for listings, haircuts, and insurance qualification?

### 7. Routing Objectives

CLC is explicit about settlement velocity, but for bioregional knowledge commons it may be important to ask what else routing should optimize for:

- ecological urgency
- seasonality
- reciprocity
- local resilience
- fairness and inclusion
- care priorities
- strategic development priorities discovered through community mapping

So another strong guiding question is:

- what objectives should routing optimize besides settlement velocity, and how might those objectives be discovered or governed through community mapping or stewardship?

### 8. Time-Aware Planning and Sequencing

On the question about timing, sequencing, and future settlement windows: this still feels underdeveloped in CLC itself. There is clearly logic around expiry, redemption windows, inventory balancing, batch netting, and route constraints. But there seems to be room for a richer time-aware or sequence-aware planning layer, especially for commitments that are best fulfilled in a future season or in a specific dependency order.

This points toward a possible distinction between:

- commitment routing and clearing
- planning, sequencing, and dependency design

The second layer may not be fully handled by CLC alone.

### 9. Playgrounds and Onboarding

This still feels like a strong idea:

- people could create intents and commitments in a low-stakes sandbox
- pool design and stewardship rules could be tested socially before real liquidity is involved
- then especially promising commitments or pools could graduate into live deployments

That could be important for community onboarding and workshops, especially if we want a path from:

- paper or conversational mapping
- digital commitments or intents
- steward curation
- test pools
- live pools, financing, and routing

### 10. Composability, Dependencies, and ValueFlows

On composability, prerequisites, and dependency graphs: this is one of the most interesting gaps.

- CLC seems strong on redeemable commitments, pools, routing, and settlement
- but less strong on modeling dependencies between commitments, prerequisites, recipes, workflows, and staged development

Example:

- "I commit agroforestry management services"
- but that depends on land access, tools, collaborators, nursery stock, financing, and timing
- so there may need to be a layer that models these dependencies before something becomes a pooled or redeemable commitment

This is why ValueFlows or hREA may matter.

ValueFlows / hREA integration point:

- not sure this should be a focus for the next week, since the immediate focus is the Celo hackathon and proving the BKC + commitment pooling + proof story
- but it seems like a very important open architectural question for the longer arc

Rough working stack idea:

- BKC = place-based memory, mapping, steward identity, proof, narrative, legitimacy
- ValueFlows / hREA = intents, commitments, plans, recipes, dependencies, process logic
- CPP / CLC = pooled redeemable commitments, liquidity, routing, settlement, portfolio pools

If that framing is right, then ValueFlows may not be the next-week focus, but it could become the planning and dependency semantics layer that sits upstream of commitment pooling.

Useful working model:

- intent = something someone wants, could offer, or might commit to
- commitment = a real promise
- attestation or proof = optional trust, quality, or verification signals
- pool inclusion = steward-curated decision
- pooled commitment = redeemable and routable commitment in a shared market
- settlement or fulfillment = actual economic completion
- proof pack, reputation, and learning = fed back into BKC

### 11. Community Mapping Workshops

This also suggests that community mapping workshops could be expanded to map:

- needs
- offers
- capacities
- intents
- commitments
- dependencies and prerequisites
- priorities and objectives
- stewarding entities
- candidate portfolio pools

That feels like a very promising bridge between bioregional commoning practice and commitment pooling infrastructure.

### 12. Near-Term Hackathon Framing

- do not over-scope into full ValueFlows integration this week
- keep the architectural question alive
- for now, focus on proving that BKC can help surface and steward commitments, route them into pools, and attach proof or attestation context that could later matter for curation and financing

## Good Next Design Questions

- what minimum commitment schema does BKC need for hackathon scope?
- what signals should BKC surface to help pool stewards decide listings?
- what kinds of proof or attestation are useful immediately, versus later?
- what is the minimum viable lifecycle from commitment creation to pool inclusion to proof of fulfillment?
- when does it make sense to introduce ValueFlows concepts like intents, plans, and dependencies more explicitly?
- what would a Cascadia-specific but CLC-compatible network profile eventually look like?
