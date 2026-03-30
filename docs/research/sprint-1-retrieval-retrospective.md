---
doc_id: bkc.sprint-1-retro
doc_kind: research
status: active
depends_on:
  - bkc.rag-synthesis
  - bkc.federated-memory-arch
---

# Sprint 1 Retrieval Retrospective

**Date:** 2026-03-30
**Scope:** B5 through B9c + P1/P2 (eval pipeline, hybrid retrieval, reranking, contextual retrieval, entity enrichment, multi-query expansion, QueryPlan IR, classifier repair, eval contract, category-specific tuning, provider abstraction, provider bakeoff)
**Duration:** 2026-03-22 to 2026-03-30 (9 days of active work)
**Starting point:** Monolithic `/chat` endpoint with pgvector-only retrieval, no eval harness, no query classification

---

## Quantitative Trajectory

| Milestone | CR | Passing | Eval Set | Classifier | Key Commit | Date |
|-----------|------|---------|----------|------------|------------|------|
| Pre-sprint baseline | 0.18 | 1/20 | 20 | N/A | — | 2026-03-23 |
| B6 Hybrid BM25+RRF | — | — | 20 | N/A | migration 073 | 2026-03-23 |
| B7 FlashRank reranking | — | — | 20 | N/A | — | 2026-03-23 |
| B8 Contextual retrieval | 0.28 | — | 20 | N/A | migration 077 | 2026-03-24 |
| B8 + corpus filtering | 0.36 | — | 20 | N/A | — | 2026-03-24 |
| B8a Entity enrichment | 0.38+ | 4/20 | 20 | N/A | — | 2026-03-24 |
| B8a full + B8b multi-query | 0.443 | 6/20 | 20 | N/A | `db23de2c` | 2026-03-26 |
| B5.5 Eval expansion | — | — | 52 | N/A | `a433d652` | 2026-03-26 |
| B9a Planner (early A/B, n=8) | +14.8% | 4/8 | 52 | 78.6% (gpt-4o-mini) | `d1088817` | 2026-03-26 |
| B9a Phase 5 (full A/B) | — | — | 52 | 65.4% | — | 2026-03-27 |
| B9a Phase 5b classifier repair | — | — | 52 | 96.2% (gpt-4o) | `22f02520` | 2026-03-27 |
| B9a Phase 5c eval contract | 0.379 (FAIL) | — | 52 | 96.2% | — | 2026-03-27 |
| B9b.1 commitment_claim fix | +4.0% | — | 52 | 96.2% | `be81f813` | 2026-03-28 |
| B9c relationship_path fix | 0.4071 (PASS) | — | 52 | 96.2% | `27c23daa` | 2026-03-29 |
| P1 Provider abstraction | — | — | 52 | 96.2% | `63bda13f` | 2026-03-29 |
| Planner live on salishsee.life | 0.4071 | — | 52 | 96.2% | — | 2026-03-30 |

### Summary metrics

- **Context Relevancy (CR):** 0.18 --> 0.4071 (+126% end-to-end; Phase 1 +146%, Phase 2 +6.2% over default)
- **Passing questions:** 1/20 --> 6/20 (Phase 1 baseline; Phase 2 used expanded 52-question set)
- **Classifier accuracy:** N/A --> 65.4% --> 96.2%
- **Eval coverage:** 20 --> 52 golden QA questions across 8 taxonomy categories
- **Architecture:** Monolithic 300-line chat_endpoint --> 4 typed retrieval executors + 3-layer router (PolicyScope, classifier, plan assembly)

### Canonical A/B result (v7 planner vs frozen v5 default, gpt-4.1 judge, 52/52 both paths)

| Gate | Result | Value |
|------|--------|-------|
| CR delta | PASS | 0.3835 --> 0.4071 (+6.2%) |
| In-domain AR | PASS | 0.9441 --> 0.9439 (-0.02%) |
| OOD abstention | PASS | 100% (6/6) |
| Faithfulness | PASS | 0.984 --> 0.9888 (+0.5%) |
| Classifier accuracy | PASS | 96.2% (50/52) |
| Errors | PASS | 0, 0 |

Per-category CR deltas: relationship_path +4.7%, commitment_claim +7.0%, entity_definition +5.9%, governance_policy -3.4% (accepted drag).

---

## What Worked

### 1. Eval-first development (B5, B5.5)

Every retrieval change was gated by the eval contract. When STRUCTURED_SQL and RELATIONSHIP_TRAVERSE looked sound in theory, the eval caught that they degraded results in practice. The eval contract itself evolved: 20 golden QA pairs (B5, 2026-03-23) --> 52 questions across 8 taxonomy categories (B5.5, 2026-03-26) --> canonical/informational verdict distinction, in-domain AR gate, OOD abstention gate, configurable judge model, resume integrity (Phase 5c, 2026-03-27). Final eval cost: ~$4.20 per full A/B run with gpt-4.1 judge.

### 2. Hybrid BM25+RRF (B6)

Two retrieval signals (pgvector semantic + PostgreSQL tsvector BM25) fused with reciprocal rank fusion. Migration 073 added `tsvector GENERATED ALWAYS` + GIN index on `koi_memory_chunks`. Top-40 vector + top-40 BM25, FULL OUTER JOIN, top 20 candidates. BM25-only fallback on embedding dimension mismatch. Consistently outperformed either signal alone.

### 3. Contextual retrieval (B8)

3,605 chunks enriched with 1-2 sentence context snippets via GPT-4o-mini (selected by direct bakeoff over other models). Migration 077 updated tsvector to index context+text. CR +56% (0.18 --> 0.28). This was the single highest-impact individual change. 1,869 code chunks were skipped during backfill.

### 4. Entity enrichment (B8a)

2,524 entities re-described and re-embedded with context-rich text (combines `metadata.context` + `description`). ~$1.70 OpenAI cost. CR +15%. The original synthesis estimated 92% of Concepts were name-only embeddings; enrichment gave them retrievable substance.

### 5. Source-aware corpus filtering

Excluding 1,869 .py/.ts/.go code entity chunks from the default `/chat` retrieval pool via `content.entity_name IS NOT NULL` filter. `include_code` parameter preserves developer mode access. CR +29% (0.28 --> 0.36). Combined with B8: +100% (0.18 --> 0.36). A reminder that corpus quality beats algorithmic sophistication.

### 6. Text-search-first routing

Across commitment_claim (B9b.1), relationship_path (B9c), and governance (B9d series), text search with multi_query expansion beat structured/graph retrieval. The pattern: `entity_lookup(3) --> text_search(multi_query, top_k=8)`. STRUCTURED_SQL and RELATIONSHIP_TRAVERSE both introduced over-retrieval noise that degraded answer quality. This was the sprint's most counterintuitive finding -- the original synthesis unanimously ranked "LLM-driven agentic retrieval" (SQL/Cypher generation) as the #1 priority upgrade.

### 7. Provider abstraction early (P1)

Decoupling LLM providers into three independent surfaces (classifier, chat answer, query expansion) via `api/chat_provider.py` makes bakeoffs, model swaps, and cost optimization trivial. The P2 bakeoff (8 frozen prompt packets, OpenAI vs Anthropic) was a direct consequence -- it would have required major refactoring without the abstraction layer. 78 tests. Deployed at `63bda13f`.

### 8. Classifier as leverage point (B9a Phase 5b)

Upgrading from gpt-4o-mini to gpt-4o with a tuned contrastive prompt moved classifier accuracy from 65.4% to 96.2%. Key prompt changes: contrastive "What is X?" disambiguation (entity_definition vs governance_policy), hardened OOD boundary, confidence recalibration. 4-variant bakeoff on 18 regression cases. Zero regressions on the 34 previously correct questions. The classifier is the single highest-leverage component in the planner architecture -- every downstream retrieval plan depends on correct classification.

---

## What Didn't Work

### 1. STRUCTURED_SQL for commitment_claim

Template-driven SQL queries against `commitment_registry` were added as a retrieval op in B9a. When tested against commitment_claim questions in B9b.1, they introduced over-retrieval noise that degraded CR. Iterative tuning across 3 rounds confirmed: removing STRUCTURED_SQL and routing commitment_claim through text-search-first produced better results. STRUCTURED_SQL is retained only for `roadmap_status` where it queries structured roadmap data.

### 2. RELATIONSHIP_TRAVERSE for relationship_path

The N-hop recursive CTE on `entity_relationships` was the natural choice for "How does X relate to Y?" queries. B9c tested two approaches: (A) tightening budgets to `max_hops=1, max=10` -- failed with -9.0% CR; (B) removing RELATIONSHIP_TRAVERSE entirely and using text-search-first with multi_query -- passed with +4.7% CR. Even 1-hop traversal added noise. RELATIONSHIP_TRAVERSE is retained only in the `governance_policy` plan.

### 3. Governance sub-routing (B9d/B9d.1/B9d.2)

Three rounds of governance-specific planner tuning, all failed:

| Round | Approach | Result |
|-------|----------|--------|
| B9d | Text-search-first, remove RELATIONSHIP_TRAVERSE | -3.4% CR vs default |
| B9d.1 | Variant A: text+entity(3); Variant B: text-only | Both lost. Revealed governance is internally mixed (definition vs policy sub-intents) |
| B9d.2 | Within-category sub-routing (definition branch + policy branch) | Definition branch: +112% avg CR over v7 planner. Policy branch: lost to default in both variants (-10.6% to -15.3%). Net: -8.5% to -11.0% |

The core problem: governance is internally heterogeneous. "What is the meta-protocol?" (definition) and "What are the data sovereignty rules?" (policy) require fundamentally different retrieval, but the classifier groups them. The -3.4% governance drag is accepted because the overall planner still passes at +6.2% CR.

### 4. Anthropic as chat-answer provider (P2)

P2 bakeoff: 8 frozen prompt packets from Octo production, OpenAI vs Anthropic side-by-side. OpenAI won 6/8. Anthropic was better on dense commitment/mechanism walkthroughs (commitment_claim_1, commitment_claim_3) but over-answered on definitions and governance. Decision: stay on OpenAI default, no on-node Anthropic trial.

---

## What Was Deferred and Why

| Technique | Synthesis Priority | Why Deferred | When to Revisit |
|-----------|-------------------|--------------|-----------------|
| **HippoRAG 2 (B2)** | Phase 3 (Week 11-12) | Scale threshold not met (~2,700 entities at synthesis time; ~1,005 after MediaWiki import dedup). PPR adds complexity without clear benefit at this graph size. | When entity count exceeds ~5,000 and multi-hop queries are a demonstrated pain point |
| **RAPTOR (B11)** | Phase 3 (Week 12-13) | Lower priority than control plane. Hierarchical summaries help broad thematic queries, which are not the current user pain point. | When thematic/broad queries become a significant portion of traffic |
| **Federated retrieval (B12)** | Phase 4 (Week 15-20) | Architecture designed (QueryPlan IR has `peer_query` stub). Cross-node query execution requires PeerCapabilityRecords and federation trust tiers not yet built. | When federation trust model is implemented and at least 2 nodes have distinct, valuable corpora |
| **Agentic SQL/Cypher** | Synthesis #1 priority | The original synthesis' unanimous #1 recommendation. Text-search-first beat it empirically. Template-driven structured_sql kept only for roadmap_status. | If a new query category emerges where structured data retrieval demonstrably outperforms text search |
| **Query decomposition** | Phase 2 (Week 9-10) | The planner routes by taxonomy category but does not decompose complex queries into sub-queries. Multi-query expansion (B8b) covers "same question, different phrasings" but not "complex question --> sub-questions." | When eval identifies specific multi-hop questions that fail due to complexity rather than retrieval quality |
| **CRAG gate (B9.5)** | Next sprint | Cheap confidence signals (token probability, retrieval score threshold) before expensive LLM judge. Would reduce eval cost and enable runtime quality gating. | Sprint 2, before expanding to 100 questions |

---

## Key Lessons

1. **Corpus quality > algorithmic sophistication.** Source-aware filtering (+29% CR) and contextual retrieval (+56% CR) outperformed every routing or plan-assembly optimization. Clean the data before adding complexity.

2. **Simpler retrieval plans outperform richer ones when extra steps add noise.** STRUCTURED_SQL and RELATIONSHIP_TRAVERSE both degraded results despite being well-implemented. The retrieval executors are correct -- the problem is that additional context from structured/graph sources dilutes the signal from high-quality text search results.

3. **Some categories are internally heterogeneous.** Governance = definitions + policy. The classifier sees one category; the retrieval needs differ. Sub-routing showed this clearly (definition branch +112%, policy branch -15.3%) but there is no clean way to expose the split without a second classification pass.

4. **The classifier is the highest-leverage single component.** Moving from gpt-4o-mini (65.4%) to gpt-4o (96.2%) with prompt tuning unblocked the entire planner. Every downstream plan depends on correct classification. The cost difference (~$0.003/query) is negligible relative to the quality improvement.

5. **An eval contract makes every other decision evidence-based.** Without the eval pipeline, STRUCTURED_SQL and RELATIONSHIP_TRAVERSE would likely have shipped based on architectural intuition. The eval contract caught regressions that were invisible to manual testing. The contract itself required iteration (Phase 5c: in-domain AR split, OOD gate, canonical vs informational verdicts, judge model selection).

6. **The original research synthesis was directionally correct but empirically wrong on priority.** "LLM-driven agentic retrieval" was the unanimous #1 recommendation across Claude, Gemini, and ChatGPT. In practice, the foundation work (BM25, reranking, contextual retrieval, entity enrichment) delivered 146% CR improvement; the control plane added 6.2% on top. The synthesis correctly identified every technique that worked -- it just over-estimated the value of dynamic query generation relative to corpus and embedding quality.

---

## Sprint Timeline

| Date | Session | Work Items | Key Result |
|------|---------|------------|------------|
| 2026-03-22/23 | `943075b5` | B5 eval pipeline, B6 BM25+RRF, B7 FlashRank | Baseline: f=1.0, ar=0.92, cr=0.18. Deployed to Octo+FR. |
| 2026-03-24 | `d050d726` | B8 contextual retrieval, corpus filtering, B8a pilot | CR: 0.18 --> 0.28 --> 0.36 --> 0.38. Corpus: 52% wiki + 48% GitHub. |
| 2026-03-26 | `9ce028dc` | B8a full, B8b multi-query, Phase 1 closure | CR 0.443 (+146%). Vendor pin `db23de2c`. Federated Memory Architecture plan. |
| 2026-03-26 | `a7b46a36` | B9a design, B5.5 eval expansion | QueryPlan IR schema (13 models). Golden QA 20 --> 52. Commit `a433d652`. |
| 2026-03-26 | `f2ab6fd9` | B9a implementation (Phases 1-4) | 4 executors extracted. Classifier + planner + executor wired. Early A/B: +14.8%. |
| 2026-03-27 | `6455dcd3` | B9a Phase 5 full A/B | Classifier accuracy 65.4% blocks gate. |
| 2026-03-27 | `b2770b61` | B9a Phase 5b classifier repair | gpt-4o + tuned prompt: 96.2% accuracy. Deployed `22f02520`. |
| 2026-03-27 | `589e9091` | B9a Phase 5c eval contract | Canonical A/B: FAIL (-4.2% CR from stub executors). 12 unit tests. |
| 2026-03-28 | `f1ff8b58` | B9b.1 commitment_claim fix | Text-search-first. Canonical: PASS (+4.0% CR). Deployed `be81f813`. |
| 2026-03-29 | `f1ff8b58` | B9c relationship_path fix | Remove RELATIONSHIP_TRAVERSE. Canonical: PASS (+6.2% CR). Deployed `27c23daa`. |
| 2026-03-29 | — | B9d/B9d.1/B9d.2 governance tuning | Three rounds, all failed. Drag accepted (-3.4%). |
| 2026-03-29 | — | P1 provider abstraction | 3 independent providers. 78 tests. Deployed `63bda13f`. |
| 2026-03-30 | — | P2 provider bakeoff | OpenAI wins 6/8. Stay on OpenAI default. |
| 2026-03-30 | — | Planner enabled on live site | `planner: true` via commons-web BFF. Active on salishsee.life. |

---

## Open Questions for Sprint 2

1. **HippoRAG 2 at current scale?** The graph has ~1,005 entities after MediaWiki import. Is that enough for PPR to help multi-hop queries, or does it need to grow further?

2. **Query decomposition for remaining failures?** Would decomposing complex queries into sub-queries help the categories where text-search-first still underperforms (governance_policy in particular)?

3. **Research synthesis refresh cadence?** The original synthesis (2026-03-22) was based on ~2,700 entities and ~4,500 chunks. The corpus, architecture, and eval have all changed substantially. When should a second three-model synthesis run?

4. **Eval expansion to 100 questions?** The current 52-question set has thin coverage in some categories (roadmap_status: 5, commitment_claim: 5). Should the set expand to 100 before the next tuning sprint, or is 52 sufficient for gating?

5. **CRAG (Corrective RAG) as runtime quality gate?** Cheap confidence signals (retrieval score thresholds, token probability, embedding similarity floor) could enable per-query quality gating without an LLM judge. Worth implementing before Sprint 2 tuning begins?

6. **Governance category split?** B9d.2 proved that governance_definition and governance_policy need different retrieval. Should the taxonomy expand from 7 to 8 categories, or is the classifier already at the limit of useful granularity?

---

## Frozen Artifacts

- **Default baseline:** `tests/eval/results/-ab-default-v5-2026-03-27-215618.json`
- **Planner v7:** `tests/eval/results/-ab-planner-v7-2026-03-29-145721.json`
- **Golden QA:** `tests/eval/golden_qa.json` (52 questions)
- **Eval taxonomy:** `tests/eval/eval_taxonomy.md`
- **QueryPlan IR spec:** `docs/specs/b9a-query-plan-spec.md`
- **Research synthesis:** `BioregionalKnowledgeCommoning/docs/research/rag-techniques-synthesis.md`
- **Federated memory architecture:** `BioregionalKnowledgeCommoning/docs/foundations/federated-memory-architecture.md`
