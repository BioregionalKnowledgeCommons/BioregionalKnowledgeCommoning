# Submission Pack — Celo V2 + Synthesis Hackathons

Ready-to-paste blurbs, tweet copy, and demo video shot list.
All grounded in the same story. Adapt per track, don't rewrite.

---

## What We Built

A nursery in Victoria pledges seedlings. An AI agent structures the commitment — typed offers, wants, and limits. A routing scorer matches it to stewarded pools across the Salish Sea and Front Range. Stewards curate what fits. Evidence is linked when seedlings arrive. A proof pack captures the full loop — who promised, who curated, who verified, what was delivered — anchored on Regen Ledger and attested on Celo EAS.

Underneath is a federated knowledge graph: 2,759 entities, 23 active types, 39 semantic predicates across 4 bioregional nodes. The graph is what makes routing contextual — bioregion proximity, semantic taxonomy overlap, seasonal fit, governance compatibility — not just token-pair adjacency.

This serves real communities. The Victoria Landscape Group — part of Regenerate Cascadia's Hub Cultivator program, 9 landscape groups across 3 eco-regions, 35 stewards, $80K flowing to place-based regenerative work — is entering its bioregional mapping and flow funding phase. The mapping workshops that this phase describes are the exact input to our commitment extraction pipeline. The GiftableToken and SwapPool contracts deployed here are Grassroots Economics contracts — the same codebase running the Sarafu Network (26K users, 188 pools, $320K+ swap volume, 1,200 acres restored on Celo mainnet).

The next time someone in Cascadia needs native seedlings, the knowledge graph already knows who delivers and who vouched for them. Trust compounds. The commons remembers.

---

## Track-Specific Blurbs

### Synthesis Open Track — "Agents That Cooperate"

Octo is an AI agent that helps bioregional communities cooperate through structured commitments. It operates on a federated knowledge graph — 2,759 entities, 23 types, 39 semantic predicates across 4 bioregional nodes (Salish Sea, Greater Victoria, Cowichan Valley, Front Range). The agent extracts offers, wants, and limits from natural language, routes them to stewarded pools with a deterministic 5-factor scorer, and proves fulfillment through dual-chain attestation (Regen Ledger + Celo EAS). Four nodes share entities through a consent-aware membrane — trust through kept promises, not token mechanics. The sensing-to-learning loop closes: proof of kept commitments feeds back into the knowledge graph, informing the next cycle of routing. Nine landscape groups across Cascadia are entering their mapping phase this month. The graph remembers who delivered and who vouched.

### Celo (Synthesis Partner Track)

Victoria Commitment Vouchers (VCV) are GiftableTokens on Celo mainnet — the same contract pattern running the Sarafu Network (26K users, 188 active pools, $320K+ swap volume). 33,400 VCV minted from 23+ verified commitments. A multi-participant TBFFSettler redistributed 3,000 VCV across 3 wallets matching needs-weighted thresholds. A BKC SwapPool enables VCV-cUSD exchange. Dual-chain EAS attestation with three-way content hash verification. BKC adds what pure on-chain routing doesn't have: a federated knowledge graph that sees the bioregion, the steward, the seasonal window, the consent boundary — contextual routing intelligence upstream of settlement. Built for the Victoria Landscape Group, a real seed group in Regenerate Cascadia's Hub Cultivator program entering its flow funding phase.

### Protocol Labs — "Let the Agent Cook"

Octo runs a complete autonomous decision loop on production infrastructure: (1) Discover — transcribe a mapping workshop audio recording via Whisper (203s in 9.6s), (2) Plan — extract 10 commitment candidates (5 offers + 5 needs) via GPT-4o-mini with few-shot prompting, (3) Execute — create commitments on a federated knowledge graph, route to pools, verify qualifying pledges, mint VCV tokens on Celo mainnet, (4) Verify — TBFF settlement with 3-participant redistribution (3,000 VCV, converged in 2 iterations), (5) Submit — anchor proof to Regen Ledger, attest on Celo EAS with three-way hash verification. Safety: consent membrane filters 34 query sites, node_private visibility scope prevents sensitive commitments from reaching on-chain, deterministic scorer (no black-box ML) produces transparent, auditable routing suggestions. The agent also participates as an economic actor — registering its own offers and needs. The full loop runs unattended via `demo-full-loop.sh`.

### Protocol Labs — "Agents With Receipts"

Octo is registered as ERC-8004 agentId 1855 on 8004scan (Celo mainnet). Every step in the commitment routing pipeline produces verifiable on-chain receipts: VCV mint transactions (`0xbe1f12...`), TBFF settlement transactions (3 participants, real VCV redistribution), Celo EAS attestation UIDs (`0xf6597a...`) with content-hashed proof packs, and CAT (Content Addressable Transformation) receipt chains linking every transformation back to source. The agent's A2A card at `/.well-known/agent.json` exposes 15 tools for programmatic interaction. `agent_log.json` captures the full execution trace keyed to ERC-8004 agent identity.

Vision: Our federation topology is already an agent trust graph — 4 nodes with explicit edge-approval governance, consent-aware data flow, and capability-scoped sharing. ERC-8004 as a graph register would make this legible on-chain: agents as nodes in a capability/trust graph, not flat metadata. The `broader` edge from Salish Sea to Cascadia is a trust relationship between bioregional agents.

### Octant — PG Data Collection

The Bioregional Knowledge Commons is a public goods data infrastructure: 2,759 entities across 4 federated nodes collecting bioregional knowledge — organizations, projects, locations, practices, commitments, evidence. 23 entity types and 39 semantic predicates structure relationships between watershed stewards, First Nations partnerships, restoration practices, and community coordination. The knowledge graph IS the public good: structured, federated, consent-governed bioregional knowledge. MediaWiki import densified from the Salish Sea Wiki. Every entity is discoverable, queryable, and federable across bioregion boundaries while respecting consent boundaries (34 filtered query sites, node_private visibility scope).

### Octant — PG Data Analysis

The commitment routing scorer analyzes public goods contributions through 5 deterministic factors: bioregion proximity (is this commitment geographically relevant?), offer/need taxonomy overlap (does the semantic content match?), timeframe alignment (seasonal fit?), capacity fit (can the pool absorb this?), and governance compatibility (do curation standards align?). Each factor produces a transparent, auditable score — no black-box ML. The scorer enables communities to discover where their capacity is most needed, routing public goods commitments to the pools where they'll have the greatest impact. The `broader` predicate enables cross-bioregion routing: a commitment in the Salish Sea can match Cascadia-wide pools at +15 umbrella match.

### Octant — Mechanism Design for PG Evaluation

Threshold-Based Flow Funding (TBFF) is a mechanism for evaluating and distributing public goods commitments. Participants set maximum thresholds ("lake levels") — overflow redistributes to chosen recipients via weighted allocation preferences. Converges in 1-4 iterations. Deployed on Celo mainnet as TBFFSettler (`0x2a13c4eB...`) with 3 participants: Darren (individual steward), Victoria Landscape Hub (landscape group), Kinship Earth (bioregional funder). 3,000 VCV redistributed with post-settle balances matching thresholds exactly. Settlement events write back to the knowledge graph as Evidence entities, creating an auditable record of how public goods funding was evaluated and distributed. The mechanism is deterministic, needs-weighted, and transparent.

### Celo V2 — Best Agent

Bioregional Commitment Routing brings real-world utility to landscape groups entering their mapping and flow funding phase — 9 groups across 3 eco-regions in Regenerate Cascadia's Hub Cultivator program. The agent extracts commitments from mapping workshop conversations, routes them with a deterministic scorer grounded in a federated knowledge graph (2,759 entities, 4 nodes), and settles them as VCV tokens on Celo mainnet. Economic agency: 33,400 VCV minted, 3,000 VCV redistributed via TBFF, VCV-cUSD swap via GE SwapPool. BKC maps onto all 4 CLC (Cosmo-Local Credit) interfaces — Curation, Valuation, Limitation, Exchange — positioning as routing intelligence for a production commitment pooling network with proven scale (Sarafu: 26K users, 188 pools).

### Celo V2 — Best Agent Infrastructure

KOI federation protocol: 4 bioregional nodes (Salish Sea coordinator, Greater Victoria, Cowichan Valley, Front Range) with holonic architecture, ECDSA-signed envelopes, event-driven replication, and consent-aware membrane governance (edge-approval gating, visibility scope filtering, 34 query sites reconciled). Commitment routing scorer: 5-factor deterministic scoring (bioregion/overlap/timeframe/capacity/governance, max 100). BFF pattern: server-side aggregation with bounded concurrency (max 5) and 30s cache across all 4 nodes. Deployment pipeline: vendor pin at canonical SHA, deploy.sh with rsync + migration + systemd restart, health check with rollback. ERC-8004 agent identity (agentId 1855) with A2A card exposing 15 tools.

### Venice (Conditional)

Community conversations are private. Mapping workshops involve sensitive topics — Indigenous land rights, restoration commitments, organizational capacity. Octo's consent-aware architecture ensures private cognition produces trustworthy public action: AI extraction happens on private infrastructure using Venice no-retention models (Llama 3.3 70B — fully private, no data retention). The consent membrane (34 filtered query sites, node_private visibility scope) ensures only what the community explicitly consents to goes on-chain. The pipeline: private community conversation → private Venice inference → consent-gated knowledge graph → public on-chain proof (VCV tokens, EAS attestation). Venice is load-bearing: without private inference, sensitive community data would flow through retention-enabled providers, undermining the consent architecture that makes commitment routing trustworthy.

---

## Tweet Copy

```
Bioregional Commitment Routing — AI agents extract commitments from community conversations, route them through a federated knowledge graph (2,759 entities, 4 nodes), and prove them on Celo mainnet.

@kaborahq: https://www.karmahq.xyz/project/bioregional-commitment-routing
8004scan: https://www.8004scan.io/agents/celo/1855

Built on @Celo with VCV tokens, TBFF settlement, EAS attestations.

@CeloDevs @CeloPG #CeloV2Hackathon
```

Note: May need to shorten for 280-char limit. Core elements: project name + knowledge graph + Celo + links + tags.

**Short version (under 280 chars):**
```
Bioregional Commitment Routing — federated knowledge graph + AI agents + commitment pooling on @Celo mainnet. 2,759 entities, 4 nodes, real VCV settlements.

Karma: karmahq.xyz/project/bioregional-commitment-routing
8004scan: 8004scan.io/agents/celo/1855

@CeloDevs @CeloPG
```

---

## Demo Video Shot List (90-120s, story-centric)

| Time | Story Beat | Screen Content |
|------|-----------|----------------|
| 0-10s | "A landscape group in the Salish Sea maps what their community can offer and what it needs." | BKC Knowledge Garden homepage at `salishsee.life`. Quick glimpse of entity browser showing real organizations. |
| 10-25s | "An AI agent extracts commitments from a mapping workshop conversation." | `/commons/commit` — show transcript input, extraction output with typed offers/wants/limits. Show the voice memo → structured commitment flow. |
| 25-40s | "A deterministic routing scorer suggests which pools match." | `/commons/routing` — force-directed graph. Click a commitment node to show detail panel. Click an edge to show 5-factor score breakdown (bioregion 30, overlap 10, timeframe 15, capacity 20, governance 0). |
| 40-55s | "Stewards curate, verify, and mint commitment vouchers on Celo." | Celoscan: VCV token address `0x4CDb98Ff...`, a mint TX. Show GiftableToken = Grassroots Economics contract pattern. |
| 55-70s | "Threshold-based flow funding redistributes capacity across 3 participants." | Settlement results: 3 participants (Darren, Victoria Hub, Kinship Earth), 3,000 VCV, 2 iterations, post-settle balances matching thresholds. |
| 70-85s | "Proof packs anchor on Regen Ledger and Celo EAS." | celo.easscan.org attestation view. Show three-way content hash match (BKC, Regen, Celo). |
| 85-100s | "The knowledge graph remembers. Next time someone in Cascadia needs native seedlings, it knows who delivers." | `/commons/routing` — show the broader edge connecting Salish Sea to Cascadia. The learning layer. |
| 100-115s | "4 federated nodes. 2,759 entities. 9 landscape groups starting their mapping phase. Trust compounds. The commons remembers." | Quick montage: entity browser, pool status, flow funding viz. End on BKC logo/tagline. |

---

## On-Chain Artifacts (for submissions)

| Artifact | Address / Link |
|----------|---------------|
| VCV Token (GiftableToken) | [`0x4CDb98Ff88af070b1794752932DbAD9Edf7a1573`](https://celoscan.io/address/0x4CDb98Ff88af070b1794752932DbAD9Edf7a1573) |
| TBFFSettler (multi-participant) | [`0x2a13c4eB94Fe5b5E93c1Fe380bC9Af3f72Cb3faF`](https://celoscan.io/address/0x2a13c4eB94Fe5b5E93c1Fe380bC9Af3f72Cb3faF) |
| BKC SwapPool | [`0x181E36AD6ae826b75e739C3510Bd059b27C34aB4`](https://celoscan.io/address/0x181E36AD6ae826b75e739C3510Bd059b27C34aB4) |
| EAS Attestation | [`0xf6597a...`](https://celo.easscan.org/attestation/view/0xf6597a662d2d94aeab6b2ebe747df0ef7dd60df6cd91eba540cf60fa73666298) |
| EAS Schema | [`0xdcf86a...`](https://celo.easscan.org/schema/view/0xdcf86a36ec6ec644e7727f9e1c7290b38f7f8503b051b893774cdd52573ee1e0) |
| 8004scan Agent | [agentId 1855](https://www.8004scan.io/agents/celo/1855) |
| Agent Wallet | `0x6f844901459815A68Fa4e664f7C9fA632CA79FEa` |
| Karma Project | [Bioregional Commitment Routing](https://www.karmahq.xyz/project/bioregional-commitment-routing) |

## Live Demo URLs

| Page | URL |
|------|-----|
| Knowledge Garden | https://45.132.245.30.sslip.io |
| Routing Visualization | https://45.132.245.30.sslip.io/commons/routing |
| Commitments Dashboard | https://45.132.245.30.sslip.io/commons/commitments |
| Create Commitment | https://45.132.245.30.sslip.io/commons/commit |
| Pools | https://45.132.245.30.sslip.io/commons/pools |
| Flow Funding | https://45.132.245.30.sslip.io/commons/flow-funding |

## Repos (open source)

| Repo | Purpose |
|------|---------|
| [BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning](https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning) | Governance, protocol foundations, pilot docs |
| [BioregionalKnowledgeCommons/bioregional-commons-web](https://github.com/BioregionalKnowledgeCommons/bioregional-commons-web) | Web dashboard (Next.js, routing viz, flow funding) |
