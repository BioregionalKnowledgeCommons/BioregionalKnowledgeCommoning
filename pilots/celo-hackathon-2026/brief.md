# Agentic Commitment Routing for Bioregional Swarms on Celo

## One-line

AI agents help communities express offers, wants, and limits — then route commitments into stewarded pools with governance and on-chain provenance.

## The Problem

Bioregional coordination runs on commitments: a nursery pledges native seedlings, a land trust offers monitoring hours, a collective promises mycoremediation labor. These commitments exist today — in conversations, spreadsheets, handshake agreements — but they're invisible to neighboring communities that need exactly what's being offered.

The result: parallel efforts, unmatched capacity, and coordination that scales only as far as personal relationships reach.

## The Insight

Will Ruddick's arc from *Footnotes on Intelligence* traces the loop: **sensing → meaning-making → caring → committing → coordinating → learning**. The ancient patterns are already there — Mweria (Kenyan reciprocal labor), Meitheal (Irish communal work), Chama (East African savings circles). What's missing isn't the protocol. It's the infrastructure to make commitments legible across communities without losing the trust that makes them work.

From *Touching the Knowledge Commons*: the shared memory of kept commitments is the emotional center. From *Honor, Integrity, and the Cost of Keeping Our Word*: trust comes from witnessed follow-through, not token mechanics.

AI and Celo are layers — stewardship is the foundation.

## What We Built

The **Bioregional Knowledge Commons (BKC)** is a federated knowledge graph connecting four bioregional nodes across the Salish Sea and Front Range. It already tracks ~1,005 entities, proves claims with on-chain anchors, and governs data flow through a consent-aware federation membrane.

We extended it with **commitment routing**:

### Agents That Cooperate

An AI agent takes natural language — *"Regenerate Cascadia offers 200 hours of native plant restoration, valued at $8,000, April-September. Wants: soil testing equipment. Limit: max 3 concurrent sites."* — and structures it into a commitment object with typed offers, wants, limits, and routing tags.

A deterministic routing scorer matches commitments to pools based on bioregion proximity, offer/need taxonomy overlap, timeframe alignment, capacity fit, and governance compatibility. No black-box ML — transparent, auditable scoring.

### Agents That Trust

Every commitment carries provenance: who pledged, who verified, who approved routing. State transitions (PROPOSED → VERIFIED → ACTIVE → EVIDENCE_LINKED → REDEEMED) are logged in an insert-only audit trail. Evidence entities link proof of fulfillment. The full chain is assembled into a proof pack — archivable, verifiable, anchored to Regen Ledger.

Steward governance gates every transition. The routing scorer suggests; humans decide.

### Agents That Pay

Threshold-Based Flow Funding (TBFF) settles verified commitments through tiered policy: auto-advance for small amounts, semi-automated for mid-range, manual review for large commitments. Settlement receipts chain back to the original commitment through the knowledge graph.

### Agents That Keep Secrets

A consent-aware visibility scope system (34 query sites filtered across 15 public endpoints) ensures that `node_private` commitments never leak to unauthorized consumers. Communities control what's visible to the network.

## Architecture

```
Natural Language ──→ Agent Draft ──→ Commitment Object
                                         │
                                    Routing Scorer
                                         │
                              ┌──────────┴──────────┐
                              ▼                      ▼
                     Pool A (Victoria)      Pool B (Cascadia)
                              │
                      Steward Approval
                              │
                    Pledge + Threshold Check
                              │
                      ┌───────┴───────┐
                      ▼               ▼
               Evidence Link    Celo Attestation
                      │          (stretch)
                 Proof Pack
```

**BKC is canonical.** The knowledge graph, governance, and routing logic live in BKC. Celo provides settlement and provenance — a layer, not the product.

## Grassroots Economics Alignment

BKC commitment pooling maps directly to the patterns Grassroots Economics has proven at scale with Sarafu Network (3,149 monthly active users, 239 vouchers, 33 pools, 1,200+ acres restored):

| BKC | GE / Sarafu | What it means |
|-----|-------------|---------------|
| Commitment (offers/wants/limits) | Community Asset Voucher (CAV) | BKC adds typed constraints and agent-assisted drafting |
| CommitmentPool + governance | Swap pool + token registry | BKC adds steward governance membrane |
| Evidence + proof pack | CAV redemption receipt | BKC adds cryptographic provenance chain |
| TBFF threshold bands | Token limiter | Similar safety mechanics, different layers |
| Routing scorer | (Manual matching) | New: deterministic multi-factor routing |

**CLC DAO convergence**: Will Ruddick's Credit Loop Commons DAO (white paper in progress) adds multi-hop routing, value index pricing, and netting flows on Celo. Our routing scorer is BKC-native, designed to be CLC-compatible. The integration path is a post-hackathon study (C1), not hackathon scope.

## Demo

Three moments:

1. **Agent drafts commitment** from natural language → structured object with offers, wants, limits, routing tags
2. **Routing suggestion + steward approval** → scorer ranks pools → steward reviews → approves → pledge
3. **Proof + settlement** → evidence linked → proof pack assembled → (stretch) Celo attestation

Works entirely within BKC. No live Celo dependency for core flow.

## Hackathon Fit

| Hackathon | Angle |
|-----------|-------|
| **Synthesis** (celopg.eco) | Agents that cooperate (routing) + trust (proof packs) + pay (TBFF) + keep secrets (visibility scope) |
| **Agent V2** (Celo) | Real-world agent infrastructure: natural language → structured commitment → deterministic routing → stewarded pools |

Same codebase, tailored narratives.

## Team

- **Darren Zal** — BKC architect. Commitment routing, API, MCP tools, Celo adapter.
- **Benjamin Life** — Web UX, flow visualization, submission narrative, demo polish.

## Links

- [Salish Sea Knowledge Garden](https://45.132.245.30.sslip.io) (live BKC node)
- [BKC GitHub](https://github.com/BioregionalKnowledgeCommons)
- [Commitment Pooling Foundations](https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning/blob/main/docs/foundations/commitment-pooling-foundations.md)
- [Flow Funding Visualization](https://45.132.245.30.sslip.io/commons/flow-funding) (live)
