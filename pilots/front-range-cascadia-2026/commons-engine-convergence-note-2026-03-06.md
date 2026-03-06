# Commons Engine Convergence Note - 2026-03-06

## Purpose

Short Telegram message responding to Benjamin Life's Commons Engine spec. To be posted as a separate message after the async seed pack lands. Tone: collaborative, appreciative, non-prescriptive.

## Context

Benjamin is a co-steward in the BKC pilot (triad with Darren and Shawn). He built the globe visualizer we forked and wired to live KOI data. The Commons Engine spec describes an agent-native collaborative knowledge commons toolkit — primarily a UX/editor/moderation layer that explicitly uses KOI as federation plumbing.

The spec does not reinvent our backend work. It designs the frontend layer that makes graph-native knowledge commoning accessible to non-technical communities.

## Convergence Map

| Commons Engine Layer | BKC/Octo Infrastructure | Status |
|---------------------|------------------------|--------|
| Edit tab (agent sidebar) | `/chat`, `/entity-search` | Live |
| Edit tab (save) | GitHub push -> webhook -> `/ingest` | Adapter needed |
| Moderation tab | `/commons/web/process` (entity preview) | Live |
| Publish tab | `/register-entity` + vault notes + Quartz | Live |
| Federation tab | KOI-net protocol endpoints | Live, 4 nodes |
| Agent-to-agent | `/chat` + KOI-net | Infrastructure exists |
| `schema.yaml` | `bkc-ontology.jsonld` + mapping workflow | Live (local_type / canonical_type / mapping_status) |
| OPAL onboarding | onboarding playbook + setup-node.sh | Docs exist, UX gap |

Key observation: the Commons Engine maps to Profile A (Non-KOI Node) in our node-participation-profiles.md — GitHub as backend with adapter export to the shared graph.

## Telegram Message (Post 2 of 2)

Post this as a direct reply to Benjamin's Commons Engine message, after the seed pack has landed.

---

Really appreciate the thinking in this, Benjamin. The Commons Engine framing — "the Visualizer is the map, this is the territory" — is exactly right.

I see strong convergence between your spec and what I've been building on the backend. The knowledge graph federation is running across 4 nodes with signed envelopes. The schema bridge concept you describe maps well to the ontology mapping workflow we've been developing. The consent governance piece is enforced at the database level now.

Your spec makes the community-facing layer much clearer — the collaborative markdown editing, the GitHub-native moderation flow, the OPAL onboarding, the democratic publishing. That's what makes this accessible to communities who aren't running things from the command line, and it's built on the visualizer foundation you already laid.

If it's useful, the infrastructure side is available to build against: https://salishsee.life/commons has the live graph, search, chat, and ingest. Happy to walk through the API surface whenever that would help.

---

## Why This Message Works

- Frames the work as converging, not as one layer sitting on top of the other
- Credits the visualizer foundation in context (not in the seed pack)
- Offers availability without imposing architecture
- Keeps it conversational, not spec-like
- Leaves the integration conversation for Benjamin to drive

## Follow-Up Integration Work (If Convergence Conversation Proceeds)

These would be separate implementation plans, driven by the collaboration:

1. Commons Engine integration quickstart doc
2. Reference `schema.yaml` for Salish Sea commons
3. GitHub webhook -> KOI `/ingest` adapter (bridges Profile A into the live graph)
4. Updated pilot plan to include Commons Engine as the community UX layer

## Network-Specific Callouts (Optional 1:1 Follow-Ups)

Not for the group channel. Consider direct messages if the seed pack generates interest:

- **Kevin (owocki)** — Commitment pooling is in the ontology and API (C0 landed). The `/commitments/` and `/pools/` endpoints are live. Could note what's available for Gitcoin integration.
- **Todd** — A2A agent card is live at `/agent-card`. co-op.us task->Evidence pipeline is planned (B4 TBFF). Worth a direct note about interop surface.
- **AG (Neyer)** — Clawsmos Summarizer -> `/ingest` integration contract exists at `Octo/docs/integration/summarizer-ingest-contract.md`. Direct follow-up with concrete endpoint details.
