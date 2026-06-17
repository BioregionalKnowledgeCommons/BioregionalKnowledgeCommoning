---
doc_id: bkc.connection.neighbourhoods-runtime-layer
doc_kind: research
status: draft
disposition: unresolved tension
depends_on:
  - bkc.project-vision
  - bkc.coordination-stack
relates_to:
  - spore.connection.neighbourhoods-grammars-deterministic-runtime
  - bkc.commitment-pooling
  - bkc.federation-overview
sources:
  - url: https://happeningscommunity.substack.com/p/neighbourhoods-grammars-that-travel
    title: "Neighbourhoods: Grammars that Travel (Sam Turner, Happenings Community)"
    version: "article dated 2026-05-01; accessed 2026-06-16"
    note: >-
      Secondary/journalistic source describing an unreleased system; public
      neighbour-hoods GitHub org shows no substantive commits since mid-2024.
      Treat as aspirational-current, not verified.
---

# Neighbourhoods grammars — the executable coordination-runtime layer BKC is missing

## Why this note exists

BKC is strong on the **knowledge** layer (KOI: federated, semi-permeable nodes, entity
resolution, RAG) and has a **governance/coordination** layer (commitment pooling, the
coordination stack). It is thin on one thing: an **executable, local-first way for a
community to actually run a coordination practice** — a stewardship log, a resource-sharing
rota, a claims-review workflow — that the community owns, that works offline, and that can
travel to another bioregion without losing what makes it theirs.

Neighbourhoods Network describes exactly that layer: a Grammar Definition Language +
compiler + transport-agnostic runtime that turns a coordination practice into a
deterministic, peer-to-peer app (CRDT data, DID-signed actions, Merkle-forest provenance,
and a portable compiled validation module). See the Spore-side framing at
`spore.connection.neighbourhoods-grammars-deterministic-runtime` for the full primitive
mapping; this note records what it means specifically for BKC.

## What it would add to BKC

- **Execution altitude.** KOI remembers and the coordination stack governs; nothing currently
  *runs* a procedural workflow as an app a stewardship group operates day to day.
  Neighbourhoods fills that govern → know → **run** gap.
- **Offline / mesh capability.** The runtime is described as transport-agnostic (Bluetooth/WiFi
  mesh on the roadmap). That property — if real — matters disproportionately for
  low-connectivity field and stewardship work, where cloud-first tools fail.
- **Replication-by-grammar.** A stewardship-coordination grammar refined in one bioregion
  could be adopted by another — the local-to-global federated-replication story BKC already
  cares about, expressed as a portable, expert-rewarding asset.
- **Claims + reputation tie-in.** Neighbourhoods' signed actions carry a portable validation
  module verifiable by foreign systems. That is adjacent to BKC's commitment-pooling and the
  Regen claims work: a signed Neighbourhoods action could become a **KOI Claim with native
  provenance → Regen anchor**. Reputation "recognisable as a person moves between
  Neighbourhoods" rhymes with cross-pool reputation in `bkc.commitment-pooling`.

## The integration seam (does not replace KOI)

Bridge at the **claims/provenance boundary**, not by merging data models. KOI's pgvector
semantic graph and Neighbourhoods' CRDT local-first graph stay separate:

> signed Neighbourhoods action → KOI Claim (with provenance) → Regen anchor.

## The unresolved tension

Neighbourhoods enforces rules deterministically (compiled preconditions). BKC's knowledge and
much of its bioregional sensemaking is qualitative, relational, and contested — it does **not**
belong in a state machine. The right scope is the *procedural* slice (rotas, votes, logs,
claims-workflow), with the contested/epistemic slice left to KOI + the governance layer.
Over-applying a determinism engine to sensemaking would be a category error.

## Open questions

- Is the offline-mesh capability working today or still roadmap? (Websocket-only at writing.)
- Could a signed Neighbourhoods action be exported as a KOI Claim another system ingests, or
  is the validation module meant to stay in-network?
- Maturity/vendor risk (single-maintainer, code not visibly published). What is the smallest
  experiment — e.g. one stewardship-log or claims-review grammar emitting signed actions into
  KOI — that tests the seam without betting on the platform?

## Disposition

**Unresolved tension.** Records a real executable-runtime gap in the BKC stack and a genuine
determinism-vs-contestability boundary, without endorsing adoption. Outreach to Jill Burrows
opened 2026-06-16; next step is the narrow integration experiment above.
