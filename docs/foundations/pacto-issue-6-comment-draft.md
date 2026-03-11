# Draft comment for regen-network/pacto-framework#6

> Post this as a comment on the issue after review.

---

Hey Greg — thanks for the thoughtful framing in this issue. I've written a convergence document mapping BKC's current infrastructure to each of your five gaps: [pacto-bkc-convergence-v0.1.md](https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning/blob/main/docs/foundations/pacto-bkc-convergence-v0.1.md)

**Quick summary of where we converge vs. where work is needed:**

**Strongest convergence (live infrastructure):**
- **Gap 3 (Evidence trail):** BKC's append-only `claim_state_log` + proof packs provide exactly the kind of rigorous provenance chain PACTO describes. Each state transition from initial assertion through peer review to on-chain anchoring is recorded with actor, reason, and evidence references.
- **Gap 4 (Regen Ledger):** We have the most concrete integration I'm aware of — BLAKE2b-256 content hashing → IRI derivation → MsgAnchor broadcast to regen-upgrade testnet, with 49 claims anchored. The full pipeline (prepare → broadcast → poll → reconcile) handles timeouts gracefully. Honest note: this is testnet, not mainnet.

**Solid foundation (live + designed):**
- **Gap 1 (Workflow objects):** Our interview-commoning plugin produces 3 live artifact types (PracticePacket, PatternCandidatePacket, ProtocolCandidatePacket). These are machine-readable JSON but not yet PACTO-compatible schemas. The convergence doc proposes defining PACTO-compatible schemas and building thin adapters. Happy to draft these as a PR to `core/workflows/` if you think that's the right approach.
- **Gap 2 (Governance):** Our V2 attestation layer provides identity-bound review records (who reviewed what, what they concluded, what evidence they examined). Federation membrane governance controls data flow between nodes. The attestation policy gates (≥1 approved attestation for peer_reviewed, ≥2 for verified) are designed and ready for implementation.

**Weakest convergence (conceptual only):**
- **Gap 5 (DAO DAO):** This is our thinnest area. We have reviewer identity infrastructure (`reviewer_uri` FK, extensible to regen1... addresses) and a proposed minimal seam (DAO DAO roles → BKC steward roles → attestation authority), but no detailed integration design. The convergence doc proposes starting narrow: DAO DAO publishes authorized reviewers, BKC maps them to reviewer_uri entries, attestation gates reference DAO DAO roles.

**The document is deliberately honest about what's live vs. designed vs. not addressed.** BKC is an adjacent precedent — a working system that's encountered the same challenges — not a finished reference implementation.

Would love your feedback on:
1. Does the workflow object mapping (your 6 objects → BKC equivalents) seem right?
2. Is the minimal DAO DAO seam approach (reviewer-role interface) useful, or does PACTO need deeper integration?
3. Interest in a joint testnet demo — running PACTO's 6-step loop through BKC infrastructure?
