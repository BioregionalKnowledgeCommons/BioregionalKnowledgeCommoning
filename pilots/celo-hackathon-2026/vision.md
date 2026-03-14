# Vision: Commitment Routing as Cosmo-Local Infrastructure

**Sprint north star — Mar 14–22, 2026**

---

## Thesis

Commitment routing is the missing infrastructure for cosmo-local coordination. Communities already make promises — a nursery pledges seedlings, a land trust offers monitoring hours, a collective commits mycoremediation labor. What they can't do is *route* those promises: match offers to needs across bioregion boundaries, verify follow-through with shared provenance, and settle obligations without losing the trust that makes them work.

The ancient patterns already exist. Mweria (Kenyan reciprocal labor), Meitheal (Irish communal work), Chama (East African savings circles) — these are commitment pooling protocols that predate software by centuries. The gap isn't in the social technology. It's in making these patterns legible across communities that don't yet know each other.

AI agents and blockchain settlement are layers on top of this foundation. Stewardship is the foundation itself.

---

## The Arc

Will Ruddick's narrative arc from *Footnotes on Intelligence* traces the loop:

```
sensing → meaning-making → caring → committing → coordinating → learning
```

Each step maps to what we've built:

| Loop stage | BKC implementation |
|------------|-------------------|
| **Sensing** | Federated knowledge graph — 1,005 entities across 4 nodes, MediaWiki import, interview commoning |
| **Meaning-making** | Ontology-grounded entity resolution, discourse graph (supports/opposes/informs) |
| **Caring** | Community-governed visibility scope — 34 query sites filtered, consent membrane |
| **Committing** | Commitment creation with typed offers/wants/limits, self-sovereign promise issuance |
| **Coordinating** | Deterministic routing scorer, steward pledge/verify, pool governance |
| **Learning** | Proof packs — evidence chain + attestations + ledger anchor, archivable and verifiable |

The loop closes when proof of fulfillment feeds back into the knowledge graph as evidence for the next round of sensing. This is the capital loop proof: commitments are not just made and settled — they are *remembered*, and that memory becomes the shared substrate for the next cycle.

---

## What We've Proven

This is not a prototype. The following is live and deployed:

- **1,005 entities** in a federated knowledge graph spanning 4 bioregional nodes (Salish Sea coordinator, Greater Victoria, Cowichan Valley, Front Range)
- **Commitment routing**: natural language → structured commitment → deterministic multi-factor scoring → pool suggestions with transparent score breakdowns
- **Three orthogonal governance operations**: Create (self-sovereign), Pledge (peer-curated pool acceptance), Verify (trust attestation) — independent, composable, forkable
- **Proof packs on Regen Ledger**: evidence chain + attestations + content hash + IRI + tx_hash, assembled into archivable JSON artifacts
- **TBFF settlement**: threshold-based flow funding with auto/semi/manual bands, receipt chain linking settlement back to original commitment
- **Consent membrane**: federation-wide edge approval, visibility scope filtering, 15/15 consent leakage tests passing
- **Passkey auth**: one-tap WebAuthn sign-in, steward authorization per node
- **Flow funding visualization**: live at `/commons/flow-funding` — interactive @xyflow/react graph with threshold bands and project funding progress (Demo mode; Live mode pending BFF route fix)

---

## What This Sprint Adds

The core demo path works end-to-end. This sprint is about hardening, narrative, and one high-signal on-chain artifact:

1. **Harden** — smoke test every demo path step on live Octo, fix any brittleness
2. **One Celo proof artifact** — research Celo attestation infra (EAS or Celo Attestation Service), aim for one Alfajores attestation proving a commitment was verified. Kill date: Day 3. If it doesn't land, BKC-only demo stands on its own.
3. **ERC-8004 receipt framing** — proof packs already *are* receipts. Frame them explicitly for the "Agents With Receipts" track.
4. **Lock the narrative** — demo video, brief.md refresh, submission assets for both Celo V2 and Synthesis
5. **Bonus integrations** — Locus payment, ENS identity, routing visualization. Only if Phases 1–3 are frozen.

---

## The Cosmolocalism Thread

BKC commitment routing maps directly to Will Ruddick's Cosmo-Local Credit (CLC) architecture. The CLC Commitment Pooling Protocol (CPP) defines four interfaces:

| CLC interface | BKC implementation | Status |
|---------------|-------------------|--------|
| **Curation** | Governance membrane — steward pledge/verify, edge approval, visibility scope | Live |
| **Valuation** | Routing scorer — bioregion proximity, taxonomy overlap, timeframe, capacity fit | Live |
| **Limitation** | TBFF threshold bands + pool capacity limits | Live |
| **Exchange** | Settlement execution — TBFF auto-advance, receipt chains | Live (BKC-native) |

Our routing scorer implements CLC §5.2 on-demand routing: scored pool suggestions that a CLC SwapRouter would execute as multi-hop `Hop[]` paths. The mapping is direct — BKC provides the upstream intelligence (which commitments should route where, based on what governance), CLC provides the downstream execution (multi-hop settlement across pool networks).

Post-hackathon convergence (C1/C2), not scope. But naming it shows where this goes: BKC as the curation and valuation layer for a cosmo-local credit network operating on Celo.

---

## Why This Matters

The Sarafu Network has proven commitment pooling works at scale: 26,367 users, 188 active pools, 745 vouchers, over 1,200 acres restored, 84% positive income impact. What it hasn't yet solved is the *routing problem* — how commitments from one community find matching needs in another, with governance that scales beyond personal relationships.

BKC adds three things the existing infrastructure lacks:

1. **Structured routing** — a deterministic scorer that matches commitments to pools based on multiple factors, not just manual selection. Transparent, auditable, no black-box ML.

2. **Federated governance** — a consent-aware membrane that controls what flows where, with steward approval at every boundary. Communities control their own data and trust relationships.

3. **Provenance chain** — every state transition logged, every verification attributed, every settlement linked to evidence, assembled into proof packs anchored on-chain. The shared memory of kept commitments — Will Ruddick's "emotional center" of the knowledge commons.

This is coordination infrastructure for bioregional economies. Not another ReFi token scheme. Not a grant-funded prototype. A working system that makes ancient commitment patterns legible to modern coordination tools, settled on-chain, governed by the communities who use it.

---

## North Star

A nursery in Victoria pledges seedlings. An AI agent structures the commitment with typed offers, wants, and limits. A routing scorer suggests matching pools across the Salish Sea and Front Range. A steward in each bioregion curates what fits their community. A peer verifies the nursery can deliver. Evidence is linked when seedlings arrive. A proof pack captures the full loop — who promised, who curated, who verified, what was delivered — anchored on Regen Ledger and (stretch goal) attested on Celo.

The next time someone in Cascadia needs native seedlings, the knowledge graph already knows who delivers and who vouched for them. Trust compounds. Coordination scales. The commons remembers.

That's what we're building.
