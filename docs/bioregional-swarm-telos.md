# Bioregional AI Swarms — Telos Document
*Three-plane architecture for coalition-grade bioregional intelligence*
*For: Mar 5 Build Day screen-share (Segment 5) and owocki's audience*

---

## The Three Planes

Bioregional AI swarms need three complementary planes working together. No single project builds all three. The coalition exists because each plane needs the others.

```
┌─────────────────────────────────────────────────────────────────┐
│  CAPITAL PLANE  (Action — where value flows)                    │
│                                                                 │
│  owockibot treasury allocation    Gitcoin rounds (GG25-29)      │
│  Hypercerts from Evidence entities    co-op patronage engine    │
│  Bounded authority: ≤$500 auto, larger = multisig               │
│                                                                 │
│  WHO BUILDS: owocki (capital logic), co-op.us (patronage),      │
│              BKC (Evidence entities + Hypercerts bridge)         │
│  STATUS: owocki PRD designed │ BKC TBFF bridge live │           │
│          co-op patronage building                               │
├─────────────────────────────────────────────────────────────────┤
│  COORDINATION PLANE  (Real-time — where agents talk)            │
│                                                                 │
│  Clawsmos Matrix rooms + agent roles (Summarizer, Orchestrator, │
│    Moderator, Representative)                                   │
│  A2A protocol for cross-agent discovery                         │
│  co-op.us agent API + task allocation                           │
│  Floor control, turn-taking, negotiation                        │
│                                                                 │
│  WHO BUILDS: AG Neyer / Clawsmos (Matrix agents),              │
│              Todd / co-op.us (task allocation),                 │
│              Nou-Techne (A2A demos)                             │
│  STATUS: Clawsmos architecture defined │ co-op.us building │   │
│          A2A agent cards live (BKC + others)                    │
├─────────────────────────────────────────────────────────────────┤
│  KNOWLEDGE PLANE  (Persistent — where truth lives)              │
│                                                                 │
│  BKC federated knowledge graph (4 nodes, 560+ entities)         │
│  KOI-net protocol (ECDSA-signed, consent-gated federation)      │
│  Governance membrane (staged → approved → ingested)             │
│  Entity resolution (4-tier deduplication)                       │
│  Knowledge-grounded RAG chat (<6s, 6-8 cited sources)           │
│  Summarizer pipeline (transcript → entities → graph)            │
│  Watershed data + ecological monitoring                         │
│                                                                 │
│  WHO BUILDS: Darren Zal / BKC (knowledge infra + federation),  │
│              watershed partners (ecological data collection)    │
│  STATUS: ██████████ LIVE IN PRODUCTION                          │
└─────────────────────────────────────────────────────────────────┘

Cross-cutting concerns (touch all three planes):

  TRUST       ECDSA node identity │ A2A Agent Cards │ steward roles │ WebAuthn passkeys
  LOCATION    Astral TEE attestation (near-term) │ ZK trilateration (R&D)
  GOVERNANCE  Commons membrane (knowledge) │ Bounded authority (capital) │ Consent gates (federation)
```

---

## How Capital Flows Through the System

```
  Knowledge created          Capital allocated         Evidence recorded
  (transcript, data,    →    (bounties, grants,    →   (outcomes logged as
   field observation)         work orders)              Evidence entities)
        │                          │                         │
        ▼                          ▼                         ▼
  ┌──────────┐            ┌──────────────┐           ┌──────────────┐
  │ KNOWLEDGE│            │   CAPITAL    │           │  KNOWLEDGE   │
  │  PLANE   │───────────▶│    PLANE     │──────────▶│    PLANE     │
  │ (BKC)    │  Evidence  │ (owockibot)  │  Receipt  │   (BKC)      │
  └──────────┘  informs   └──────────────┘  closes   └──────────────┘
                allocation                  the loop

  The loop closes: knowledge informs capital → capital flows are themselves knowledge.
  Every allocation has a provenance chain back to the evidence that justified it.
```

**Concrete example (build day context):**
1. Owocki allocates $1k USDC bounty for "bioregional swarm knowledge infrastructure"
2. BKC Knowledge Plane records work evidence: entities created, relationships mapped, governance decisions logged
3. Evidence entities reference the bounty RID — the loop closes
4. Hypercerts can be minted from Evidence entities (planned) — making impact claims verifiable and tradeable

---

## Holonic Topology — What's Live Now

```
                    ┌─────────────────────┐
                    │  Cascadia           │  ← future meta-coordinator
                    │  (planned)          │
                    └─────────┬───────────┘
                              │
                    ┌─────────┴───────────┐
                    │  Salish Sea / Octo  │  ← federation coordinator
                    │  45.132.245.30      │     15-tool AI agent (Octo)
                    │  560+ entities      │     knowledge gardener
                    └──┬──────┬───────┬───┘
                       │      │       │
           ┌───────────┘      │       └───────────┐
           │                  │                   │
  ┌────────┴────────┐ ┌──────┴────────┐ ┌────────┴────────┐
  │ Greater Victoria │ │ Cowichan      │ │ Front Range     │
  │ 37.27.48.12     │ │ Valley        │ │ :8355 (co-loc)  │
  │ leaf node       │ │ 202.61.242.194│ │ Boulder/Denver  │
  │ Salish Sea      │ │ leaf node     │ │ bioregion       │
  └─────────────────┘ └───────────────┘ └─────────────────┘

  Each node: sovereign database │ own identity │ own governance │ same KOI API
  Federation: ECDSA-signed envelopes │ consent-gated sharing │ holonic nesting
```

**Key architectural principle — cosmolocal:**
> *Light things global:* protocols, ontologies, pattern language.
> *Heavy things local:* knowledge graphs, relationships, trust, governance.

Every project in the coalition independently arrived at this principle. BKC has implemented it.

---

## What's Live vs. Planned

### Live in Production (demo-ready)

| Capability | Where | Verifiable |
|---|---|---|
| 4-node federated knowledge graph | Salish Sea, FR, GV, CV | `curl .../health` → 200 on all 4 |
| 560+ entities across 15 types | Octo + FR graphs | Entity search returns results |
| Knowledge-grounded RAG chat | `/chat` endpoint | <6s response, 6-8 cited sources |
| Commons governance membrane | Steward login + approval flow | Staged → approved → ingested (live) |
| A2A Agent Card (15 tools) | `/.well-known/agent-card.json` | Any A2A agent can discover BKC |
| Entity resolution (4-tier) | `/ingest` pipeline | Exact, fuzzy, semantic, create |
| Summarizer pipeline | darren-workflow + KOI ingest | Transcript → entities → graph |
| WebAuthn steward auth | Passkey-based, no passwords | Live steward login on production |
| CAT provenance receipts | Every ingest operation | Receipt URIs returned on ingest |
| KOI-net federation (ECDSA) | Cross-node sharing | Signed envelopes with consent gates |

### Planned / Building

| Capability | Owner | Timeline |
|---|---|---|
| Hypercerts from Evidence entities | BKC + owocki | Q2 2026 |
| GraphRAG community detection | BKC | Post-build day |
| Cascadia meta-coordinator node | BKC | Q2 2026 |
| External Summarizer hookup (Clawsmos) | AG Neyer + BKC | Gate A/B decision Mar 3 |
| co-op.us task → Evidence pipeline | Todd + BKC | Post-build day |
| Astral TEE location attestation | John Caldwell + BKC | Near-term integration |
| ZK trilateration proofs | R&D track | Future |
| Per-node AI reasoning (FR, GV, CV) | BKC | Phased deployment |

---

## Integration Seams — How the Planes Connect

### Knowledge → Coordination (BKC ↔ Clawsmos / co-op.us)
```
Clawsmos Summarizer ──POST /ingest──▶ BKC Knowledge Graph
                                          │
BKC /chat endpoint ◀──query──── Clawsmos agents (knowledge-grounded responses)
                                          │
co-op.us task completion ──▶ BKC Evidence entity (provenance chain)
```

### Knowledge → Capital (BKC ↔ owockibot)
```
BKC Evidence entities ──reference──▶ owockibot allocation decisions
                                          │
Allocation receipts ──▶ BKC Knowledge Graph (loop closes)
                                          │
Evidence entities ──mint──▶ Hypercerts (planned, Q2)
```

### Cross-Agent Discovery (A2A)
```
Any A2A agent ──GET /.well-known/agent-card.json──▶ 15-tool KOI contract
                                                        │
                                                   Auto-discovers:
                                                   entity-search, chat,
                                                   ingest, graph-query,
                                                   health, ... (15 tools)
```

---

## The Governance Membrane — What Makes This Different

Everyone else is planning knowledge graphs. Nobody else has built the governance layer.

```
  External agent                    Commons boundary                Graph
  (Clawsmos, co-op.us,     ──▶    ┌─────────────────┐    ──▶    Persistent
   any A2A agent)                  │  Steward reviews │           knowledge
                                   │  Staged entity   │
       Proposes knowledge          │  Approves/rejects│           Trusted,
       but cannot write            │  Decision logged │           auditable,
       unilaterally                │  (immutable)     │           governed
                                   └─────────────────┘
```

**This is the differentiator.** The consent membrane means:
- External agents can propose knowledge but cannot write to the commons unilaterally
- Every boundary-crossing requires a steward decision
- Decisions are logged immutably (INSERT-only audit log)
- The membrane is visible in the demo — you can watch a steward approve an entity live

This is the "bounded authority" pattern from owocki's PRD — implemented at the knowledge layer.

---

## Coalition Asks (Build Day and Beyond)

| Ask | To | Seam | Effort |
|---|---|---|---|
| Wire Summarizer → BKC `/ingest` | AG Neyer / Clawsmos | Knowledge ↔ Coordination | 1 pairing session |
| Task completions → Evidence entities | Todd / co-op.us | Knowledge ↔ Coordination | 1 webhook |
| Bounty allocation → Evidence references | owocki | Knowledge ↔ Capital | Contract alignment |
| Location attestation integration | John Caldwell / Astral | Cross-cutting trust | API hookup |
| Social narrative for owockibot audience | Tommy / proofoftom | Movement comms | Content creation |
| Recurring sprint cadence (Fridays noon-3pm?) | All | Coalition ops | Calendar invite |
| GG25-29 bioregional swarms round scope | owocki | Capital allocation | Scope doc |

---

## The Invitation

BKC is not asking anyone to adopt our stack. We are saying:

1. **The knowledge plane exists.** It's live, federated, governed, and queryable.
2. **Pick one seam.** Wire your system to one BKC endpoint. Verify it works.
3. **If it works, we have a live integration** across two independent systems. That's the demo.
4. **The pattern language is open.** Take the patterns. Fork the implementation. Build your own holonic node.

The architecture is open. The governance is explicit. The claims are auditable. The invitation is real.

---

*Darren Zal — Salish Sea Bioregion — zaldarren@gmail.com*
*Bioregional Knowledge Commons — [Live app](https://45.132.245.30.sslip.io/commons) | [GitHub](https://github.com/BioregionalKnowledgeCommons)*
*License: CC-BY (pattern language), MIT (code)*
