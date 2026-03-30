---
doc_id: bkc.2026-summer-solstice-review
doc_kind: research
status: active
depends_on:
  - bkc.sprint-1-retro
  - bkc.technique-ledger
source_docs:
  - "ic.2026-summer-solstice-research"
---

# Summer Solstice 2026 Seasonal Review

**Cycle:** Summer Solstice 2026 (first seasonal intelligence cycle)
**Date:** 2026-03-30
**Sprint 1 closed at:** `27c23daa` (retrieval), `63bda13f` (providers)
**Eval baseline:** Default v5 vs Planner v7 frozen pair (52 questions, gpt-4.1 canonical judge)
**Research packet:** `ic.2026-summer-solstice-research`

---

## Sprint 1 Summary

Sprint 1 (B5–B9c + P1/P2) delivered:
- **CR 0.18 → 0.4071** (+126% cumulative, +6.2% planner over default)
- **Eval:** 20 → 52 golden QA, 8-category taxonomy, 6 automated gates, gpt-4.1 canonical judge
- **Architecture:** Monolithic chat_endpoint → 3-layer router + 4 typed executors + provider abstraction
- **Key finding:** Text-search-first with multi-query expansion beat LLM-generated SQL/Cypher (the original synthesis' unanimous #1 recommendation)
- **Classifier accuracy:** 96.2% (GPT-4o with tuned contrastive prompt)
- **Provider bakeoff:** OpenAI wins 6/8 vs Anthropic; stay on OpenAI default

**Open drags:** governance_policy -3.4% (accepted after 3 tuning rounds), roadmap_status lowest CR at 0.281.

---

## Candidate Comparison

### Rubric (1-5 each)

| Dimension | What It Measures |
|-----------|-----------------|
| Expected quality gain | How much will this improve CR/AR/F on the eval set? |
| Implementation feasibility | How much effort to build, test, and deploy? |
| Maintenance burden | Ongoing cost of keeping it running and tuned? |
| Fit with current scale | Does this make sense at ~2,500 entities / ~3,600 chunks? |
| Eval readiness | Can we measure the impact with current eval infrastructure? |

### Scores

| Candidate | Quality | Feasibility | Maintenance | Scale Fit | Eval Ready | Total | Rank |
|-----------|---------|-------------|-------------|-----------|------------|-------|------|
| **B9.5 CRAG gate** | 3 | 5 | 5 | 5 | 5 | **23** | **1** |
| **golden-qa-100** | 1 | 5 | 5 | 5 | 5 | **21** | **2** |
| Query decomposition | 3 | 3 | 3 | 4 | 3 | **16** | **3** |
| HippoRAG 2 (`work.b2-graphrag-v1`) | 4 | 2 | 2 | 2 | 3 | **13** | **4** |
| RAPTOR (`work.b11-raptor-tree`) | 2 | 3 | 3 | 3 | 2 | **13** | **5** |

### Detailed Assessment

#### B9.5 CRAG Gate — Score: 23/25

**Quality (3):** Expected +3-5% CR by eliminating false-positive answers where the retriever returns irrelevant context but GPT-4o-mini generates a plausible-sounding response. The CRAG pattern (Yan et al., ICLR 2025) demonstrates clear value; the BKC-specific gain depends on how many of the 36 failing questions are retrieval-quality failures vs context-assembly failures.

**Feasibility (5):** Uses existing signals already computed in the pipeline: BM25 rank scores, FlashRank reranker confidence, entity match counts, embedding similarity scores. Implementation slots between reranking output and context assembly in `plan_executor.py`. No new models, no new dependencies. Estimated: 1-2 weeks.

**Maintenance (5):** Thresholds need calibration against the eval set, but the signals are deterministic and stable. No model drift, no retraining. Cost: zero (no API calls).

**Scale fit (5):** Works identically at any corpus size. Confidence gating is scale-independent.

**Eval readiness (5):** Measurable with existing 52-question eval set. Every signal can be logged in `plan_trace` telemetry. Pre/post comparison straightforward.

#### golden-qa-100 (Eval Expansion) — Score: 21/25

**Quality (1):** No direct CR impact — this is infrastructure. But enables confident statistical comparisons for all future techniques.

**Feasibility (5):** Writing 48 questions following the existing labeling rubric and taxonomy. Mechanical work, no architecture changes.

**Maintenance (5):** Questions are static once written. No ongoing cost.

**Scale fit (5):** Eval infrastructure scales independently of corpus.

**Eval readiness (5):** Is itself eval infrastructure.

#### Query Decomposition — Score: 16/25

**Quality (3):** RT-RAG shows +7% F1 on multi-hop benchmarks, but BKC's relationship_path CR is 0.5826 and improving. The gain depends on whether remaining failures are decomposition-gap failures or retrieval-quality failures — not yet diagnosed.

**Feasibility (3):** Requires a decomposition step in the planner, sub-query tracking, result merging, and error propagation handling. Medium complexity. 2-3 weeks.

**Maintenance (3):** Decomposition quality depends on LLM capability. Model upgrades may shift behavior. Sub-query chains create debugging complexity.

**Scale fit (4):** Works at any scale. Multi-hop queries exist in BKC's domain (relationship tracing across entities).

**Eval readiness (3):** Current eval set has no dedicated multi-hop category. Would need new questions to measure impact — circular dependency with golden-qa-100.

#### HippoRAG 2 (`work.b2-graphrag-v1`) — Score: 13/25

**Quality (4):** Published +7% F1 on associative QA benchmarks. The technique is well-validated.

**Feasibility (2):** Requires dual-node knowledge graph (passage + phrase nodes), PPR implementation, LLM-based triple extraction for indexing. Substantial architecture change. 3-4 weeks.

**Maintenance (2):** Knowledge graph must be maintained as entities are added. Triple extraction introduces LLM cost at ingest time. PPR parameters need tuning.

**Scale fit (2):** Designed for larger graphs. At ~2,500 entities, PPR's signal-to-noise ratio may be too low. The original paper tested on 50K+ documents. Revisit trigger (5,000 entities) is not met.

**Eval readiness (3):** Would need multi-hop/associative questions to measure the specific improvement. Current eval has some relationship_path questions but no associative reasoning category.

#### RAPTOR (`work.b11-raptor-tree`) — Score: 13/25

**Quality (2):** Best for broad thematic queries. BKC's current query distribution is entity-focused and relationship-focused. No evidence of thematic query demand.

**Feasibility (3):** Cluster → summarize → re-embed pipeline is well-documented. ~600-1,000 summary nodes. One-time cost ~$0.50-2.00.

**Maintenance (3):** Tree must be rebuilt when corpus changes significantly. Summary quality depends on LLM.

**Scale fit (3):** Works at current scale but the benefit (thematic queries) has no documented demand.

**Eval readiness (2):** No thematic category in eval taxonomy. No questions targeting broad-thematic retrieval. Would need eval expansion first.

---

## Decision

### Sprint 2 Candidate: **B9.5 CRAG Gate**

CRAG gate is the clear winner by rubric score (23/25) and satisfies the default decision bias (prefer cheap confidence + eval work before larger architecture changes). Evidence is mixed on the magnitude of quality gain, but the implementation risk is minimal, the maintenance burden is near-zero, and the technique enables runtime quality monitoring — a capability that all future techniques will benefit from.

**Scope:** Implement cheap confidence signals (reranker score threshold, entity match count, BM25 score distribution) as a gate between reranking and context assembly. Three actions: Confident (proceed to LLM generation), Low-confidence (expand query and retry with deeper retrieval), Very-low-confidence (abstain with explanation). Calibrate thresholds using the 52-question eval set. Log all signals in plan_trace telemetry.

**Roadmap item:** `work.b9.5-crag-gate` (planned, P1, 30-90d)

### Default Follow-on: **golden-qa-100**

Can run in parallel with CRAG gate implementation. Expanding from 52 to 100 questions fills thin categories (roadmap_status: 5, commitment_claim: 5) and creates the evaluation substrate needed for confident technique comparison at the Autumn Equinox gate.

### Deferred Candidates

| Candidate | Status | Revisit Trigger | Revisit Gate |
|-----------|--------|-----------------|--------------|
| Query decomposition | **Deferred** | Multi-hop eval questions consistently fail due to decomposition gaps (not retrieval quality). Requires golden-qa-100 to diagnose. | Autumn Equinox 2026 |
| HippoRAG 2 (`work.b2-graphrag-v1`) | **Deferred** | Entity count > 5,000 AND multi-hop associative queries are a documented pain point. | Winter Solstice 2026 earliest |
| RAPTOR (`work.b11-raptor-tree`) | **Deferred** | Thematic/broad query demand evidenced in production logs or user feedback. | Winter Solstice 2026 earliest |

---

## Phase 4 Readiness Check (Federated Retrieval)

| Question | Status | Evidence |
|----------|--------|----------|
| Do we have real cross-node query demand? | **No** | No user queries observed requiring knowledge from multiple nodes. `cross_node_provenance` taxonomy class exists but zero questions in eval set target it. |
| Do at least 2 nodes have meaningfully distinct corpora? | **Partial** | Octo has ~2,500 entities (Salish Sea wiki + docs). FR has ~50 entities (Boulder boundaries). GV has minimal corpus. Corpora are distinct but FR/GV are too thin to be useful retrieval targets. |
| Do we have a stable evidence bundle contract? | **Yes** | `EvidenceBundle` Pydantic model in `api/schemas/query_plan.py` is stable and used by all 4 live executors. Includes `source_type`, `confidence`, `metadata`. |
| Do we have capability/profile records worth routing on? | **No** | `peer_query` stub exists but `PolicyScope.eligible_peers` is not implemented. No `PeerCapabilityRecord` entities in any node's graph. |

**Phase 4 readiness: 1/4 (Yes on evidence bundle only). Not a candidate this cycle.** Phase 4 advances to active consideration when ≥3 questions are answered "yes" — likely requires FR or GV corpus growth and real cross-node demand.

---

## Cycle Provenance

This is the first seasonal intelligence cycle. It validates the learning loop defined in `ic.project-vision`:

- **Continuous sensing:** Eval baselines, technique ledger triggers, provider bakeoff results, production state
- **Deep research:** 3-model frontier sweep with browsing, synthesized into `ic.2026-summer-solstice-research`
- **Seasonal decision:** Rubric-scored candidate comparison producing one Sprint 2 candidate + one follow-on
- **Eval baseline snapshot:** Sprint 1 frozen pair (`-ab-default-v5-2026-03-27-215618.json`, `-ab-planner-v7-2026-03-29-145721.json`) reused as this cycle's official snapshot

Cross-project linkage is documentary: this review references `ic.2026-summer-solstice-research` in `source_docs` frontmatter. This is not carried into the graph by current tooling — it records provenance for human readers and future graph ingestion.
