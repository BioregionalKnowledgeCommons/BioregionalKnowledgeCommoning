---
doc_id: bkc.technique-ledger
doc_kind: operations
status: active
depends_on:
  - bkc.rag-synthesis
---

# Technique Ledger

Maps each recommendation from bkc.rag-synthesis to its actual outcome in the BKC/Octo production system. Updated at each seasonal gate's Revise phase.

## Tier 1 Techniques (Implement < 1 Week)

| # | Technique | Synthesis Recommendation | Implemented | Work Item | CR Delta | Verdict | Notes |
|---|-----------|------------------------|-------------|-----------|----------|---------|-------|
| 1 | Hybrid BM25+dense+RRF | Unanimous. 15-30% recall improvement. | Yes (B6) | `work.b6-hybrid-bm25-rrf` | Part of cumulative 0.18→0.443 | **Ship** | tsvector+GIN, top-40 each, FULL OUTER JOIN RRF. BM25-only fallback on dim mismatch. |
| 2 | Cross-encoder reranking | Unanimous. FlashRank with MiniLM-L-12. | Yes (B7) | `work.b7-cross-encoder-reranking` | Part of cumulative | **Ship** | ~50MB model, ~200ms for top-20→8. Lazy-loaded. Graceful degradation if flashrank not installed. |
| 3 | Contextual retrieval | Unanimous. 49-67% fewer retrieval failures. | Yes (B8) | `work.b8-contextual-retrieval` | +56% CR | **Ship** | 3,605 chunks enriched via GPT-4o-mini. ~$1.28 one-time. Migration 077 (tsvector indexes context+text). |
| 4 | Automated eval pipeline | Unanimous. Required gate before any advanced technique. | Yes (B5+B5.5) | `work.b5-eval-gates` | Enabled all other work | **Ship** | DeepEval runner, 52 golden QA (synthesis recommended 100+). 8-category taxonomy. gpt-4.1 canonical judge. |

## Tier 1 Techniques (Added During Sprint)

| # | Technique | Origin | Implemented | Work Item | CR Delta | Verdict | Notes |
|---|-----------|--------|-------------|-----------|----------|---------|-------|
| 5 | Entity enrichment | Synthesis Phase 1 Week 2. | Yes (B8a) | `work.b8a-entity-enrichment` | +15% CR | **Ship** | 2,524 entities re-described + re-embedded with context-rich text. ~$1.70 one-time. |
| 6 | Multi-query expansion | Synthesis Phase 1 Week 3. | Yes (B8b) | `work.b8b-multi-query-expansion` | +3.5% CR, +2.8s latency | **Ship (default off)** | LLM reformulations + cross-query RRF. Enabled per-category via decision matrix. |
| 7 | Source-aware corpus filtering | Discovered during B8. | Yes | — | +29% CR | **Ship** | Exclude 1,869 code entity chunks from /chat retrieval. `include_code` parameter for dev mode. |
| 8 | Provider abstraction | P1, not in original synthesis. | Yes (P1) | — | — | **Ship** | Per-surface LLM decoupling. Three independent providers (classifier, chat, expansion). |

## Tier 2 Techniques

| # | Technique | Synthesis Recommendation | Implemented | Work Item | CR Delta | Verdict | Notes |
|---|-----------|------------------------|-------------|-----------|----------|---------|-------|
| 5 | LLM-driven agentic retrieval (SQL/Cypher) | Unanimous #1 highest impact. Stages A-D. | QueryPlan control plane shipped (B9a). LLM SQL/Cypher generation tested and rejected. | `work.b9-agentic-sql-cypher` | Text-search-first beat it | **Deprecated** | STRUCTURED_SQL caused over-retrieval in commitment_claim (B9b.1). RELATIONSHIP_TRAVERSE noise in relationship_path (B9c). Template-driven structured_sql kept only for roadmap_status. |
| 6 | HippoRAG 2 (PPR) | Unanimous. +7% multi-hop, no degradation on simple QA. | No | `work.b2-graphrag-v1` | — | **Deferred** | Scale threshold not met (~2,700 entities). Revisit trigger: entity count > 5,000 or multi-hop eval questions consistently fail. |
| 7 | Query decomposition + iterative retrieval | All three reports recommend. | No | — | — | **Not started** | Sub-query decomposition for multi-hop. Would integrate with current planner's decision matrix. Revisit trigger: multi-hop eval category added. |
| 8 | CRAG confidence gate | Summer Solstice 2026 seasonal review selected as Sprint 2 candidate. | Telemetry-only (B9.5) | `work.b9.5-crag-gate` | Quality-neutral (-0.2% to +1.8% across runs) | **Telemetry shipped** | Cheap signals (reranker score, entity count, text count, spread) computed and logged to plan_trace. Full retry/abstention behavior disabled after 4 canonical eval runs showed quality-neutral results with +4s latency cost. FlashRank scores too compressed (0.05-0.10 range) for meaningful discrimination. Infrastructure value: signals logged for future analysis. Revisit trigger: richer retrieval diagnostics (raw BM25/vector scores) or a discriminative reranker. |

## Tier 3 Techniques

| # | Technique | Synthesis Recommendation | Implemented | Work Item | CR Delta | Verdict | Notes |
|---|-----------|------------------------|-------------|-----------|----------|---------|-------|
| 9 | RAPTOR (hierarchical summaries) | All three recommend as medium priority. | No | — | — | **Deferred** | Best for broad thematic queries ("What is the overall status of restoration?"). Revisit trigger: thematic query category added to eval. |
| 10 | LightRAG evaluation | Comparison baseline. | No | — | — | **Not started** | Entity profiling pattern already implemented via B8a. Dual-level retrieval pattern worth evaluating. |
| 11 | Federated retrieval | ChatGPT + Gemini emphasize. | Architecture only (QueryPlan IR, federated-memory-architecture.md) | — | — | **Design done** | Execution requires peer capability records and federation trust tiers. Revisit trigger: second node needs cross-node query answering. |

## Infrastructure Decisions

| Decision | Synthesis Recommendation | Outcome | Notes |
|----------|------------------------|---------|-------|
| Embedding model | Stay with text-embedding-3-small, evaluate after contextual retrieval. | **Switching to Ollama** | Ollama mxbai-embed-large on poly (37.27.48.12) via WireGuard. Eliminates ~30% of OpenAI API cost. Eval gate required (CR regression < 5%). |
| Vector DB | Stay with pgvector, add pgvectorscale at 100K+ vectors. | Stayed | ~7,500 vectors total. Well within pgvector HNSW capacity. |
| Graph DB | Keep Apache AGE for current scale. | Stayed | ~7K edges. AGE Cypher was not used for LLM-generated queries (text-search-first beat it). |
| LLM strategy | Multi-model: cheap for routing, capable for generation. | Yes | Classifier: GPT-4o. Chat: GPT-4o-mini. Expansion: GPT-4o-mini. Eval judge: gpt-4.1 (canonical), gpt-4.1-mini (dev). |
| Eval batch pricing | Not in original synthesis. | **Not started** | OpenAI batch API gives 50% discount on eval scoring. Requires eval runner changes: collect all /chat responses first, construct scoring prompts, submit as JSONL batch, parse results. Cuts gpt-4.1 canonical runs from ~$35-50 to ~$17-25. ROI: significant for gpt-4.1 gates, marginal for gpt-4.1-mini dev runs. Revisit trigger: next time a canonical gpt-4.1 gate run is needed. |
| GPU | Start without, add when reranking latency becomes bottleneck. | No GPU needed | FlashRank CPU reranking ~200ms. Not the bottleneck. |

## Revision History

| Date | Sprint | Changes |
|------|--------|---------|
| 2026-03-30 | Sprint 1 closure | Initial ledger created. All Tier 1-3 techniques mapped. |
| 2026-03-30 | Summer Solstice review | Revisit-trigger check: zero triggers met. Entity count ~2,500 (HippoRAG threshold 5,000 not met). No thematic demand (RAPTOR). No multi-hop category (query decomposition). No cross-node query demand (federated). All deferred techniques remain correctly deferred. |
| 2026-03-31 | Sprint 2 closure | B9.5 CRAG gate: implemented, evaluated (4 canonical runs), closed as telemetry-only. Quality-neutral (-0.2% to +1.8% CR across runs). Retry/abstention behavior disabled. Confidence signals logged to plan_trace for future analysis. FlashRank reranker scores too compressed for meaningful discrimination at current corpus scale. Next move: golden-qa-100 eval expansion. |
