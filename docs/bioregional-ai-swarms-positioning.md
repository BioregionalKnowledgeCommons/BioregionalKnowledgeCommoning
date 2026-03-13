# BKC as Knowledge Plane for Bioregional AI Swarms
*Positioning one-pager — for sharing in Telegram: "bioregional ai swarms < builders >"*
*Share before Mar 5 build day so participants arrive with context*

---

## The Two-Plane Model

The bioregional AI swarm stack needs two complementary planes. BKC is the knowledge plane.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  KNOWLEDGE PLANE                    ACTION PLANE
  (persistent state)                 (real-time coordination)

  KOI-net federation          ←→     Matrix rooms / A2A agents
  Entity graph (15 types)     ←→     Task allocation (co-op.us)
  Commons intake governance   ←→     Floor control / turn-taking
  RAG chat (grounded answers) ←→     Agent negotiation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  CROSS-CUTTING CONCERNS:

  TRUST:    ECDSA identity, A2A Agent Cards, steward roles
  LOCATION: Astral TEE attestation (near-term), ZK trilateration (R&D)
  CAPITAL:  Hypercerts from Evidence entities, TBFF bridge

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  FOUNDATION: Cosmolocal philosophy
  Light things global: protocols, ontologies, pattern language
  Heavy things local: knowledge graphs, relationships, trust
```

---

## What BKC Has Built (live in production, 4 federated nodes)

- **Federated knowledge graph** — 4 nodes (Salish Sea, Front Range, Greater Victoria, Cowichan Valley), 560+ entities, 15 types, 27 predicates. KOI-net protocol with ECDSA-signed envelopes and consent-gated federation.
- **Governance membrane (consent intake)** — staged → approved → ingested. Immutable decision audit log. Per-node steward authorization. This is what everyone else is planning.
- **Knowledge-grounded RAG chat** — `/chat` with 2-hop graph traversal, doc chunks, web sources. <6s latency, 6-8 cited sources per response. Hallucination-resistant.
- **Knowledge Gardener AI (Octo)** — 15-tool KOI contract, 4-stage quality gates, CAT receipts for provenance. Running on Salish Sea coordinator.
- **Summarizer pipeline (darren-workflow)** — MacWhisper/Otter → entity extraction → governed ingest → KOI graph. This is ~90% of what Clawsmos calls a Summarizer. Already working.
- **Personal Claw (personal-koi-mcp)** — 53-tool MCP server: 15 portable contract tools + 38 personal extensions (email, vault, session search, document sharing with permission modes). This IS the Personal Claw.
- **TBFF bridge** — Knowledge→Flow→Evidence loop. Finance decisions logged as Evidence entities with RIDs.
- **WebAuthn auth** — Passkey-based steward authentication. No passwords.

---

## Comparison Matrix

| Capability | BKC | Clawsmos | co-op.us | Owocki PRD |
|------------|-----|----------|----------|-----------|
| Federated knowledge graph | ✅ Production | 🔷 Planning | ❌ | ❌ |
| Governance membrane (consent) | ✅ Production | ❌ | ❌ | ❌ |
| Entity resolution / dedup | ✅ Production | ❌ | ❌ | ❌ |
| Knowledge-grounded RAG chat | ✅ Production | ❌ | ❌ | ❌ |
| Meeting → entity pipeline | ✅ Production | 🔷 Planning | ❌ | ❌ |
| Real-time agent coordination | ❌ | 🔷 POC | 🔶 Building | ❌ |
| Per-node AI reasoning | 🔶 Octo live; per-node = arch goal | 🔷 Planning | 🔶 Building | ❌ |
| Task allocation | ⚠️ Partial | ❌ | 🔶 Building | ❌ |
| Capital allocation primitives | ⚠️ TBFF bridge | ❌ | ❌ | 🔷 Design |
| Holonic topology (documented) | ✅ Deeply | ❌ | ⚠️ Cosmolocal | ❌ |

---

## The Holonic Framing — What Nobody Else Has

Bioregions are nested: a watershed feeds a river feeds an inlet feeds a sea feeds an ocean.
Knowledge commons should mirror this structure.

Each BKC node is a **holon** — whole unto itself (sovereign, self-governing, locally held knowledge) AND part of something larger (federated, pattern-sharing, interoperable). This isn't just architecture — it mirrors ecological reality.

Every project in this Telegram group independently arrived at **cosmolocal** as the design principle:
> *Light things global (protocols, patterns, ontologies). Heavy things local (knowledge, relationships, governance).*

BKC has implemented this. Fully. Now.

---

## The Natural Integration Seams

**BKC ↔ Clawsmos (highest value):**
- Clawsmos Summarizer calls BKC `/ingest` → persistent memory from Matrix coordination
- BKC `/chat` exposed to Clawsmos agents → knowledge-grounded responses
- `personal-koi-mcp` IS the Personal Claw — available as reference implementation
- **Build day goal: wire Summarizer to `/ingest` in one pairing session**

**BKC ↔ co-op.us:**
- Task completion → KOI Evidence entity (provenance chain for bounties)
- Bounty outcomes → Hypercerts claims (already planned in BKC, low effort)

**BKC ↔ A2A protocol:**
- 15-tool KOI contract published as Agent Cards at `.well-known/agent-card.json`
- Any A2A-compatible agent auto-discovers BKC tools — zero custom integration
- This is already on BKC roadmap

---

## The Governance Membrane Is the Differentiator

Everyone else is planning knowledge graphs. Nobody else has built the governance layer.

BKC's consent-based intake means:
- External agents can propose knowledge but cannot write to the commons unilaterally
- Every boundary-crossing requires a steward decision
- Decisions are logged immutably (INSERT-only audit log)
- The membrane is visible in the demo — you can watch a steward approve a Clawsmos-submitted entity live

This is the piece owocki's PRD describes as "bounded authority." BKC has built it at the knowledge layer. The capital layer (≤$500 USDC auto; larger = multisig) is an extension of the same pattern.

---

## Invitation for Build Day (Mar 5, 2pm MT)

BKC will demo live: 4-node federation, knowledge-grounded chat, governance membrane, evidence loop.

**If you want to pair during build day:**
- Clawsmos: bring your Summarizer and the ingest contract (see `Octo/docs/integration/summarizer-ingest-contract.md`)
- co-op.us: bring your task completion webhook and let's wire it to Evidence entities
- owocki: the knowledge half of your PRD is running — let's talk Hypercerts

**The ask is not adoption of BKC's stack.** The ask is: pick one seam, wire it, verify it works. If it works, we have a live integration across two independent systems. That's the demo.

---

## Attribution

BKC is building the knowledge plane as an open contribution to the bioregional swarm ecosystem.

**Core contributors:** Darren Zal (Salish Sea BKC), BKC COP (Bill Baue, Eli Ingraham, Simon Grant), and the practitioners and Indigenous knowledge holders being interviewed across Cascadia.

**Technical stack:** OpenClaw (agent), KOI-net (federation protocol), FastAPI (backend), Next.js (dashboard), PostgreSQL + pgvector + Apache AGE (graph).

**License:** Open source. The pattern language and meta-protocol are CC-BY. The code is MIT.

**GitHub:** [BioregionalKnowledgeCommons](https://github.com/BioregionalKnowledgeCommons) | **Live app:** [Salish Sea Knowledge Commons](https://salishsee.life/commons) | **Knowledge site:** [Salish Sea Knowledge Garden](https://salishsee.life)

---

*Darren Zal — Salish Sea Bioregion — zaldarren@gmail.com*
*For Telegram: "bioregional ai swarms < builders >" — share before Mar 5*
