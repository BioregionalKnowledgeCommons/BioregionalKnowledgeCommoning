# Telegram Post — Bioregional Builders Working Group

**Target:** Tonight or tomorrow morning, before Friday noon session.

---

Hey all — heads up on two hackathons we're entering this week, both on Celo:

**Synthesis** (celopg.eco, build Mar 13 → winners Mar 25) — "Agents that cooperate + trust"
**Agent V2** (Celo, Mar 2 → Mar 22) — "Agent infrastructure for real-world coordination"

Same codebase, tailored narratives.

**What we're building:** Agentic commitment routing for bioregional swarms.

The short version: AI agents help communities express offers, wants, and limits as structured commitments → a routing scorer suggests pool matches → stewards curate (pledge to pools) → peers verify (trust attestation) → proof of fulfillment gets anchored. Three independent operations: create, pledge, verify. BKC is the knowledge layer, Celo is settlement/provenance.

We already have the commitment pooling API (C0), proof packs with on-chain anchors, and the flow-funding visualization. This week we're adding the routing scorer, a web intake form, and a steward review dashboard.

**Friday noon session:** Demo storyboard walkthrough + feedback + role assignment. Brief is shared in the repo: `pilots/celo-hackathon-2026/brief.md`

The narrative arc comes from Will Ruddick's work: sensing → meaning-making → caring → committing → coordinating → learning. We're making the ancient coordination patterns (Mweria, Meitheal, Chama) legible in a federated knowledge graph. AI and Celo are layers — stewardship is the foundation.

Build sequence:
- Day 1: Seed demo data + routing scorer endpoint
- Days 2-4: Web form + steward review UI
- Days 3-5: MCP tools (agent-assisted commitment drafting)
- Days 5-8: Celo adapter (stretch)
- Days 8-10: Demo recording + submission

Roles:
- Darren: Routing logic, API, MCP tools, Celo adapter
- Benjamin: Web form UX, flow viz adaptation, demo polish

If you want to contribute or have feedback on the storyboard, hop in. The demo storyboard is at `pilots/celo-hackathon-2026/demo-storyboard.md`.
