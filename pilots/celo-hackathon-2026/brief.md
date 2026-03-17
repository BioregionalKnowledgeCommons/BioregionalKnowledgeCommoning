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

We extended it with **commitment routing** and deployed a **commitment economy on Celo mainnet**:

### Agents That Cooperate

An AI agent takes natural language — *"Regenerate Cascadia offers 200 hours of native plant restoration, valued at $8,000, April-September. Wants: soil testing equipment. Limit: max 3 concurrent sites."* — and structures it into a commitment object with typed offers, wants, limits, and routing tags.

A deterministic routing scorer matches commitments to pools based on bioregion proximity, offer/need taxonomy overlap, timeframe alignment, capacity fit, and governance compatibility. No black-box ML — transparent, auditable scoring.

The full pipeline runs audio-to-blockchain: a real audio recording is transcribed via Whisper, commitments are extracted by LLM, routed to pools, verified, and minted as on-chain tokens — all orchestrated by the agent.

### Agents That Trust

Commitments are self-sovereign — anyone can make a promise. The question is which pools accept it.

Three orthogonal operations govern the lifecycle:
1. **Create** — the pledger issues a commitment (self-sovereign, no gatekeeper)
2. **Pledge** — a pool steward curates by accepting the commitment into a pool (peer-curated, like SPROUT License peer review)
3. **Verify** — a peer attests that the pledger can deliver (trust signal, earned through witnessed follow-through)

These operations are independent: a commitment can be pledged while PROPOSED, verified without being in any pool, or both. There is no single approval gate.

Every commitment carries provenance: who created, who curated, who verified. State transitions are logged in an insert-only audit trail. Evidence entities link proof of fulfillment. The full chain is assembled into a proof pack — archivable, verifiable, anchored to Regen Ledger.

**Forkability as safety valve:** If a pool's curation standards diverge from community values, any steward can fork the pool — take the commitments they trust and create a new pool with different governance. This is the antidote to possessive stewardship: authority over a pool is earned by curation quality, not granted by position.

### Agents That Pay

Victoria Commitment Vouchers (VCV) are deployed on Celo mainnet as a GiftableToken (`0x4CDb98Ff88af070b1794752932DbAD9Edf7a1573`). Verified commitments are minted as VCV tokens — 28,600 VCV minted from 23 verified commitments in the demo run. Threshold-Based Flow Funding (TBFF) settles verified commitments through a TBFFSettler contract (`0x10De66A7f4e20d696Fb0d815c99068D4fA1f9030`) with needs-based redistribution across 5 nodes. Settlement receipts chain back to the original commitment through the knowledge graph.

The agent itself participates as an economic actor — registering 4 offers (transcription, extraction, routing, attestation services) and 3 needs (audio data, community feedback, governance templates), demonstrating that infrastructure providers are first-class participants in the commitment economy.

### Agents That Keep Secrets

A consent-aware visibility scope system (34 query sites filtered across 15 public endpoints) ensures that `node_private` commitments never leak to unauthorized consumers. Communities control what's visible to the network.

## Architecture

```
Audio Recording ──→ Whisper Transcription ──→ LLM Extraction
                                                    │
                                            Commitment Objects
                                                    │
                                              Routing Scorer
                                                    │
                                       ┌────────────┴────────────┐
                                       ▼                          ▼
                              Pool A (Victoria)          Pool B (Cascadia)
                                       │
                                Steward Approval
                                       │
                              Pledge + Verify + Mint
                                       │
                        ┌──────────────┼──────────────┐
                        ▼              ▼              ▼
                   VCV Token     TBFFSettler     Celo EAS
                   (Celo)       (Celo)         Attestation
                        │              │              │
                        └──────────────┼──────────────┘
                                       ▼
                                  Proof Pack
                          (BKC + Regen Ledger + Celo)
```

**BKC is canonical.** The knowledge graph, governance, and routing logic live in BKC. Celo provides the token layer (VCV minting), redistribution layer (TBFFSettler), and attestation layer (EAS) — complementary infrastructure, not the product.

## Grassroots Economics Alignment

BKC commitment pooling maps directly to the patterns Grassroots Economics has proven at scale: 26,367 users, 188 active pools, 745 vouchers, $320K swap volume (per Dune Analytics dashboard, as of Jul 2025):

| BKC | GE / Sarafu | What it means |
|-----|-------------|---------------|
| Commitment (offers/wants/limits) | Community Asset Voucher (CAV) | BKC adds typed constraints and agent-assisted drafting |
| CommitmentPool + governance | Swap pool + token registry | BKC adds steward governance membrane |
| Evidence + proof pack | CAV redemption receipt | BKC adds cryptographic provenance chain |
| TBFF threshold bands | Token limiter | Similar safety mechanics, different layers |
| Routing scorer | (Manual matching) | New: deterministic multi-factor routing |

**CLC convergence**: Will Ruddick's Cosmo-Local Credit (white paper at cosmolocal.credit) adds multi-hop routing via CPP (Commitment Pooling Protocol) with four interfaces — Curation, Valuation, Limitation, Exchange. BKC provides Curation (governance membrane) and Valuation (routing scorer); CLC provides Limitation and Exchange (settlement execution). Our routing scorer implements §5.2 on-demand routing — scored pool suggestions that a CLC router would execute multi-hop. The integration path is a post-hackathon study (C1), not hackathon scope.

## Demo

Three acts, all running on Octo production with real on-chain transactions:

1. **Human participation** — A real audio recording of a mapping workshop is transcribed via Whisper. The agent extracts 10 commitment candidates from conversation, routes them to the Victoria pool, verifies qualifying commitments, and mints VCV tokens on Celo mainnet for each verified commitment.
2. **Agent self-commitment** — The agent registers itself as an economic actor: 4 offers (transcription, extraction, routing, attestation services) and 3 needs (audio data, community feedback, governance templates). Its own commitments are verified and minted as VCV, demonstrating that infrastructure providers participate in the same economy as human contributors.
3. **TBFF settle + attest** — The TBFFSettler contract redistributes VCV across 5 nodes based on needs-weighted scoring. A Celo EAS attestation is created for the settlement, completing the dual-chain proof (BKC knowledge graph + Regen Ledger anchor + Celo attestation).

End-to-end: audio → transcription → extraction → routing → verification → minting → settlement → attestation. All on-chain, all auditable.

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
