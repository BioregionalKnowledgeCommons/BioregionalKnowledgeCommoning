# Bioregional AI Swarms: A Pattern Language
*A living document for the bioregional swarm coordination ecosystem*
*BKC as reference implementation — patterns are framework-agnostic*

---

## Purpose

This document captures eight reusable patterns that have emerged from building and observing bioregional knowledge commons infrastructure. These patterns are offered to the broader bioregional AI swarms community as a shared vocabulary — not BKC-specific technology, but recurring design solutions that any project in this space will encounter.

The patterns follow the Alexander/Hillman tradition: each names a recurring problem, describes the forces in tension, and proposes a generative solution. BKC is the primary reference implementation, but the patterns apply to Clawsmos, co-op.us, and any future bioregional coordination project.

**Relationship to existing BKC pattern language:** This document extends `pattern-language-for-bioregional-knowledge-commoning-v0.1.md`. That document addresses the governance and interoperability patterns. This document addresses the multi-agent coordination patterns that emerge when you add AI swarms to the picture.

---

## Pattern 1: Holonic Node

**Context:** A bioregional community wants to participate in a larger swarm coordination network without losing its internal sovereignty or becoming a mere data endpoint.

**Problem:** How do you design a node that is simultaneously self-governing (a whole) and part of a larger coordinating whole?

**Forces:**
- Internal complexity (governance, identity, local knowledge) vs. external simplicity (what the network sees)
- Sovereignty (the node's right to refuse, filter, consent) vs. federation (the network's need for coordination)
- Specialization (the node's unique bioregional knowledge) vs. interoperability (shared protocols)

**Solution:** Design each node as a **holon** — an entity that presents a coherent, bounded interface outward while remaining internally plural and self-governing. The node can act as a single "agent" from the outside (accepting queries, publishing knowledge, executing governance decisions) while internally being a human collective with its own processes. The boundary is the governance membrane.

**Tradeoffs:** More complex than a flat node architecture; requires deliberate boundary design. Internal changes are invisible to peers unless explicitly federated.

**Implementation Signals:**
- A node has a defined identity (name, geographic scope, public key)
- External agents can query the node without knowing its internal structure
- The node can refuse or filter federated knowledge based on its own governance
- Human decisions inside the node and AI agent decisions look equivalent from outside

**Anti-Patterns:**
- Treating the node as a passive data endpoint (no sovereignty)
- Treating the node as a fully transparent system (no boundary)
- Designing for nodes to be identical (erases bioregional distinctiveness)

**BKC Reference:** Each KOI node (Octo/Salish Sea, FR, GV, CV) is a holonic node. External agents call the KOI API and get a coherent response; internally, Octo runs an AI agent, human stewards approve commons intakes, and the PostgreSQL graph is locally sovereign. The node's identity is ECDSA-keyed.

---

## Pattern 2: Knowledge Gardener

**Context:** A knowledge graph accumulates entities from many sources (human-entered, AI-extracted, federated from peers). Without active curation, it degrades: duplicates multiply, stale entries persist, quality drops.

**Problem:** How do you maintain a living, high-quality knowledge graph without requiring constant human attention?

**Forces:**
- Human attention is scarce and should focus on high-stakes decisions
- AI curation without oversight creates quality and consent risks
- Batch cleanup is disruptive; incremental maintenance is hard to coordinate
- Knowledge quality is hard to measure automatically

**Solution:** Designate an AI agent whose primary responsibility is **stewardship of the knowledge graph** — not answering questions (that's the chat layer), but actively curating: proposing entity merges, flagging low-quality entries, running quality gates before ingestion, enriching entities from verified sources, and presenting merge candidates to human stewards for decision. The human steward reviews and approves; the AI does the legwork.

**Tradeoffs:** Requires trust calibration — the gardener must be conservative (present options, not act unilaterally). Over-curation can flatten valuable local knowledge.

**Implementation Signals:**
- Quality gates run before any knowledge enters the graph (not after)
- Merge candidates are surfaced to humans, not auto-merged
- The agent has read access to the graph but write access only through a governed intake path
- CAT receipts (or equivalent provenance records) log what the gardener did and why

**Anti-Patterns:**
- A chatbot that also writes to the knowledge graph (mixing roles)
- Batch curation without human review points
- Treating all knowledge sources as equally trusted

**BKC Reference:** Octo is the Knowledge Gardener for the Salish Sea node. It runs 4-stage quality gates (structure → content → consistency → entity-check), surfaces merge candidates, and creates CAT receipts for every provenance-sensitive action. It does not auto-approve its own writes.

---

## Pattern 3: Consent Membrane

**Context:** Knowledge crosses boundaries between communities, bioregions, and agents. Some knowledge should flow freely; some is community-specific; some is personal or sensitive.

**Problem:** How do you enforce consent boundaries without making sharing so cumbersome that it doesn't happen?

**Forces:**
- Knowledge discovery requires some openness (hard to share what can't be found)
- Sovereignty requires some restriction (communities must control what crosses their boundary)
- Consent must be meaningful (not just a checkbox)
- Different boundaries apply at different scales (local → bioregional → global)

**Solution:** Implement a staged intake process where knowledge crossing a boundary moves through explicit consent states: **staged** (proposed, not yet visible) → **approved** (reviewed and accepted) → **ingested** (in the graph, federable). Each stage has a defined actor (proposer, steward, system). The boundary is the membrane; the stages are the membrane's gates. Rejections and approvals are logged immutably so the consent record outlives any particular system.

**Tradeoffs:** Adds latency between knowledge production and graph availability. Requires steward attention for approvals. Approval fatigue is a real risk.

**Implementation Signals:**
- Knowledge in transit has a visible state (not just "in" or "out")
- Approvals are logged with actor, timestamp, and rationale
- There is a defined fallback when stewards are unavailable (hold, not auto-approve)
- Consent metadata travels with the knowledge artifact

**Anti-Patterns:**
- A single "share" button with no consent record
- Auto-approval after a timeout
- Treating all content as equally sensitive (approval fatigue)
- Consent that's only recorded in the UI, not in the data model

**BKC Reference:** BKC's commons intake: staged → approved → ingested. Decision log is INSERT-only (immutable). Boundary types: visibility (who can see), consent (who approved), conflict (who can resolve). Per-node steward authorization via `commons_memberships` table.

---

## Pattern 4: Cosmolocal Split

**Context:** A multi-bioregion network needs shared protocols and ontologies so nodes can interoperate, but each bioregion has distinct knowledge, relationships, and governance that should not be homogenized.

**Problem:** What should be shared globally vs. what should remain local?

**Forces:**
- Interoperability requires some standardization (shared vocabulary, shared protocols)
- Bioregional sovereignty requires local control (local knowledge, local relationships, local governance)
- Too much globalization: erases bioregional distinctiveness, imposes outside ontologies
- Too much localism: prevents learning across bioregions, duplicates effort

**Solution:** Split deliberately: **light things global** (protocols, shared ontologies, pattern language, meta-protocol commitments) and **heavy things local** (knowledge graphs, relationships, trust networks, governance decisions). Shared protocols define the interface; local implementations define the content.

**Tradeoffs:** Requires ongoing discipline to maintain the split as systems evolve. Edge cases (should this ontology concept be global or local?) need governance.

**Implementation Signals:**
- Clear documentation of what is in the shared protocol vs. what is local policy
- New ontology terms have a defined process for becoming "global" vs. remaining "local"
- Local knowledge graphs are not replicated in full across all nodes
- Shared protocols are versioned and governed by multi-bioregion consensus

**Anti-Patterns:**
- "One true knowledge graph" shared by all (destroys sovereignty)
- Complete isolation (no interoperability)
- Pretending a single bioregion's patterns are universal defaults

**BKC Reference:** BKC's three layers: Pattern Language (global, human), Meta-Protocol (global, machine-minimal), Reference Profiles (local, implementable). KOI nodes share the protocol and ontology schema; each node's knowledge graph is locally held. SOUL.md defines the cosmolocal philosophy for Octo.

---

## Pattern 5: Practices → Protocols

**Context:** A new domain (bioregional governance, ecological stewardship, Indigenous knowledge management) needs a protocol or ontology. The temptation is to design the protocol first and ask communities to conform.

**Problem:** How do you build a protocol that actually reflects community practices rather than imposing outside assumptions?

**Forces:**
- Protocol design benefits from generalizability (abstract patterns that work everywhere)
- Community practices are specific, contextual, and often tacit
- Top-down ontologies tend to reflect the designer's worldview, not the community's
- Bottom-up emergence can be slow and may not converge to interoperability

**Solution:** Start with **observation of existing practices** — in place, community by community, ideally Indigenous-led where Indigenous knowledge is at stake. Abstract those into **patterns** that recur across contexts. Codify patterns into **protocols** only after sufficient practice-grounding. Test protocols against the practices that generated them. Accept that the first protocol is v0.1, not the final answer.

**Tradeoffs:** Slower than designing a protocol from first principles. Requires ethnographic skill alongside technical skill. Early protocols may be incomplete.

**Implementation Signals:**
- Protocol design process includes practice documentation phase
- Community members are co-authors of the ontology, not just informants
- Pattern language predates (and generates) the protocol
- Protocol revisions are explicitly tied back to practice observations

**Anti-Patterns:**
- "We'll map community X's knowledge to our ontology"
- Treating community knowledge as input to be processed, not co-created
- Publishing a v1.0 protocol before testing it against actual practices

**BKC Reference:** BKC COP methodology (from Bill Baue, Feb 9 meeting): practices → patterns → ontologies. BKC's onboarding playbook documents practices first via structured interviews. The BKC ontology is explicitly versioned as evolving with community input.

---

## Pattern 6: Personal Claw

**Context:** In a multi-agent swarm, each human participant generates context — emails, meetings, projects, relationships, tasks — that is relevant to their collective work but is held in fragmented personal tools.

**Problem:** How does an agent provide a coherent, personal-context-aware interface for a human participant without violating their privacy or requiring them to re-enter information constantly?

**Forces:**
- Personal context makes collective intelligence more useful (knowing who knows what)
- Personal data is sensitive and must not leak to unauthorized parties
- Context fragmentation (email, calendar, notes, tasks) reduces agent effectiveness
- Per-person agents add system complexity

**Solution:** Give each human participant a **personal context agent** with access to their personal knowledge sources (email, calendar, notes, vault) AND shared tools (commons ingest, query, federation). The agent resolves entities contextually (knows that "Clare" means Clare Attwell from your specific working group), surfaces relevant collective knowledge filtered through personal context, and respects the consent boundary between personal and shared. The personal layer never auto-shares without explicit action.

**Tradeoffs:** High operational complexity (one agent per human). Sensitive personal data requires strong access controls. Personal agents can drift if not maintained.

**Implementation Signals:**
- Personal agent can access both private and shared knowledge sources
- Sharing from personal context to commons requires explicit action (not auto-share)
- Entity resolution is contextual (resolves names differently for different people)
- Personal agent is distinct from the Knowledge Gardener (different roles, different access)

**Anti-Patterns:**
- One shared agent with access to everyone's personal data
- Personal agents that can write to the commons without consent step
- Personal context that is never connected to shared knowledge

**BKC Reference:** `personal-koi-mcp` — 53-tool MCP server with 15-tool portable contract core + 38 personal extensions (email, vault, Claude Code sessions, shared documents with permission modes). Contextual entity resolution uses phonetic + org/project affiliation. Document sharing has explicit permission modes (root_only, root_plus_required, context_pack).

---

## Pattern 7: Summarizer Pipeline

**Context:** Group coordination generates structured outputs — meeting recordings, governance decisions, project updates — that should be preserved in a shared knowledge graph but rarely are, due to the effort of manual transcription and structuring.

**Problem:** How do you convert the outputs of coordination (meetings, decisions, discussions) into structured knowledge automatically, without losing meaning or manufacturing false precision?

**Forces:**
- Manual knowledge capture is a bottleneck (who takes notes? who enters them?)
- Automated extraction creates noise and false precision if unreviewed
- Knowledge that isn't captured doesn't accumulate; every meeting starts from scratch
- Meeting participants have authority over what gets published from their session

**Solution:** Build a pipeline from **capture** (transcript or recording) through **extraction** (entity recognition, relationship identification, task identification) through **staging** (proposed knowledge, not yet published) through **review** (human approval of proposed entities and relationships) through **ingest** (into the commons graph). Each stage is distinct; the pipeline can be interrupted for review. Idempotency keys prevent duplicate entries if the pipeline runs more than once on the same content.

**Tradeoffs:** Requires transcript quality; fails gracefully with poor transcripts. Review step is necessary but can become a bottleneck. Entity resolution quality matters a lot.

**Implementation Signals:**
- Transcripts are the primary input, not notes (higher fidelity)
- Entity extraction proposes, does not assert
- Duplicate prevention via idempotency (same meeting processed twice = same result)
- The pipeline has a human review gate before commons publication
- Action items from meetings create tasks, not just mentions

**Anti-Patterns:**
- Publishing meeting transcripts verbatim to a shared knowledge graph
- Auto-ingesting every extracted entity without review
- Building per-platform integrations instead of a transcript-level abstraction

**BKC Reference:** `darren-workflow` meeting pipeline: MacWhisper/Otter → structured meeting note → entity extraction → wikilinks → backend ingest (via `/process-note`). Idempotent taskKeys prevent duplicate task creation. Owner parsing + alias resolution for action item attribution. Verification gates (YAML, dangling wikilinks, mentionedIn completeness) before pipeline completes.

---

## Pattern 8: Evidence Loop

**Context:** Capital allocation decisions (bounties, grants, resource flows) in a regenerative economy should be grounded in verified knowledge — what was done, by whom, with what ecological impact — not just proposals or assertions.

**Problem:** How do you connect knowledge evidence to capital allocation in a way that creates a virtuous feedback loop: better knowledge → better decisions → more accountable resource flows?

**Forces:**
- Capital allocation without evidence is opaque and gameable
- Evidence tracking adds overhead to every action
- The agents making decisions need to access the evidence (knowledge commons as substrate)
- Capital flows should be logged as evidence themselves (circularity: allocations become part of the evidence base)

**Solution:** Build an explicit loop: **Knowledge entities** (project outcomes, ecological measurements, governance decisions) generate **evidence claims** (Hypercerts, EAS attestations, or equivalent). Evidence claims inform **capital allocation decisions** (bounty payouts, grant recommendations, work orders). Allocation decisions are logged as **evidence entities** in the knowledge graph, closing the loop. Each step is auditable; the loop is visible.

**Tradeoffs:** Requires all three systems (knowledge, evidence, capital) to have compatible data models. High-stakes allocation decisions still require human oversight. Evidence quality depends on knowledge quality.

**Implementation Signals:**
- Capital allocation decisions reference knowledge entity RIDs (not just descriptions)
- Allocation outcomes are logged as Evidence entities with provenance
- Evidence claims are machine-readable and linked to the underlying knowledge artifacts
- Bounded autonomy: small allocations automated; larger ones require human multisig

**Anti-Patterns:**
- Capital allocation with no knowledge grounding (grants based on proposals, not evidence)
- Knowledge produced for allocation purposes but not reused for other decisions
- Allocation decisions that are not themselves logged as evidence

**BKC Reference:** TBFF bridge — Knowledge→Flow→Evidence loop. Finance decisions are logged as Evidence entities with RIDs. Planned: Hypercerts from KOI Evidence entities, EAS attestations from governance decisions. Bounded authority model: automated below threshold, multisig above.

---

## BKC as Reference Implementation

BKC instantiates all eight patterns in a live, production system across 4 federated nodes:

| Pattern | BKC Implementation | Status |
|---|---|---|
| Holonic Node | 4 KOI nodes (Octo/Salish Sea, FR, GV, CV) with ECDSA identity | ✅ Production |
| Knowledge Gardener | Octo AI agent with 15-tool KOI contract, 4-stage quality gates | ✅ Production |
| Consent Membrane | Commons intake (staged → approved → ingested), immutable audit log | ✅ Production |
| Cosmolocal Split | Three-layer architecture (pattern → protocol → profile), local knowledge graphs | ✅ Production |
| Practices → Protocols | BKC COP practice-interview methodology, BKC ontology as living document | ✅ Active |
| Personal Claw | `personal-koi-mcp` — 53 tools, contextual entity resolution, permission modes | ✅ Production |
| Summarizer Pipeline | `darren-workflow` — MacWhisper → entity extraction → governed ingest | ✅ Production |
| Evidence Loop | TBFF bridge, Evidence entities with RIDs, planned Hypercerts/EAS | 🔶 Partial |

**The portable contract:** The 15-tool KOI contract core (search, ingest, federate, curate web, manage commons, query graph) is the minimum interface any agent needs to participate in a holonic knowledge commons. It is designed to be exposed via A2A Agent Cards for zero-friction agent-to-agent discovery.

---

## Invitation

These patterns are offered as a contribution to the emerging bioregional AI swarms community. If you're building in this space — coordination agents, knowledge commons, regenerative capital flows — you are probably encountering these same problems. BKC is happy to be a reference implementation, a conversation partner, and a test bed for new patterns you discover.

**Current open questions (contribute your practice):**
- What does the Consent Membrane look like for real-time coordination (vs. async knowledge)?
- How should the Evidence Loop handle disputed or contradictory evidence?
- What is the right granularity for a Holonic Node (watershed? city? organization?)?
- How do the patterns interact with Indigenous data sovereignty frameworks?

*This document is versioned and maintained by the BKC community. Changes follow the decision-issue process in `BioregionalKnowledgeCommoning/.github/`.*

---

**Attribution:** Bioregional Knowledge Commons (BKC) — Darren Zal, Salish Sea Bioregion. This document draws on: BKC COP practice interviews (Bill Baue, Eli Ingraham, Simon Grant), Clawsmos architecture (AG Neyer, Lucian), co-op.us/nou-techne (Todd Youngblood), and the broader bioregional AI swarms Telegram community. Pattern language methodology after Christopher Alexander and Hillman.

*Last updated: 2026-02-28 | Version: v0.1-swarms*
