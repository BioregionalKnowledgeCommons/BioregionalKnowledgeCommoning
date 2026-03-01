# Mar 5 Build Day — Demo Runbook
*30-minute segment | Thu Mar 5, 2026 at 2pm MT | Build Day: Bioregional AI Swarms*

**Demo operator:** Darren Zal
**Runbook status:** DRAFT — complete Gate C verification by Mar 4, 18:00 MT
**Fallback:** 8-step BFF demo (existing system, no external integration required)

---

## Pre-Flight Checklist (complete by Mar 4, 18:00 MT)

### Node Health

> **URL structure note:** App runs at `basePath: '/commons'`. Node IDs use full slugs.

```bash
# Check all 4 nodes — expect 200 with healthy status
curl https://45.132.245.30.sslip.io/commons/api/nodes/octo-salish-sea/health
curl https://45.132.245.30.sslip.io/commons/api/nodes/front-range/health
curl https://45.132.245.30.sslip.io/commons/api/nodes/greater-victoria/health
curl https://45.132.245.30.sslip.io/commons/api/nodes/cowichan-valley/health
```
- [ ] All 4 nodes return healthy status
- [ ] Globe at `https://45.132.245.30.sslip.io/commons` loads with all node markers visible

### Auth
- [ ] Steward account (Darren's WebAuthn passkey) works — sign in at `https://45.132.245.30.sslip.io/commons/` then open a node panel and switch to the Commons tab
- [ ] Demo operator named, credentials tested

### Pre-Stage Helper (Segment 3 — Commons Governance Demo)

Pre-create a staged entity in Octo's commons queue by sending a KOI-net share event from the FR node. Run this before the demo starts.

```bash
ssh root@45.132.245.30 'curl -s -X POST http://127.0.0.1:8355/koi-net/share \
  -H "Content-Type: application/json" \
  -d "{
    \"document_rid\": \"orn:fr.meeting:build-day-demo-entity:2026-03-05\",
    \"recipient\": \"orn:koi-net.node:octo-salish-sea+f06551d75797303be1831a1e00b41cf930625961882082346cb3932175a17716\",
    \"recipient_type\": \"commons\",
    \"message\": \"Build day demo entity for commons governance demo\",
    \"share_mode\": \"root_plus_required\"
  }" | python3 -m json.tool'
```

**Verify:** Sign in at `https://45.132.245.30.sslip.io/commons` → click Salish Sea node → Commons tab → confirm ≥1 staged item is pending approval.

- [ ] Pre-stage helper run — commons queue has ≥1 staged item ready to approve

---

### Integration Seam (if Gate B confirmed)
- [ ] `x-ingest-token` shared with AG Neyer
- [ ] At least one test call to `/commons/api/nodes/octo-salish-sea/ingest` succeeded (see `Octo/docs/integration/summarizer-ingest-contract.md`)
- [ ] Clawsmos Summarizer has the token and full endpoint URL (including `/commons` prefix)

### Fallback
- [ ] 8-step BFF demo walkthrough reviewed (see Section 5 below)
- [ ] Chat prompts pre-tested (see Section 2)
- [ ] Commons intake test entity staged and ready to approve live

---

## 1. Demo Script (30 min)

### Segment 1 — Live 4-Node Federation on the Globe (2 min)

**What you're showing:** The network is real and running.

**Steps:**
1. Open `https://45.132.245.30.sslip.io/commons` on shared screen
2. Globe should load with 4 node markers (Salish Sea/Octo, Front Range, Greater Victoria, Cowichan Valley)
3. Click each node marker — node card opens with Knowledge Panel showing entity count, health status, federated peers
4. Say: *"This is a live 4-node bioregional knowledge network. Each node is an autonomous knowledge commons. They federate via KOI-net — signed envelopes, consent-gated publication. The Salish Sea node is the coordinator. All of this is running right now."*

**Fallback if globe doesn't load:** Navigate to `https://45.132.245.30.sslip.io/commons/entities` directly and show the entity list with node filters.

---

### Segment 2 — Chat Grounded in Knowledge Graph (5 min)

**What you're showing:** Knowledge-grounded AI responses, not hallucination.

**Steps:**
1. Click the Salish Sea node marker → node card opens → click **Chat** tab in the Knowledge Panel
2. Enter pre-tested prompt:
   > *"What organizations are working on bioregional knowledge commons, and what are their relationships to each other?"*
3. Wait for response (<6 seconds). Response should cite entity sources (6-8 sources).
4. Show sources panel — point to entity URIs and relationship citations
5. Try a front-range specific prompt:
   > *"What projects in the Front Range are connected to regenerative practice?"*
6. Say: *"Every answer is grounded in the knowledge graph. You can trace any claim to its entity source. No hallucination — if it's not in the graph, the model says so."*

**Pre-tested prompts (confirm these work the day before):**
- "What organizations are working on bioregional knowledge commons?"
- "Who attended BKC meetings and what projects are they affiliated with?"
- "What is the relationship between the Salish Sea and Front Range nodes?"
- "What ecological stewardship practices are documented in the Cascadia region?"

**Fallback if chat is slow:** Have a pre-recorded screen capture of a successful chat response.

---

### Segment 3 — Commons Intake Governance (5 min)

**What you're showing:** The governance membrane — human approval required before knowledge crosses the boundary.

**How staging works:** The commons-intake queue is populated via **KOI-net share events** (`/koi-net/share` with `recipient_type=commons`), not via `/ingest`. The `/ingest` endpoint writes directly to the graph. For this demo segment, the staged entity must be pre-created via the KOI-net share path, or use an existing merge candidate in the queue.

**Pre-setup (before demo):** Create a staged entity by sending a KOI-net share event from the FR node to Octo, or manually insert a test merge candidate via the admin API. Confirm a pending item appears in the commons queue before the demo starts.

**Steps:**
1. Click the Salish Sea node marker → node card opens → click **Commons** tab in the Knowledge Panel (requires steward login via WebAuthn passkey)
2. Show the merge candidate queue — the pre-staged entity appears awaiting review
3. Click "Approve" — entity moves from staged → ingested
4. Switch to the **Knowledge** tab — the approved entity now appears in the graph
5. Say: *"Every piece of knowledge crossing a boundary requires a steward decision. This is the governance membrane. It's not a feature we're planning — it's running right now. The decision is logged immutably."*

**If Clawsmos Summarizer integration is live:** The `/ingest` call from AG Neyer creates entities directly in the graph (no staging required — they're immediately visible). The governance demo then runs separately with a pre-staged merge candidate to show the consent layer. Both features can be shown in the same segment.

**Fallback:** If the commons queue is empty, show the merge candidate queue UI and explain the pattern. Approve a pre-staged entity if available. If nothing is staged, skip to showing the immutable decision log instead.

---

### Segment 4 — TBFF Bridge (Evidence Loop) (5 min)

**What you're showing:** Knowledge → capital connection. Evidence loop closing.

**Steps:**
1. Show an Evidence entity in the entity browser (or create one live via chat/demo)
2. Explain: *"In this system, governance decisions and project outcomes are stored as Evidence entities with unique RIDs. These RIDs can be referenced by capital allocation systems — bounties, grants, work orders."*
3. Show the TBFF bridge concept: *"We have a bridge that converts Knowledge entities → Evidence claims → Hypercerts (planned) and EAS attestations. The owocki PRD describes exactly this model. We've already built the knowledge half."*
4. Say: *"Your bounty of 1k USDC for the bioregional swarm — when it's allocated, that allocation becomes an Evidence entity in this graph. The evidence loop closes: knowledge informs capital, capital flows are themselves knowledge."*

**Note:** This segment is more concept + live demo of entities than a live capital transaction. The Hypercerts integration is planned, not yet deployed.

---

### Segment 5 — Open Question to the Room (10 min)

**What you're showing:** BKC is an infrastructure provider, not a competitor. Inviting collaboration.

**Steps:**
1. Switch to the Two-Plane Architecture diagram (from the positioning one-pager)
2. Say: *"BKC is the knowledge plane. You're building the action plane. The natural integration seam is: your Summarizer writes to our `/ingest`; your agents query our `/chat`. Here's the MCP/A2A surface. The 15-tool KOI contract is ready to be published as an A2A Agent Card — any agent in the room can auto-discover BKC's capabilities."*
3. Open to questions:
   - *"Who wants to wire up their Summarizer?"* (to AG Neyer)
   - *"Who wants to reference knowledge-graph-grounded evidence in your bounty allocations?"* (to owocki)
   - *"Who wants their task completions logged as Evidence entities?"* (to Todd)
4. End with: *"The pattern language doc I shared in Telegram documents what BKC has built as 8 reusable patterns. Take the patterns. Fork the implementation. Build your own holonic node."*

---

## 2. Fallback: Core Demo (No External Integration)

If external integration is not ready, run the core demo using only the existing system:

1. Open globe at `https://45.132.245.30.sslip.io/commons` — show 4 live nodes
2. Click a node marker — open Knowledge Panel; show entity count, health, federated peers
3. Search for an entity (e.g., "Salish Sea" or "regenerative practice") — show results
4. Open entity detail at `/commons/entities` — show linked relationships and bioregional context
5. Switch to **Chat** tab on Salish Sea node — run a grounded query, show cited sources
6. Switch to **Commons** tab (steward login required) — show the governance queue
7. Approve a staged entity live — show it appearing in the Knowledge tab
8. Point to federation arcs on globe — explain how entities propagate to peer nodes

**This demo requires zero external dependencies and has been verified in production.**

---

## 3. Timing Guide

| Segment | Time | Bailout if over |
|---|---|---|
| Setup/intro | 0:00–0:02 | Skip intro, go straight to globe |
| Globe: 4-node federation | 0:02–0:04 | Move to chat at 0:04 |
| Chat: grounded knowledge | 0:04–0:09 | Cut to commons intake at 0:09 |
| Commons intake governance | 0:09–0:14 | Cut to TBFF at 0:14 |
| TBFF bridge / evidence loop | 0:14–0:19 | Cut to open discussion at 0:19 |
| Open discussion | 0:19–0:30 | Hard stop at 0:30 |

---

## 4. Setup Requirements

**Technical:**
- Laptop with browser open to `https://45.132.245.30.sslip.io/commons` (preloaded, not cold-loaded)
- WebAuthn passkey works in this browser/device
- Screen share configured and tested
- Backup: second device with same URLs open

**Accounts:**
- Darren's steward account active in the Salish Sea node panel → **Commons** tab
- If AG Neyer is live: their ingest token confirmed working

**Connection:**
- Venue WiFi tested OR personal hotspot as backup
- SSH to Octo server available if emergency restart needed: `ssh root@45.132.245.30`

**Emergency restart (if a node is down):**
```bash
ssh root@45.132.245.30
systemctl status koi-api        # Octo node (port 8351)
systemctl status fr-koi-api     # FR node (port 8355)
systemctl restart koi-api       # restart Octo if needed
systemctl restart fr-koi-api    # restart FR if needed
# GV is on a separate server:
ssh root@37.27.48.12 "systemctl restart gv-koi-api"
```

---

## 5. Rollback Decision Tree

```
Is Clawsmos Summarizer integration live?
├── Yes → Run full 5-segment demo (Sections 1-5 above)
└── No → Is all 4 nodes healthy?
    ├── Yes → Run 8-step BFF demo (Section 2 above) + segments 2-5 adapted
    └── No → Which nodes are down?
        ├── Only GV or CV down → Run demo with 3 nodes, mention GV/CV as remote
        ├── FR down → Run demo Salish Sea + GV + CV only
        └── Octo down → ABORT LIVE DEMO. Show pre-recorded screen capture.
                         Say: "We had a server incident this morning. Here's what it looks like working."
```

---

## 6. Post-Demo

After the segment:
- Share the positioning one-pager in the Telegram channel
- Share the `summarizer-ingest-contract.md` with AG Neyer for follow-up integration
- Share the pattern language doc link with the group
- Log any live decisions or entity approvals done during the demo as a Meeting entity via the pipeline

---

*Runbook owner: Darren Zal | Last updated: 2026-02-28 | Gate C deadline: 2026-03-04 18:00 MT*
