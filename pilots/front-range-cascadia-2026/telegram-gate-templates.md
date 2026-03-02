# Telegram Gate Templates — Mar 3-5 Build Day
*Pre-drafted messages for Gate A/B decision points and expanded Telegram post*

---

## Gate A — Tuesday, March 3, 12:00 PM MT

### Template A1: Summarizer Confirmed

> Build-day update from BKC:
>
> AG Neyer confirmed — Clawsmos Summarizer will wire to BKC `/ingest` for Mar 5.
>
> **What this means for Thu:** We'll demo the full Summarizer pipeline live — transcript goes in one end, entities appear in the federated knowledge graph at the other. Governance membrane approves. Graph-grounded chat answers questions about what just arrived.
>
> **Technical next step:** Running Gate B contract checks by 6pm today. Token rotation + sample call against the frozen contract. If it passes, we're locked for demo.
>
> Integration contract: `summarizer-ingest-contract.md` in the BKC repo.

### Template A2: Summarizer Not Confirmed (Fallback)

> Build-day update from BKC:
>
> No confirmation from Clawsmos Summarizer team yet — proceeding with standalone BKC demo path for Mar 5. Integration slot stays open.
>
> **What we'll show Thu:** BKC's full knowledge commons pipeline — 4-node federation, governance membrane, entity resolution, and graph-grounded chat. We'll use a staged sample payload to demonstrate the Summarizer ingest flow, proving the contract works end-to-end.
>
> **Open offer:** Anyone who wants to wire a Summarizer (or any structured extraction pipeline) to BKC can use the frozen contract at `summarizer-ingest-contract.md`. Happy to pair this week.

---

## Expanded Telegram Post — Three-Plane Framing

*Use this as the primary build-day positioning message (works for both Gate A outcomes):*

> **Bioregional AI Swarms — what's live, what's next, and what we need from each other**
>
> The coalition is building across three planes:
>
> **Knowledge Plane** (BKC) — persistent truth layer
> - 4-node federation live: Salish Sea, Front Range, Greater Victoria, Cowichan Valley
> - 640+ entities, governance membrane (staged → approved → ingested), graph-grounded chat with 6-8 cited sources
> - Summarizer pipeline ready: transcript → entities → federated graph
>
> **Coordination Plane** (Clawsmos + co-op.us) — real-time agent layer
> - Matrix rooms + agent roles (Summarizer, Orchestrator, Moderator, Representative)
> - A2A agent cards live for cross-agent discovery
> - co-op.us agent API + task allocation building
>
> **Capital Plane** (owockibot + Gitcoin) — value flow layer
> - Treasury allocation with bounded authority
> - Hypercerts from Evidence entities
> - co-op patronage engine
>
> **Integration seams we're offering:**
> 1. `/ingest` — any Summarizer can write structured entities to BKC (frozen contract, token-authed)
> 2. `/chat` — any agent can query the knowledge graph for grounded answers
> 3. A2A Agent Card at `/.well-known/agent-card.json` — 15-tool KOI contract for capability discovery
> 4. KOI-net federation — any new bioregion node can join the mesh
>
> **What we need from the coalition:**
> - Who wires the first external Summarizer pipeline to `/ingest`?
> - Who owns the social narrative layer (clips, posts, audience building)?
> - When is the first recurring cross-plane sprint?
> - What scope for GG25-29 round proposals?
>
> Happy to pair with anyone who wants to connect action-plane outputs to evidence entities in the commons. DM or reply here.
>
> — Darren (BKC / Salish Sea)

---

## Gate B — Tuesday, March 3, 6:00 PM MT

### Template B1: Scope Lock — Summarizer Integration Confirmed

> **Gate B: Scope lock confirmed** ✓
>
> Summarizer contract sample call passed. Token rotated and shared out-of-band with AG Neyer.
>
> Locked for Mar 5:
> - Segment 4 = Live Summarizer pipeline demo (transcript → entities → graph → chat)
> - Contract: `summarizer-ingest-contract.md`
> - Fallback: staged payload if live feed has issues
>
> No new code after Gate C (Wed 6pm MT). Feature freeze.

### Template B2: Scope Lock — Standalone Demo Path

> **Gate B: Scope lock confirmed** ✓
>
> Proceeding with standalone BKC demo path. Summarizer segment uses staged sample payload.
>
> Locked for Mar 5:
> - Segment 4 = Staged Summarizer pipeline demo (sample payload → entities → graph → chat)
> - Integration slot documented and open post-demo
> - Contract published for async integration
>
> No new code after Gate C (Wed 6pm MT). Feature freeze.

---

*Templates owner: Darren Zal | Created: 2026-03-02 | For use in Telegram bioregional-ai-swarms channel*
