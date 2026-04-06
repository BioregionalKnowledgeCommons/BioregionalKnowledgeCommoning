---
doc_id: bkc.kg-chat-follow-on-decision-memo
doc_kind: research
status: active
depends_on:
  - bkc.sprint-1-retro
  - bkc.rag-synthesis
---

# KG Chat Follow-On Decision Memo

**Date:** 2026-04-05  
**Scope:** Post-Sprint-1 retrieval work through Phase 2 Intelligence closure, v1.1 workflow follow-up, B10 scoping, unified search resilience, and targeted ecology source-family testing.

This memo is the durable home for follow-on KG chat lessons that are too important to leave only in session notes, but too detailed to live in the roadmap itself.

## What Goes Where

| Surface | Purpose | What belongs there |
|---|---|---|
| `CLAUDE.md` | Operator handoff and current state | What is live, what is next, deploy notes, active plans |
| `docs/research/*.md` | Durable lessons and falsified hypotheses | Retrospectives, experiment outcomes, keep/defer/reject decisions |
| `docs/roadmap/semantic-roadmap.json` | Committed priorities | Planned work, status, dependencies, explicit deferrals |
| `~/.claude/plans/*.md` | Execution packets | Session-scoped plans, stop conditions, validation steps |

The practical rule: do not treat `CLAUDE.md` as the long-term memory for retrieval research. Use it as a pointer to the durable memo.

## What We Tried After Sprint 1

| Area | Hypothesis | Result | Decision |
|---|---|---|---|
| Prompt hardening | A strict "do not infer" rule would reduce confabulation without hurting answer quality | False as written. AR fell because the model stopped legitimate multi-chunk synthesis. | Keep grounded synthesis, not blanket anti-inference. |
| Page co-occurrence expansion | Adjacent wiki-page chunks would improve mechanism answers | False. It hurt 9/15 mechanism questions and added noise. | Removed. Do not revive without a new targeted hypothesis. |
| Deeper entity-definition retrieval | `entity_definition` needed standard-depth retrieval and text search | False. Enriched entity descriptions at shallow depth performed better. | Keep `entity_definition` shallow when B8a descriptions are strong. |
| Document-primary synthesis clause | Refusal behavior was caused by under-weighting document chunks | True. A one-sentence clause fixed false refusals without regressions. | Ship. Relevant documents are the primary evidence surface. |
| Structured Briefs | A claim-centered explainer format would be more useful than a generic detailed answer | True. Product validation passed and the UI was renamed to `Brief`. | Shipped as Phase 2 closure. |
| Brief-to-claims bridge | Explainer output could become machine-usable without auto-claims | True. `brief_payload` and manual review workflow landed cleanly. | Shipped. Keep human review explicit. |
| Review-workflow helper | Evidence-preparation helper was needed for stewards | False. `/entity-search` already solved claimant lookup, and current brief evidence is mostly document refs. | No helper. Keep the evidence-from-documents gap parked. |
| B10 query decomposition | Multi-hop failures were mainly decomposition failures | False. Audit found `0` clear `DECOMPOSITION` cases; failures were dominated by `CONTENT` and `RANKING`. | Defer B10. |
| Salish Sea ecology wiki packet | A small page packet from `salishsearestoration.org` could fix ecology-heavy multi-hop failures | False. The source family is wrong for reef nets and clam gardens, and too weak for the remaining chains. | Stop this wiki path for those failures. |
| Unified search resilience | Embedding outage should degrade gracefully instead of hard-failing | True. `/knowledge/unified-search` now falls back to text-first search with explicit degraded signaling. | Keep this resilience behavior. |

## Falsified Hypotheses Worth Remembering

1. More retrieval depth is not automatically better. It often adds noise.
2. More retrieval surfaces are not automatically better. `STRUCTURED_SQL`, `RELATIONSHIP_TRAVERSE`, and page co-occurrence expansion all looked plausible and lost under eval.
3. A source family that is ecologically adjacent is not necessarily the right source family. Restoration science is not the same as Indigenous ecological practice.
4. Not every workflow pain deserves automation. The evidence-from-documents gap is a review-and-authorship task, not a narrow transformation helper.

## What Remains Unresolved

| Gap | Current Best Reading | Likely Fix Type |
|---|---|---|
| Reef nets (`multi_hop_3`, `multi_hop_11`) | Not present in current registered wiki corpus | Different source family |
| Clam gardens (`multi_hop_14`) | Not present in current registered wiki corpus | Different source family |
| Eelgrass -> juvenile Chinook -> SRKW chain (`multi_hop_7`) | Pieces exist, explicit chain does not | Authored synthesis note with citations, possibly targeted enrichment later |
| Fraser lifecycle narrative (`multi_hop_13`) | Partial sources, weak narrative coverage | Authored synthesis note or a different authoritative source |
| BKC three-layer architecture (`multi_hop_8`) | Right doc exists but does not rank into context | Ranking / retrieval tuning, not decomposition |

## Roadmap Implications

### Keep

- `B10` as a candidate idea, not the next build by default.
- `B2` HippoRAG, `B11` RAPTOR, and `B12` federated retrieval as trigger-based roadmap items.
- Briefs + claims review as the shipped product baseline.

### Defer

- `B10` until content/source work removes the dominant `CONTENT` failures and leaves at least 3 clear residual `DECOMPOSITION` failures.
- HippoRAG / RAPTOR / federated retrieval until their explicit triggers show up in eval or production use.

### Do Not Revive Casually

- SQL/Cypher as the primary agentic retrieval path.
- Page co-occurrence expansion.
- Another packet from the Salish Sea restoration wiki for reef-net / clam-garden questions.

## Source Strategy Decision Table (2026-04-05)

The targeted Salish Sea ecology-packet experiment falsified the current MediaWiki source family for the hardest remaining ecology-heavy multi-hop failures.

| Question | Current best class | Why | Minimum honest next move |
|---|---|---|---|
| `multi_hop_3` reef nets as Coast Salish technology | `park` | The current registered wiki source family does not cover this concept, and treating Indigenous practice content as a routine import target would require an explicit provenance / rights / scope decision. | Mark as a known content-limit candidate in eval until source policy changes. |
| `multi_hop_7` eelgrass -> juvenile Chinook -> SRKW | `authored_synthesis` | The pieces exist in public ecology sources, but the explicit chain is not stated in one clean chunk in the current corpus. | Author a short cited brief and ingest it. |
| `multi_hop_11` reef net as migration knowledge | `park` | Same as `multi_hop_3`: absent from the current source family, and not appropriate to smuggle in as generic wiki densification. | Mark as a known content-limit candidate in eval until source policy changes. |
| `multi_hop_13` Fraser lifecycle chain | `different_source_family` | The current wiki has only weak lifecycle coverage. Public fisheries/science sources are a better fit than the restoration wiki. | Narrow DFO / PSF source scout, not broad import. |
| `multi_hop_14` clam gardens as Indigenous mariculture | `park` | Same as reef nets: this is a source-scope and provenance decision, not a simple missing-page problem. | Mark as a known content-limit candidate in eval until source policy changes. |

### Supporting Source Read

The current best-supported next actions are:

- `multi_hop_7` authored synthesis from public ecology sources
  - NOAA Fisheries material on Southern Resident killer whale prey dependence on Chinook
  - Pacific Northwest / DFO-adjacent material on eelgrass as juvenile salmon habitat
- `multi_hop_13` narrow source-family scout
  - DFO lifecycle and Lower Fraser habitat-connectivity material
  - Pacific Salmon Foundation lifecycle/public education material

### Eval Hygiene Recommendation

`multi_hop_3`, `multi_hop_11`, and `multi_hop_14` should not continue to function as ordinary retrieval-gate failures unless and until BKC explicitly decides to include a rights-clear source family for Indigenous ecological practice content.

Recommended next eval-contract change:

- add a `known_limit` or equivalent scope annotation to these questions in `golden_qa.json`
- teach the eval gate to exclude known-limit questions from canonical pass/fail calculations while still reporting them

This is not a retrieval improvement. It is a scope / evaluation-discipline improvement.

### Smallest Next Implementation

The smallest plausible high-signal move is **not** another source import. It is a tiny authored-synthesis packet for `multi_hop_7`.

Why:

- it uses public, citeable ecology sources
- it avoids scope creep into culturally sensitive source ingestion
- it tests whether authored synthesis can move one real failure cleanly
- it does not require reopening B10, planner work, or another broad wiki experiment

## Recommended Next Step

The next real RAG/content session should be a **source strategy** session, not another import or planner session.

The goal is to answer:

1. Which failures need a **different source family**?
2. Which failures need an **authored synthesis document** instead of raw import?
3. Which failures are actually **ranking** issues and should stay out of the content lane?

The expected outcome is a small decision table, not a new ingestion sprint by default.

## Revisit Gates

### Revisit B10 only if all are true

- content/source strategy has run
- the newly added sources or authored docs are actually retrievable
- at least 3 residual failures are clearly "content exists, but one-shot retrieval still fails to bridge it"

### Revisit HippoRAG only if one of these is true

- entity/edge scale grows materially beyond current levels
- multi-hop remains weak after content and ranking work

### Revisit RAPTOR only if one of these is true

- broad thematic questions become a meaningful production use case
- thematic eval category remains weak despite normal retrieval improvements

## Canonical References

- `docs/research/rag-techniques-synthesis.md`
- `docs/research/sprint-1-retrieval-retrospective.md`
- `docs/ops/technique-ledger.md`
- `docs/roadmap/semantic-roadmap.json`
