# RAG Techniques Synthesis: Three-Model Research Report for Octo

**Date:** 2026-03-22
**Source reports:** Claude, Gemini Deep Research, ChatGPT (o3) — all run against the same research prompt
**Purpose:** Decision document for Octo's next retrieval architecture evolution

---

## How to Read This Document

Three frontier models independently evaluated 20+ RAG techniques against Octo's architecture. This synthesis extracts consensus, highlights disagreements, and produces a single prioritized roadmap. Where all three agree, we treat it as high-confidence. Where they diverge, we note the reasoning and make a call.

**Updated constraints (relaxed from original prompt):**
- Open to dedicated vector DB (Qdrant, Weaviate, Milvus, etc.)
- Open to dedicated graph DB (Neo4j, JanusGraph, etc.) or replacing Apache AGE
- Open to GPU (renting or adding to server)
- Open to alternative LLMs (Claude, Gemini, local models via Ollama)
- Open to alternative embeddings (Nomic, Jina, Voyage, Cohere, BGE-M3)
- Flexible budget — willing to invest where it demonstrably improves quality
- Open to multi-server architecture
- **Hard constraints remain:** Self-hostable, PostgreSQL as source of truth, no extended downtime

**Dual-scenario framing:** Following ChatGPT's most distinctive contribution, recommendations below are tagged **(A)** for current constraints (single VPS, no GPU, Postgres-only) and **(B)** for relaxed constraints (GPU, polyglot DBs, flexible budget, federation). Some techniques shift dramatically between scenarios — ColBERT goes from "skip" to "viable with Vespa," MemoRAG from "skip" to "medium" with GPU, Text-to-Query from "bounded templates" to "federation control plane." Where (A) and (B) diverge, both paths are shown.

**Existing federation infrastructure:** Octo already runs a federated network — KOI-net protocol with ECDSA-signed envelopes, domain event bridge (6 event types), edge-approval membrane governance, bidirectional peering between Octo, GV, CV, and FR nodes. Federation recommendations in this document are about *extending existing federation to the retrieval layer* (federated queries, evidence packets, cross-node discovery), not building federation from scratch.

---

## Executive Summary

### Universal consensus (all three reports agree)

All three models converge on the same core upgrades, in roughly the same priority order:

| Priority | Technique | Consensus Strength | Why |
|----------|-----------|-------------------|-----|
| 1 | **LLM-driven agentic retrieval** | **UNANIMOUS #1** | Transforms 4 fixed SQL templates into dynamic query generation. All three call this the single highest-leverage upgrade. |
| 2 | **Contextual Retrieval** (Anthropic) | **UNANIMOUS** | ~49-67% fewer retrieval failures. ~$1.28 one-time cost. Works with GPT-4o-mini. |
| 3 | **Hybrid BM25 + dense + RRF** | **UNANIMOUS** | Fixes the biggest recall gap. Native PostgreSQL tsvector for quick start, ParadeDB pg_search for upgrade. |
| 4 | **Cross-encoder reranking** | **UNANIMOUS** | FlashRank (CPU, ~4MB, 100ms) or GPU rerankers with relaxed constraints. 10-25% precision improvement. |
| 5 | **HippoRAG 2 (PPR)** | **UNANIMOUS** | Best graph-native retrieval for multi-hop. Doesn't degrade simple QA (unlike GraphRAG/LightRAG). Uses existing entity graph. |
| 6 | **Automated evaluation** (DeepEval + RAGAS) | **UNANIMOUS** | Gate for all future changes. Manual 10-question QA is insufficient. |
| 7 | **Query routing / Adaptive-RAG** | **Strong (3/3)** | Classify query complexity, route to appropriate strategy. Saves latency on simple queries, enables deep retrieval on complex ones. |

### Key disagreements between reports

| Topic | Claude | Gemini | ChatGPT | Resolution |
|-------|--------|--------|---------|------------|
| **LightRAG** | "Strong candidate but evaluate carefully" — comparison baseline alongside existing system | Top 5, native PG support, 4-6 day effort | "High applicability" for entity profiling + dual retrieval | **Evaluate as comparison baseline.** Don't replace the pipeline wholesale — cherry-pick the entity profiling and dual-level retrieval patterns. |
| **MemoRAG** | "DO NOT IMPLEMENT" — GPU hard blocker, steal clue-generation concept only | "Medium complexity, 3-5 days" — seems to understate GPU requirement | "Low applicability (A), Medium (B)" — correctly identifies GPU need | **Skip MemoRAG.** Implement HyDE-style query expansion (the useful insight) as a 10-line prompt wrapper. Gemini understated the GPU blocker. |
| **HyperGraphRAG** | "Consider for Phase 2" — bipartite pattern useful, don't adopt codebase | Top technique (9.4/10) — n-ary relationships, +55% fact recall | "Low (A), Medium-High (B)" — correctly flags extraction overhead | **Defer.** At ~2,769 entities, binary relations suffice. Extract the bipartite design pattern for future use if domain complexity demands n-ary facts. |
| **OGRAG2** | "DO NOT IMPLEMENT" — immature codebase (6 commits), no PG support | Not evaluated | "Medium (A), High (B)" — notes ontology mapping effort | **Skip.** Codebase too immature. Revisit if BKC ontology formalizes further. |
| **LazyGraphRAG** | Not specifically evaluated | Top technique (9.5/10) — dynamic community detection | Not specifically evaluated | **Strategic interest, but not at current scale.** Gemini scores this highest because it optimizes for extreme scale and rapid graph evolution. At ~2.7K entities, the overhead of dynamic Louvain clustering + LLM re-summarization isn't justified — the graph can be fully traversed in milliseconds. Revisit when graph exceeds 50K entities and incremental re-clustering becomes cheaper than full traversal. |
| **pgvectorscale** | Not evaluated | High priority (9.2/10) — billion-scale vector search | Not evaluated | **Not needed now.** Gemini's 9.2 score assumes Octo is scaling to millions/billions of vectors. At 4,500 chunks + 2,769 entities, pgvector HNSW is more than adequate with sub-millisecond queries. Install when corpus exceeds 100K vectors and HNSW memory footprint becomes a concern. |
| **Federation architecture** | Not addressed (prompt didn't emphasize) | Significant focus — MCP, A2A, RAGRoute | **Central theme** — QueryPlan IR, evidence packets, KOI+MCP integration, AD4M/Coasys bridge | **Strategic priority.** ChatGPT's QueryPlan IR concept is the most actionable federation-ready design. Build toward it incrementally. |
| **Infrastructure evolution** | "Stay with PostgreSQL" — existing stack validated | "Scale with pgvectorscale + MCP" | Dual roadmap: (A) Postgres-first now, (B) polyglot with dedicated engines at scale | **Follow ChatGPT's dual-track.** Postgres-first for current scale, abstract retrieval behind QueryPlan IR so future engine swaps are low-risk. |

---

## Consensus Technique Evaluations

### Tier 1: Implement Now (< 1 week each, transformative impact)

#### 1. Hybrid BM25 + Dense Retrieval with RRF

**Consensus:** All three reports rank this as a foundational upgrade. Fixes the biggest recall gap (ILIKE is not real keyword search).

**What:** Add real BM25 scoring via PostgreSQL `tsvector` + GIN index. Combine with pgvector cosine similarity via Reciprocal Rank Fusion (RRF, k=60).

**Quick-start (native PostgreSQL, zero dependencies):**
```sql
-- Add tsvector column
ALTER TABLE koi_memory_chunks ADD COLUMN tsv tsvector
  GENERATED ALWAYS AS (to_tsvector('english', content->>'text')) STORED;
CREATE INDEX idx_chunks_tsv ON koi_memory_chunks USING GIN(tsv);

-- Hybrid query with RRF
WITH vector_results AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> $query_vec) AS rank
    FROM koi_memory_chunks ORDER BY embedding <=> $query_vec LIMIT 40
),
bm25_results AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY ts_rank_cd(tsv, plainto_tsquery($query)) DESC) AS rank
    FROM koi_memory_chunks WHERE tsv @@ plainto_tsquery($query) LIMIT 40
)
SELECT COALESCE(v.id, b.id),
    COALESCE(1.0/(v.rank+60), 0) + COALESCE(1.0/(b.rank+60), 0) AS rrf_score
FROM vector_results v FULL OUTER JOIN bm25_results b ON v.id = b.id
ORDER BY rrf_score DESC LIMIT 10;
```

**Upgrade path:** ParadeDB `pg_search` for true BM25 with IDF weighting when quality becomes measurably better.

**Effort:** 0.5-2 days | **Impact:** 15-30% recall improvement

---

#### 2. Cross-Encoder Reranking

**Consensus:** Unanimous. CPU-viable since ModernBERT revolution.

**What:** After hybrid retrieval returns top-50 candidates, rerank with a cross-encoder to find the best 5-8 for the LLM.

**Recommended stack:**
- **Now (CPU):** FlashRank with MiniLM-L-12 — `pip install flashrank`, ~50MB, ~200ms for 50 docs, no PyTorch dependency
- **With GPU:** `gte-reranker-modernbert-base` (149M params, matches 1.2B-param quality) or Cohere Rerank API ($2/1K searches)

**Effort:** 0.5-1 day | **Impact:** 10-25% precision improvement

---

#### 3. Contextual Retrieval

**Consensus:** Unanimous. Highest ROI indexing upgrade.

**What:** Batch-process each chunk through GPT-4o-mini to generate a 1-2 sentence context snippet explaining the chunk's position in its source document. Prepend to chunk text before embedding.

**Results:** 35% fewer retrieval failures (embeddings alone), 49% with BM25, 67% with reranking.

**Cost:** ~$1.28 one-time for 4,500 chunks. Works with GPT-4o-mini (validated by multiple community implementations, not Claude-only).

**Implementation:** Batch process → re-embed → update BM25 index. Also add tsvector on the contextualized chunks for contextual BM25.

**CDTA tension:** Claude discovered Cross-Document Topic-Aligned Chunking (CDTA, Nov 2025) which reports 88% Hit@1 vs 63% for Contextual Retrieval. CDTA discovers global topics across the entire corpus and consolidates information per topic. The benchmarks are compelling, but Contextual Retrieval is preferred here because: (a) it's far simpler — no corpus-wide clustering or topic discovery, just per-chunk prompting; (b) it's well-validated across multiple community implementations; (c) it composes naturally with BM25 and reranking; (d) CDTA's benchmarks are on general corpora, not domain-specific knowledge graphs. **Recommendation:** Implement Contextual Retrieval now, evaluate CDTA at the next major re-indexing cycle — particularly if thematic queries remain weak after RAPTOR.

**Effort:** 1-2 days | **Impact:** 49-67% fewer retrieval failures

---

#### 4. Automated Evaluation Pipeline

**Consensus:** Unanimous. Required gate before any agentic or advanced technique.

**What:** Replace manual 10-question QA with automated regression testing.

**Stack:**
- **DeepEval** for running evaluations (pytest-style, 7+ RAG metrics, Apache 2.0, works with GPT-4o-mini)
- **RAGAS** for generating synthetic test sets (knowledge-graph-based diverse query generation)
- Generate 100-200 Q&A pairs (50 synthetic via RAGAS, 50+ human-validated)
- Set thresholds: faithfulness >= 0.7, context relevancy >= 0.6
- Run on every pipeline change

**Framework disagreements:**
- **ARES:** ChatGPT recommends alongside RAGAS for context relevance/faithfulness scoring via synthetic data + lightweight judges. Claude says skip (requires GPU for fine-tuning judges, needs 150+ human annotations). **Resolution:** Start with DeepEval + RAGAS (zero GPU). Add ARES later **(B)** if you have GPU and want a second evaluation signal.
- **TruLens:** ChatGPT recommends for instrumenting tool calls and agentic workflows. Claude says skip (Snowflake-centric direction). **Resolution:** Use DeepEval's `@observe` decorator for component-level tracing initially. Evaluate TruLens if agentic pipeline debugging proves difficult — its strength is tracing multi-step tool call chains.

**Cost:** ~$0.10-0.50 per 100-sample evaluation run with GPT-4o-mini.

**Effort:** 1-2 days | **Impact:** Enables data-driven iteration on everything else

---

### Tier 2: Next Sprint (1-2 weeks, substantial capability gain)

#### 5. LLM-Driven Agentic Retrieval (The Big One)

**Consensus:** All three reports call this the highest-impact upgrade. This is what transforms Octo from 4 fixed query templates to an intelligent retrieval planner.

**What:** Replace hardcoded SQL templates with an LLM agent that dynamically decides what retrieval strategy to use, generates queries, evaluates results, and iterates.

**The spectrum (implement incrementally as Stages A-D, mapped to roadmap Phases 1-4):**

**Stage A — Schema-Aware SQL Generation → roadmap Phase 2, Week 4-5:**
- For structured queries: LLM generates SQL with schema-aware prompting (DDL + 20 validated examples)
- Parse → execute → on error, feed error back → regenerate (max 3 retries)
- Fallback to existing 4 templates on failure
- Expected first-attempt accuracy: 70-85%, rising to 85-95% with retry

**Stage B — Text-to-Cypher via Apache AGE → roadmap Phase 2, Week 5-7:**
- Add Cypher generation using LangChain's AGE integration
- Build Cypher schema prompt from `ag_catalog` metadata
- 10-15 validated Cypher examples as few-shot

**Stage C — Multi-Tool Orchestration → roadmap Phase 2, Week 7-9:**
- LangGraph/PydanticAI orchestrator with tool nodes:
  - `semantic_entity_search(query)` — pgvector cosine on entities
  - `keyword_search(query)` — BM25 on chunks
  - `graph_traverse(entity_id, hops)` — AGE Cypher
  - `dynamic_sql_query(description)` — LLM-generated SQL
  - `document_chunk_search(query)` — pgvector on chunks
- Sufficiency evaluation: "Do you have enough? If not, what's missing?"
- Re-retrieve once if insufficient

**Stage D — Self-Improving + Federation-Ready → roadmap Phase 4, Week 15-16:**
- Cache successful NL→SQL/Cypher mappings as few-shot examples
- QueryPlan IR (typed JSON AST) for federation readiness (ChatGPT's design)
- MCP tool contracts so remote nodes can participate in query plans

**Safety (all reports agree):**
- Never execute raw LLM-generated SQL directly — validate, allowlist ops, parameterize
- Budget guards (k limits, hop depth, timeouts)
- Deterministic fallback to existing pipeline on any failure
- Plan auditing + tracing (store QueryPlan, inputs/outputs, evidence selection)

**Framework decisions:**

| Framework | What | Strengths | Weaknesses | Verdict |
|-----------|------|-----------|------------|---------|
| **Vanna AI** | Text-to-SQL with RAG (20K stars, MIT, PG native) | Purpose-built for NL→SQL. Trains on your schema + validated examples. Auto-improves. | SQL-only — no Cypher, no graph traversal, no multi-tool orchestration. | **Use for Stage A** (SQL generation). Best NL→SQL tool available. |
| **LangGraph** | State machine orchestration (LangChain ecosystem) | Multi-tool, conditional routing, persistence, debugging. Official AGE Cypher integration. | Heavier dependency. LangChain ecosystem churn. | **Use for Stage C+** (multi-tool orchestration, sufficiency loops). |
| **PydanticAI** | Type-safe agent framework (Pydantic ecosystem) | Clean typed interfaces, lighter than LangGraph, good for structured tool calling. | Smaller ecosystem, less graph-specific tooling. | **Viable alternative to LangGraph.** Gemini recommends it. Consider if LangChain's weight becomes a burden. Both work for multi-step reasoning. |
| **LangChain GraphCypherQAChain** | Text-to-Cypher for AGE | Official Apache AGE integration. Schema-aware prompting. | Tightly coupled to LangChain. | **Use for Stage B** (Cypher generation). |

**Recommendation:** Vanna AI (Stage A) → LangChain AGE integration (Stage B) → LangGraph or PydanticAI (Stage C orchestration). The orchestration framework choice (LangGraph vs PydanticAI) can be deferred until Stage B is running — evaluate both against the codebase style at that point.

**Effort:** 2-8 weeks (phased) | **Impact:** 40-60% on complex queries, unlimited query patterns

---

#### 6. HippoRAG 2 (Personalized PageRank)

**Consensus:** Unanimous. Best graph-native retrieval technique for Octo's existing data.

**What:** PPR-based associative memory over the entity graph. Propagates relevance from query-matched entities through the graph to find related context.

**Why it's special:** Only technique that improves multi-hop queries *without degrading simple QA* — GraphRAG, LightRAG, and RAPTOR all lose 5-10 F1 on simple queries.

**Fit:** Octo's existing AGE graph (2,769 entities, 7,015 edges) is essentially what HippoRAG 2 builds from scratch. PPR can be implemented via iterative SQL/Cypher on AGE. Open-source implementation (OSU-NLP-Group/HippoRAG, 3.7K stars) supports GPT-4o-mini.

**Benchmarks:** MuSiQue F1 44.8→51.9, 2Wiki Recall@5 76.5→90.4%. Uses only 9M tokens for indexing (vs 115M for GraphRAG).

**Effort:** 2-3 weeks | **Impact:** +7% on multi-hop, adaptive neighborhood sizing replaces fixed 2-hop CTE

---

#### 7. Query Decomposition + Iterative Retrieval

**Consensus:** All three reports recommend this, with varying ambition levels.

**What:** For complex queries, decompose into 2-4 sub-queries with retrieval method annotations. Execute independently, synthesize results. If initial retrieval is insufficient, reformulate and re-retrieve (max 1-2 iterations).

**Patterns discovered:**
- **CoRAG** (Microsoft, NeurIPS 2025): Chain-of-retrieval — query → sub-query → retrieve → extract sub-answer → reformulate based on accumulated context → repeat. >10 EM points on multi-hop QA.
- **Auto-RAG** (2024): Autonomous iterative retrieval with adaptive iteration count based on difficulty.
- **Speculative RAG** (ICLR 2025): Parallel drafts from different evidence subsets, verified by stronger model. +12.97% accuracy, -51% latency.

**Implementation:** Start with a simple self-evaluation loop ("Do you have enough information? If not, what's missing?") before building full iterative retrieval.

**Effort:** 1-2 weeks | **Impact:** Addresses multi-hop gap and "no query reformulation"

---

### Tier 3: Strategic (1-4 weeks, architectural evolution)

#### 8. RAPTOR (Hierarchical Summarization)

**Consensus:** All three recommend as medium priority. Adds multi-scale retrieval (leaf chunks + theme summaries).

**What:** Build a tree over chunks: cluster → summarize → re-embed → re-cluster → re-summarize (2-3 levels). Add summary nodes to the same pgvector table as leaf chunks. At query time, search across all levels simultaneously.

**For 4,500 chunks:** Expect ~600-1,000 summary nodes. One-time cost: ~$0.50-2.00 with GPT-4o-mini. Zero additional query-time latency.

**Best for:** Thematic/broad queries ("What is the overall status of restoration in the Salish Sea?").

**Weakness:** No incremental update strategy — batch periodic rebuilds (acceptable at current scale).

**Effort:** 3-7 days | **Impact:** High for synthesis queries, moderate for entity-specific lookups

---

#### 9. LightRAG — Evaluate as Comparison Baseline

**Consensus:** All three see value, but disagree on adoption strategy. Claude recommends comparison baseline, Gemini recommends adoption, ChatGPT recommends cherry-picking.

**What:** Production-grade graph-augmented RAG with native PostgreSQL support (PGVectorStorage + PGGraphStorage for AGE). 29,300 stars, daily active development. Dual-level retrieval: local (entity-focused) + global (relationship-focused).

**Resolution:** Deploy alongside existing system, benchmark both. Cherry-pick the most valuable patterns:
- **Entity profiling:** Generate rich text profiles for each entity (name + description + source excerpts + related entities). This directly addresses Gap #7 (92% of Concepts are name-only embeddings).
- **Dual-level retrieval mode:** Low-level entity search + high-level thematic search as separate retrieval paths.

**Caveats:** AGE integration has reported stability issues under concurrent writes (GitHub issues #2122, #2255). Creates its own graph schema — migration required.

**Effort:** 4-6 days for evaluation | **Impact:** Informs whether to adopt or cherry-pick

---

#### 10. Extending Federation to Retrieval

**Consensus:** ChatGPT and Gemini both emphasize this; Claude didn't address it (prompt didn't focus on federation). This becomes important with relaxed constraints.

**What already exists:** Octo's KOI-net federation is production — signed envelopes, edge-approval gating, domain event bridge, bidirectional peering across 4 nodes (Octo, FR, GV, CV). What's missing is *federated retrieval*: the ability for a query on one node to discover and incorporate evidence from peer nodes, with provenance.

**ChatGPT's philosophical insight:** "Federation changes the definition of 'grounding' from 'cite local sources' to 'return provenance across nodes.'" This aligns directly with KOI's signed-envelope design and BKC's claims engine — the retrieval layer should return typed evidence packets with cross-node provenance chains, not just text chunks. Grounding becomes a network property, not a local one.

**Key design from ChatGPT (most actionable):**

**QueryPlan IR (Typed JSON AST):**
```json
{
  "version": "0.1",
  "user_intent": { "task": "qa", "constraints": { "bioregion": "salish-sea", "privacy_tier": "public" } },
  "entities": [{ "mention": "eelgrass", "candidates": ["orn:koi..."], "resolution_confidence": 0.82 }],
  "plan": [
    { "op": "bm25_search", "target": "chunks", "query": "...", "k": 50 },
    { "op": "dense_search", "target": "chunks", "k": 50 },
    { "op": "rank_fuse", "method": "rrf", "k": 60 },
    { "op": "rerank", "model": "cross_encoder", "k": 20 },
    { "op": "graph_expand", "method": "ppr", "seeds_from": "entities" },
    { "op": "federated_search", "peers": ["nodeA"], "subplan": [...] },
    { "op": "assemble_context", "max_tokens": 6000, "include_provenance": true }
  ],
  "safety": { "max_latency_ms": 8000, "max_iterations": 2, "no_raw_query_execution": true }
}
```

**Evidence Packets with Provenance:**
Retrieval returns typed evidence (not just text) with source artifacts, confidence scores, and cross-node signatures — aligned with KOI's provenance chain design.

**Implementation path:** Build the QueryPlan IR as the internal representation for the agentic retrieval system (Technique #5). It works locally first, then naturally extends to federated queries via MCP tool contracts.

**Effort:** Integrated with agentic Stage D / roadmap Phase 4 | **Impact:** Future-proofs for federation

---

## Infrastructure Decisions Under Relaxed Constraints

### Embedding Model

| Model | Dims | MTEB Avg | Cost/M tokens | Context | Notes |
|-------|------|----------|---------------|---------|-------|
| text-embedding-3-small (current) | 1536 (or 768 via Matryoshka) | 62.26 | $0.02 | 8K | Good value. Matryoshka at 768 dims halves index size with ~1-2% quality loss — worth testing. |
| text-embedding-3-large | 3072 (or 1536 via Matryoshka) | 64.60 | $0.13 | 8K | Easy switch, same API. Matryoshka to 1536 dims keeps current index size at higher quality. |
| Voyage-3-large | 1024 | 66.80 | $0.06 | 32K | Best API cost:quality ratio. Long context enables late chunking. |
| Nomic-embed-text-v1.5 | 768 | ~63 | Self-host (Apache-2.0) | 8K | Fully open-source. Matryoshka support. Good for self-hosted stack. |
| BGE-M3 | 1024 | ~65 | Self-host | 8K | Dense + sparse + multi-vector in one model. Could replace separate BM25 index entirely. **(B)** requires GPU for self-hosting. |
| Jina-embeddings-v3 | flexible (Matryoshka) | ~65 | $0.02 | 8K | Multilingual + long-context + Matryoshka dimensionality reduction. Enables late chunking experiments. |

**Decision:** Stay with text-embedding-3-small until Contextual Retrieval is implemented and evaluated. Then benchmark Voyage-3-large and BGE-M3. Re-embedding costs are trivial (~$0.05-0.09), so model swaps are cheap. **Quick experiment:** Try Matryoshka truncation to 768 dims on text-embedding-3-small — halves storage with minimal quality loss, useful data point before committing to a model swap. BGE-M3 is the most interesting **(B)** option because it produces dense + sparse vectors from one model, potentially replacing the separate BM25 index entirely.

### Vector DB

| Engine | License | GPU | Hybrid Search | Best For |
|--------|---------|-----|---------------|----------|
| pgvector (current) | PostgreSQL | No | Via tsvector + RRF | Current scale (< 100K vectors) |
| pgvectorscale | Apache-2.0 | No | StreamingDiskANN + SBQ | Scaling pgvector to millions |
| Qdrant | Apache-2.0 | Yes (v1.13+) | Sparse + dense Query API | Mid-scale, good filtering |
| Weaviate | BSD-3 | NVIDIA cuVS | Native BM25 + vector hybrid | Hybrid-first workloads |
| Milvus | Apache-2.0 | Explicit GPU indexes | Dense + sparse hybrid | Large-scale distributed |

**Decision:** Stay with pgvector now. At current scale (4,500 chunks + 2,769 entities), pgvector HNSW is more than adequate. Add pgvectorscale when approaching 100K+ vectors. Consider Qdrant or Weaviate only if you need features pgvector can't provide (multi-tenancy, GPU ANN, native hybrid scoring). The key insight from ChatGPT: abstract retrieval behind a QueryPlan IR so engine swaps become configuration changes, not rewrites.

### Graph DB

| Engine | License | Query Language | Fit |
|--------|---------|---------------|-----|
| Apache AGE (current) | Apache-2.0 | Cypher (in PostgreSQL) | Good for current scale, keeps everything in one DB |
| Neo4j Community | GPLv3 | Cypher + vector indexes | Better tooling ecosystem, LangChain integration |
| JanusGraph | Apache-2.0 | Gremlin/TinkerPop | Massively scalable, multi-backend |

**Decision:** Keep Apache AGE for now. At ~7K edges, both AGE and Neo4j execute in single-digit milliseconds. AGE's advantage is zero-ops (same PostgreSQL instance). Critical optimization: create explicit BTREE indexes on `id`, `start_id`, `end_id` for all edge labels, and GIN indexes on properties. The LLM-driven agentic retrieval system should generate Cypher for AGE directly via LangChain's AGE integration. Migrate to Neo4j only if AGE's Cypher limitations (concurrent write stability, expression restrictions) become blocking.

### LLM Strategy

| Use Case | Current | Recommended |
|----------|---------|-------------|
| Chat generation | GPT-4o-mini | GPT-4o-mini (adequate), or Claude Sonnet 4.6 for quality |
| Query routing/classification | N/A | GPT-4o-mini (cheapest, fast) |
| SQL/Cypher generation | N/A | GPT-4o or GPT-4.1-mini ($0.40/M) for accuracy |
| Contextual Retrieval indexing | N/A | GPT-4o-mini (batch, one-time) |
| Evaluation judges | N/A | GPT-4o-mini via DeepEval |

**Decision:** Multi-model strategy. Use GPT-4o-mini for routing and generation (cost-effective). Use a stronger model (GPT-4o or Claude Sonnet) for SQL/Cypher generation where accuracy matters. Budget impact is minimal — query planning adds ~$0.001-0.005 per query.

*Note: Model names and pricing reflect March 2026 offerings. This landscape shifts quarterly — evaluate current models at implementation time. The architectural pattern (cheap model for routing, capable model for generation/query planning) is stable regardless of specific model versions.*

### GPU Decision

**When to add GPU:**
- Reranking becomes the latency bottleneck and you want stronger rerankers than CPU FlashRank
- You adopt long-context embedding strategies (late chunking) needing fast embedding throughput
- You want local model inference (Ollama for routing, embedding, or small task-specific models)
- Vector DB with GPU indexing (Milvus, Qdrant v1.13+)

**Not needed for:** BM25, RRF fusion, Contextual Retrieval indexing (API-based), evaluation pipeline, agentic retrieval orchestration.

**Decision:** Start without GPU. Add when reranking latency or embedding throughput becomes the measured bottleneck after Tier 1 is deployed.

---

## Techniques All Three Reports Agree to Skip

| Technique | Why Skip | Source |
|-----------|----------|--------|
| **MemoRAG** | **(A)** Hard skip — requires 16-24 GiB GPU VRAM for 7B memory model, no API alternative. **(B)** Becomes medium-viable with GPU, but still heavy for unclear benefit vs simpler multi-query + iterative retrieval patterns. Steal the "clue generation" concept as HyDE-style query expansion regardless. | Claude, ChatGPT |
| **Full Self-RAG** | Requires fine-tuned local LLMs with reflection tokens. Better implemented as CRAG-style document grading via standard API calls. | All three |
| **ColBERT / late interaction** | **(A)** Skip — pgvector doesn't support multi-vector embeddings; cross-encoder reranking gives 80% of the benefit at 20% complexity. **(B)** Becomes viable with Vespa (which explicitly supports ColBERT-style retrieval) or a dedicated ColBERT serving stack. Still competes with "hybrid + rerank + contextual embeddings" which is simpler. Revisit under (B) only if reranking quality plateaus. | Claude, ChatGPT |
| **OGRAG2 codebase** | 6 commits, no PostgreSQL support, no API server. Research artifact, not a framework. | Claude |
| **Full-rebuild GraphRAG** (Microsoft) | Map-reduce community summaries too expensive for evolving graph. HippoRAG 2 preferred. LazyGraphRAG viable at extreme scale only. | All three |
| **Multi-agent frameworks** (CrewAI, AutoGen) | Overkill for single-database architecture. Single LangGraph state machine covers all needs. | Claude |
| **Raw LLM-generated SQL execution** | Safety risk. Use QueryPlan IR with allowlisted ops, or validated template mapping. | ChatGPT, Claude |
| **ArangoDB / SurrealDB** | BSL 1.1 license (not OSI open source during restriction window). Conflicts with commons/OSS values. | ChatGPT |

---

## Unified Implementation Roadmap

### Phase 1: Foundation (Week 1-3)

*Note: ChatGPT's roadmap is more conservative than Claude's here, and more realistic. This phase is sequenced so each change can be measured independently.*

| Week | Action | Addresses |
|------|--------|-----------|
| 1 | Add BM25 via tsvector + GIN index on chunks table. Implement RRF fusion (hybrid BM25 + pgvector in single SQL query). | No BM25 gap, no ranking fusion |
| 1 | Install FlashRank, add reranking step after hybrid retrieval (top 50 → top 8). | No reranking gap |
| 1-2 | Set up DeepEval + RAGAS evaluation pipeline. Generate 100+ Q&A pairs (50 synthetic, 50+ human-validated). Establish baseline metrics. | Manual QA only |
| 2 | Entity enrichment: batch-generate profiles for all 2,769 entities. Re-embed. Two levels: *basic* (2-3 sentence description, ~$0.50-1.00) or *rich* LightRAG-style (name + description + source excerpts + related entities, ~$1-3). Start basic, upgrade to rich during LightRAG evaluation in Phase 3. | 92% sparse entity descriptions |
| 2-3 | Run Contextual Retrieval batch: GPT-4o-mini context snippets for all 4,500 chunks. Re-embed. Update BM25 index. | No contextual embedding |
| 3 | Add multi-query expansion: generate 2-3 query reformulations per user question, retrieve for each, fuse with RRF. Distinct from decomposition — this is "same question, different phrasings" for recall. | No query reformulation |
| 3 | Add query complexity router (GPT-4o-mini classifier → fast/standard/deep paths) + self-evaluation loop ("Do you have enough information?"). | Fixed retrieval limits, no adaptive retrieval |

**Why entity enrichment moved here:** It's a one-time batch job (~$0.50-1.00) with the same pattern as Contextual Retrieval (LLM generates text → re-embed). Since 92% of Concepts are name-only embeddings, enriching entities directly improves every retrieval path — semantic entity search, graph traversal context, and LLM prompt quality. Same effort tier as Contextual Retrieval, same cost bracket.

**Verification:** Run full eval suite after each change. Measure delta vs baseline.

**Expected cumulative impact:** 50-70% improvement in retrieval quality across query types.

### Phase 2: Intelligent Retrieval (Week 4-10)

*This is the most ambitious phase — Claude's source report estimates 8 weeks for full agentic retrieval. The timeline below is optimistic; treat week ranges as targets, not commitments. Each stage is independently deployable behind a feature flag.*

| Week | Action (Agentic Stage) | Addresses |
|------|--------|-----------|
| 4-5 | **Stage A:** Build schema-aware SQL generation via Vanna AI (DDL prompt + 20 validated examples + retry loop). Fallback to existing templates. | Primitive retrieval planner |
| 5-7 | **Stage B:** Add Text-to-Cypher via LangChain AGE integration. Cypher schema prompt + 15 examples. | Unused Apache AGE |
| 7-9 | **Stage C:** Build multi-tool orchestrator (semantic + keyword + graph + SQL tools). Choose LangGraph or PydanticAI based on Stage B experience. Sufficiency check + re-retrieve. | No agentic retrieval |
| 9-10 | Implement query decomposition for multi-hop (split into sub-queries with method annotations). Integrates with Stage C orchestrator. | No multi-hop beyond 2-hop |

**Verification:** Compare agentic pipeline vs baseline on 50+ multi-hop queries. Measure first-attempt accuracy, retry rate, fallback rate.

### Phase 3: Graph Intelligence (Week 11-14)

| Week | Action | Addresses |
|------|--------|-----------|
| 11-12 | Implement HippoRAG 2 PPR over existing AGE graph. Add passage nodes linking chunks to entities. | Multi-hop beyond 2-hop |
| 12-13 | Build RAPTOR tree (cluster → summarize → re-embed, 2-3 levels). Add summary nodes to pgvector table. | Thematic/broad queries |
| 13-14 | Evaluate LightRAG as comparison baseline alongside enhanced pipeline (entity enrichment already complete from Phase 1). Focus evaluation on LightRAG's full extraction pipeline, dual-level retrieval, and entity deduplication vs the enhanced existing pipeline. Cherry-pick patterns that outperform. | Architecture decision |

**Verification:** Run eval suite on multi-hop and thematic query subsets. Measure delta.

### Phase 4: Federated Retrieval + Scale (Week 15-20) — Scenario (B)

*This phase extends Octo's existing KOI-net federation (signed envelopes, event bridge, edge-approval gating) into the retrieval layer.*

| Week | Action (Agentic Stage) | Addresses |
|------|--------|-----------|
| 15-16 | **Stage D:** Implement QueryPlan IR as internal representation for agentic retrieval. Cache successful query plans. | Federation-ready control plane |
| 16-17 | Build evidence packet format with provenance chains. Integrate with existing KOI signed envelopes and claims engine. | Cross-node grounding ("cite provenance across nodes, not just local sources") |
| 17-18 | Expose retrieval tools as MCP contracts (search, resolve, neighborhood, federated_search) — extending existing personal-koi-mcp tool contracts. | Inter-node retrieval via existing MCP infrastructure |
| 18-20 | **(B) only:** If scale demands, deploy dedicated retrieval engine (Qdrant/Weaviate) as dual-write alongside PostgreSQL. Abstract behind QueryPlan IR so swap is a config change. | Future scaling |

---

## The Target Pipeline Architecture

```
User Query
    |
[Query Router] — GPT-4o-mini classifies complexity → fast/standard/deep
    |
[Multi-Query Expansion] — generate 2-3 reformulations for recall (standard/deep paths only)
    |
[Query Decomposition] — complex queries → sub-queries with method annotations (deep path only)
    |
[Parallel Hybrid Retrieval] — run for each query variant, fuse across all
    |-- pgvector semantic search (contextualized embeddings)
    |-- BM25 keyword search (tsvector on contextualized chunks)
    |-- AGE Cypher traversal (template or LLM-generated)
    |-- Dynamic SQL (LLM-generated, schema-aware, with retry)
    |-- [Future] Federated search (MCP calls to peer nodes)
    |
[RRF Fusion] — combine results from all retrieval paths
    |
[Cross-Encoder Reranking] — FlashRank/ModernBERT, top 50 → top 8
    |
[Sufficiency Check] — "Enough to answer?" If no → reformulate → re-retrieve (max 1 retry)
    |
[HippoRAG 2 PPR] — expand from top entities through graph for associative context
    |
[Context Assembly] — chunks + entities + graph context + provenance metadata
    |                  Budget: max 16K chars, truncate lowest-scoring first
    |
[LLM Generation] — GPT-4o-mini with structured output, citations, confidence scores
    |
[Answer + Evidence Packet]

Fast path  (<1.5s): simple entity lookups, single retrieval strategy
Standard   (<3s):   moderate queries, parallel retrieval + RRF + reranking
Deep path  (<8s):   complex multi-hop, full agentic loop with iterative retrieval
```

---

## Discovered Techniques Worth Tracking

These appeared in one or more reports but aren't in the immediate roadmap. Track for future evaluation:

| Technique | Source | What | When to Revisit |
|-----------|--------|------|-----------------|
| **CoRAG** (Microsoft, NeurIPS 2025) | Claude | Chain-of-retrieval: iterative sub-query planning | When agentic pipeline is stable |
| **MiniRAG** (2025) | ChatGPT | Lightweight heterogeneous graph RAG, topology-enhanced retrieval | If LightRAG evaluation disappoints |
| **Speculative RAG** (ICLR 2025) | ChatGPT | Parallel drafts from different evidence, verified by stronger model | When multi-model strategy is mature |
| **Auto-RAG** (2024) | ChatGPT | Autonomous iterative retrieval with adaptive iteration count | When evaluation harness proves agentic loops are safe |
| **CDTA** (Nov 2025) | Claude | Cross-Document Topic-Aligned Chunking. 88% Hit@1 vs 63% for Contextual Retrieval | At next major re-indexing cycle |
| **Late Chunking** (Jina, 2024) | Claude, Gemini, ChatGPT | Full-document embedding before chunking. Requires long-context model. | When switching to Jina v3 or similar |
| **LazyGraphRAG** | Gemini | Dynamic Louvain for incremental community detection. 0.1% cost of full GraphRAG. | When graph exceeds 50K entities |
| **pgvectorscale + SBQ** | Gemini | StreamingDiskANN for billion-scale vector search in PostgreSQL | When vectors exceed 100K |
| **BGE-M3** embedding model | ChatGPT | Dense + sparse + multi-vector from one model | When evaluating embedding swap after Contextual Retrieval |
| **AD4M/Coasys bridge** | ChatGPT | Agent-centric federation substrate — see detailed section below | When federated retrieval (Phase 4) is running |

### AD4M/Coasys as Federation Substrate

ChatGPT gave this significant treatment, and given BKC's values alignment with the Coasys ecosystem, it deserves more than a tracking table entry.

**What it is:** AD4M (Agent-Centric Distributed Application Meta-ontology) provides agent-centric identity, Perspectives/Expressions/Languages, a GraphQL API, and Prolog-based "Social DNA" for defining social interaction rules. Coasys builds on AD4M to enable collaborative sense-making with LLM-generated Prolog rules for complex queries. AD4M uses SurrealDB internally for fast graph queries.

**Why it matters for BKC:** The commons-oriented design philosophy aligns with BKC's governance model. Social DNA enables rule-based governance queries ("which stewards have authority over this bioregion's data?") that complement KOI's signal-based federation. LLM-generated Prolog rules could enable a form of "text-to-query" for governance and social layer queries that SQL/Cypher can't express naturally.

**How it fits:** Treat KOI as the federation protocol layer (data exchange, provenance, signed envelopes) and AD4M/Coasys as an optional agent-centric semantic overlay for nodes that want social coordination features. The interop path: both KOI MCP tools and AD4M MCP tools can be targets in the QueryPlan IR — the orchestrator routes to either depending on peer type.

**Applicability:** **(A)** Low — adds significant infrastructure for unclear retrieval benefit. **(B)** Medium — becomes viable when multiple community nodes want social governance features beyond what KOI provides. Not a retrieval technique per se, but a federation substrate that could enable novel query types.

**Decision:** Track actively. Explore concrete interop when federated retrieval (Phase 4) is running and there's a real use case from a community node wanting AD4M-style social features.

---

## Cost Estimates

| Item | One-Time | Per-Query | Notes |
|------|----------|-----------|-------|
| Contextual Retrieval indexing | ~$1.28 | — | 4,500 chunks through GPT-4o-mini |
| RAPTOR tree building | ~$0.50-2.00 | — | Summarization + re-embedding |
| Entity enrichment (Phase 1) | ~$0.50-1.00 | — | 2,769 entity profiles — moved to Phase 1 alongside Contextual Retrieval |
| Re-embedding (any model swap) | ~$0.05-0.09 | — | Trivial at current scale |
| Evaluation pipeline | — | ~$0.005/run | 100-sample run with GPT-4o-mini |
| Query routing | — | ~$0.001 | Single GPT-4o-mini classification |
| SQL/Cypher generation | — | ~$0.003-0.01 | Per query, with retry budget |
| FlashRank reranking | — | $0 | Local CPU, no API cost |
| Total indexing investment | ~$3-5 | — | All one-time upgrades |
| Per-query overhead vs current | — | ~$0.005-0.015 | Routing + generation + eval |

---

## Sources

This synthesis draws from three independent research reports:

1. **Claude** — "RAG architecture decisions for Octo's next evolution" (360 lines, implementation-focused, strongest on specific tool recommendations and "what NOT to implement")
2. **Gemini Deep Research** — "State-of-the-Art RAG Techniques for Knowledge Graph Retrieval" (194 lines, scale and federation-focused, strongest on future-proofing and dynamic graph evolution)
3. **ChatGPT (o3)** — "Updating Octo's RAG Decision Document for Relaxed Constraints and Federation" (853 lines, most comprehensive, strongest on dual-scenario analysis, federation architecture, DB comparison tables, and QueryPlan IR design)

Each report evaluated 15-25 techniques against the same research prompt describing Octo's PostgreSQL + pgvector + Apache AGE architecture with ~2,769 entities, ~7,015 edges, and ~4,500 document chunks.
