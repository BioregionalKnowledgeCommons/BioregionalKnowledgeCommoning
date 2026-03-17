# Capital Plane Update — Funding the Commons SF

**Date:** 2026-03-13
**For:** Benjamin Life, Shawn Anderson, Dylan Tull, Jeff Emmett, FtC collaborators
**From:** Darren Zal

---

## What Is the Capital Plane

The Bioregional Knowledge Commons has three planes: Knowledge (what we know), Coordination (how we work together), and Capital (how resources move). Over the past two weeks, the Capital Plane went from thin — just a planned TBFF bridge — to a working system with commitment pooling, a claims engine with on-chain proofs, threshold-based flow funding integration, and a live visualization. Everything described below is deployed and running on the Salish Sea node.

---

## What's Live

### Commitment Pooling (C0)

The commitment lifecycle API is deployed with three orthogonal operations — **Create, Pledge, Verify** — that compose freely without creating single-point gatekeepers. Anyone can issue a commitment (self-sovereign). Pool stewards curate which commitments belong in their pool (peer-curated). Peers attest that a pledger can deliver (trust signal). These operations are independent: a commitment can be pledged while still PROPOSED, or verified without being in any pool.

- **State machine:** PROPOSED → VERIFIED → ACTIVE → EVIDENCE_LINKED → REDEEMED (with DISPUTED/WITHDRAWN branches)
- **Ontology:** 3 new entity types (Commitment, CommitmentPool, CommitmentAction) + 6 predicates in BKC ontology v1.2.0
- **Seed data:** 2 pools, 3 commitments on Octo
- **API:** `POST /commitments/`, `POST /pools/{rid}/pledge`, `PATCH /commitments/{rid}/state`
- **Live:** [Commitments dashboard](https://45.132.245.30.sslip.io/commons/commitments)

### Claims Engine with V2 Attestations

The claims engine proves that work happened, with full provenance from evidence through on-chain anchoring:

- **State machine:** `self_reported → peer_reviewed → verified → ledger_anchored`
- **V2 attestation policy:** `peer_reviewed` requires 1+ approved attestation, `verified` requires 2+
- **On-chain anchoring:** Claims anchored to Regen Ledger (`regen-upgrade` testnet) via `MsgAnchor` with content hash, IRI, and tx hash
- **Proof packs:** `GET /claims/{rid}/proof-pack` bundles claim + evidence + attestations + anchor metadata + full audit history into one archivable JSON artifact
- **Steel thread proven end-to-end:** Phase A (generic evidence → claim → anchor → proof pack, 22/22 tests) and Phase B (interview artifacts → synthesized evidence → claim → anchor, 25/25 tests on Octo with live on-chain TX)

### TBFF Threshold Policy

Settlement events from Threshold-Based Flow Funding write back to the knowledge graph with tiered governance:

| Band | Amount | Behavior |
|------|--------|----------|
| **auto** | < $500 | Auto-advance to `verified` (2 system attestations) |
| **semi** | $500–$5,000 | Auto-advance to `peer_reviewed` (1 attestation) |
| **manual** | > $5,000 | Stays `self_reported` (full review required) |

- **Endpoint:** `POST /claims/claim-from-settlement` — settlement → evidence → claim with threshold auto-advance in one call
- **Override:** `manual_override: true` forces manual review regardless of amount
- **Verified on Octo:** Full loop — settlement → evidence → claim → anchor → proof pack. TX: `B1710CF1...` on Regen testnet.

### Flow Funding Visualization

Jeff — this uses your code. We vendored [flow-funding](https://github.com/BioregionalKnowledgeCommons/flow-funding) (forked from your repo) into the commons web dashboard and wired it to live settlement data from the KOI API.

- **Demo mode:** Victoria Landscape Hub data with the "lake level" threshold visualization — Mycopunks, Kinship Earth, Regenerate Cascadia as participants
- **Live mode:** Pulls real settlement data from `GET /claims/settlements` via BFF proxy, 60s auto-refresh
- **Stack:** `@xyflow/react` v12, dark theme adapted, React Query hooks
- **Live:** [Flow Funding Visualization](https://45.132.245.30.sslip.io/commons/flow-funding)

### Hub Cultivator Decision Logging

As Victoria's Hub Cultivator in the Regenerate Cascadia landscape program, steward funding decisions are logged as Evidence entities with CAT receipt chains:

- **Script:** `scripts/log-hub-decision.sh` wraps `/ingest` with Hub Cultivator conventions
- **Receipt chains:** `GET /receipts/{id}/chain` walks provenance back to root
- **Deterministic RIDs:** `hub-cultivator:` prefix for deduplication

### Victoria Landscape Hub Seed Data

9 entities seeded on Octo representing the Victoria ecosystem: Victoria Landscape Hub, Regenerate Cascadia, Kinship Earth, Mycopunks (Organizations), Flow Funding, Hub Cultivator, TBFF (Concepts), Cascadia (Bioregion), Greater Victoria (Location) — plus relationships between them.

---

## How It Fits Together

```
Hub Cultivator Decision           TBFF Settlement Event
(human steward, DAFs)             (algorithmic, Superfluid)
        │                                  │
        ▼                                  ▼
   /ingest with                  /claims/claim-from-settlement
   hub-cultivator: prefix          (threshold auto-advance)
        │                                  │
        ▼                                  ▼
   Evidence Entity ◄──── CAT Receipt Chain ────► Evidence Entity
        │                                          │
        └──────────► Commitment Pool ◄─────────────┘
                    (proves_commitment)
                           │
                     Claim Created
                           │
                    V2 Attestations
                           │
                   Regen Ledger Anchor
                     (MsgAnchor)
                           │
                      Proof Pack
                  (archivable JSON)
```

Two write-back paths feed the same knowledge graph. Every dollar that flows through either track is traceable: decision → evidence → claim → on-chain anchor. The receipt chain preserves full provenance. The flow funding visualization reads settlement data back out for real-time display.

---

## Grassroots Economics Alignment

BKC commitment pooling maps directly to patterns GE has proven at scale (26,367 users, 188 active pools, 745 vouchers):

| BKC | GE / Sarafu | What it means |
|-----|-------------|---------------|
| Commitment (offers/wants/limits) | Community Asset Voucher (CAV) | BKC adds typed constraints + agent-assisted drafting |
| CommitmentPool + governance membrane | Swap pool + token registry | BKC adds steward governance membrane |
| Evidence + proof pack | CAV redemption receipt | BKC adds cryptographic provenance chain |
| TBFF threshold bands | Token limiter | Similar safety mechanics, different layers |
| Routing scorer | (Manual matching) | New: deterministic multi-factor routing |

**CLC convergence:** Will Ruddick's Cosmo-Local Credit protocol adds multi-hop routing via CPP (Commitment Pooling Protocol). BKC provides Curation (governance membrane) and Valuation (routing scorer); CLC provides Limitation and Exchange (settlement execution). Our routing scorer implements CLC's on-demand routing interface — scored pool suggestions that a CLC router would execute multi-hop. Integration study planned for C1.

---

## What's Next

- **C1 — Pool Mechanics:** Threshold activation for pools, multi-pool pledging, TBFF settlement gates triggering pool activation
- **C2 — Federated Pooling:** Cross-node commitment exchange via KOI-net events, meta-regional pool aggregation
- **Hypercerts Bridge:** Mint Hypercerts from REDEEMED commitments (C2)
- **Flow Funding Phase 3:** Settlement timeline replay, claim detail panel, BKC legend, polish
- **MCP Tools for Attestations:** Claims engine attestation tools for Claude Code / Cursor workflows
- **GE Protocol Compatibility:** CIC Stack ↔ KOI-net event format analysis (C1)

---

## Links

- **Salish Sea Knowledge Garden:** [45.132.245.30.sslip.io](https://45.132.245.30.sslip.io)
- **Flow Funding Visualization:** [/commons/flow-funding](https://45.132.245.30.sslip.io/commons/flow-funding)
- **Commitments Dashboard:** [/commons/commitments](https://45.132.245.30.sslip.io/commons/commitments)
- **GitHub (org):** [github.com/BioregionalKnowledgeCommons](https://github.com/BioregionalKnowledgeCommons)
- **Commitment Pooling Foundations:** [docs/foundations/commitment-pooling-foundations.md](https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning/blob/main/docs/foundations/commitment-pooling-foundations.md)
- **Flow Funding Foundations:** [docs/foundations/flow-funding-foundations.md](https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning/blob/main/docs/foundations/flow-funding-foundations.md)
- **TBFF Demo Proof:** [tbff-threshold-demo-2026-03-12.md](https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning/blob/main/docs/demo-artifacts/tbff-threshold-demo-2026-03-12.md)
- **Flow Funding Fork:** [github.com/BioregionalKnowledgeCommons/flow-funding](https://github.com/BioregionalKnowledgeCommons/flow-funding) (vendored from Jeff Emmett's repo)
