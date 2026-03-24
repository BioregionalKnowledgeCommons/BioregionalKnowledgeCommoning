# RAG architecture decisions for Octo's next evolution

**Octo's single highest-leverage upgrade is replacing its 4-template SQL retrieval planner with an LLM-driven agentic query system, followed immediately by contextual retrieval and hybrid BM25+vector search with reranking.** These three changes together address gaps #1–#4 and #5 from the priority list and can be implemented incrementally over 2–4 weeks. The research evaluated 7 seed techniques, discovered 12+ novel approaches from 2024–2026 literature, and checked 8 previously assessed techniques for updates — all against Octo's specific PostgreSQL+pgvector+Apache AGE architecture on a single VPS with no GPU.

The core finding is that Octo's architecture is already well-positioned. PostgreSQL+pgvector+AGE is validated by Microsoft's own GraphRAG Solution Accelerator, LightRAG's native support, and multiple production deployments. The bottleneck isn't infrastructure — it's retrieval intelligence. Every high-impact technique identified works within the existing stack.

---

## Executive summary: seven techniques ranked by impact × feasibility

The evaluation weighted impact on answer quality (40%), implementation feasibility (25%), maintenance burden (20%), and composability (15%). Each technique maps directly to one or more of Octo's known gaps.

| Rank | Technique | Score | Gaps addressed | Effort | Expected impact |
|------|-----------|-------|----------------|--------|----------------|
| 1 | **LLM-driven agentic retrieval** (LangGraph + Text-to-SQL/Cypher) | 92 | #1, #4, #6, #8 | 2–4 weeks (phased) | 40–60% on complex queries |
| 2 | **Contextual Retrieval** (Anthropic pattern w/ GPT-4o-mini) | 90 | #5, #3 | 1–2 days | 49–67% fewer retrieval failures |
| 3 | **Hybrid BM25+dense with RRF** (ParadeDB or tsvector) | 87 | #3 | 1–2 days | 15–30% recall improvement |
| 4 | **Cross-encoder reranking on CPU** (FlashRank or ModernBERT) | 85 | #2 | 0.5–1 day | 10–25% precision improvement |
| 5 | **Query router / Adaptive-RAG** (GPT-4o-mini classifier) | 80 | #6, #8 | 0.5–1 day | 30–40% latency reduction + quality routing |
| 6 | **HippoRAG 2** (PPR over existing AGE graph) | 75 | #6, #7 | 2–3 weeks | 7%+ on multi-hop without sacrificing simple QA |
| 7 | **DeepEval + RAGAS evaluation pipeline** | 72 | All (measurement) | 1–2 days | Enables data-driven iteration |

These seven compose into a coherent pipeline: Router → Decompose → Retrieve (hybrid BM25+vector+graph) → Rerank → Evaluate sufficiency → Re-retrieve if needed → Generate. Each component is independently deployable.

---

## Seed technique evaluations

### 1. OGRAG2 (Microsoft) — ontology-grounded hypergraph retrieval

**What it is.** OG-RAG anchors document retrieval in formal domain ontologies expressed as JSON-LD, constructing hyperedges that cluster factual knowledge grounded to ontology concepts. Published at **EMNLP 2025** (Sharma et al.). The GitHub repo (`microsoft/ograg2`) has only **6 commits** and 80 stars — this is a research artifact, not a framework.

**How it works.** Documents are mapped to ontology concepts via LLM, generating knowledge triples grouped into hyperedges. At query time, an optimization algorithm retrieves the minimal set of hyperedges that covers the query's conceptual scope. Embeddings use text-embedding-ada-002; generation uses GPT-4-turbo.

**Applicability: LOW.** Storage is entirely file-based (JSON + custom vector indices). No PostgreSQL integration exists. Octo's 23 entity types could theoretically serve as a lightweight ontology, but formalizing them into JSON-LD and rewriting the entire storage layer is prohibitive.

**Implementation complexity: VERY HIGH.** Effectively a ground-up reimplementation. The codebase lacks an API server, production features, or Docker deployment. The claimed benchmarks (+55% fact recall, +40% correctness) come from domains with rich formal ontologies — benefits diminish sharply without one.

**Verdict: ❌ DO NOT IMPLEMENT.** The ontology bottleneck and immature codebase make this impractical. The useful insight — grouping related facts into clusters for retrieval — can be approximated by enriching Octo's entity descriptions (Gap #7) without adopting OG-RAG's full pipeline.

---

### 2. HyperGraphRAG (LHRLAB) — n-ary relation retrieval

**What it is.** Extends GraphRAG by replacing binary knowledge graphs with hypergraphs where each hyperedge connects *n* entities, capturing complex multi-entity facts. Published at **NeurIPS 2025** (Luo et al.). GitHub has **344 stars**, 52 commits.

**How it works.** GPT-4o-mini extracts n-ary relations as hyperedges. The hypergraph is stored as a bipartite graph (entities ↔ hyperedges) with dual vector databases for entity and hyperedge embeddings. Retrieval uses bidirectional expansion: find matching entities → expand to connected hyperedges → gather complete relational facts. Already uses **text-embedding-3-small** (1536-dim) and GPT-4o-mini — matching Octo's stack.

**Applicability: MEDIUM.** The bipartite pattern maps naturally to Apache AGE (entities and hyperedges as separate node labels, binary edges between them). However, Octo's existing ~7,015 binary edges would need re-extraction as n-ary relations — a significant re-indexing effort. The codebase uses NanoVectorDB, not PostgreSQL.

**Benchmarks are compelling**: +10 F1 points over LightRAG on average across Medical, Agriculture, CS, and Legal domains. But at Octo's scale (~2,769 entities), the complexity advantage of hypergraphs over standard graphs may be marginal.

**Verdict: ⚠️ CONSIDER FOR PHASE 2.** Extract the bipartite hypergraph algorithm as a design pattern. Implement after LightRAG or HippoRAG 2 stabilizes. Do not adopt the codebase directly.

---

### 3. LightRAG (HKUDS) — the closest drop-in upgrade

**What it is.** A production-grade graph-augmented RAG framework with **29,300 stars**, 6,559 commits, and active daily development. Published at **EMNLP 2025**. Uses dual-level retrieval: local (entity-focused) and global (relationship-focused), with an optional "mix" mode combining graph + chunk retrieval. MIT license.

**How it works.** Documents are chunked, entities and relationships are extracted via LLM, and a knowledge graph is built with deduplication and entity merging. Each entity and relation gets a "profile" (name + description + source excerpts) that is embedded for vector search. At query time, the LLM extracts keywords, and dual-level retrieval finds relevant entities (local) and relationships (global) via vector similarity, expanding to connected subgraphs.

**Applicability: EXCELLENT.** LightRAG has **native PostgreSQL support** using the exact Octo stack: `PGVectorStorage` for embeddings, `PGGraphStorage` for Apache AGE, `PGKVStorage` for key-value data. It supports HNSW indexes, text-embedding-3-small, and GPT-4o-mini. It includes a REST API server and web UI.

**Implementation complexity: LOW-MEDIUM.** Install via `pip install lightrag-hku` or Docker. Configure with environment variables pointing to existing PostgreSQL and OpenAI API. The main work is re-indexing existing documents through LightRAG's extraction pipeline.

**Caveats worth noting**: AGE integration has reported stability issues under concurrent writes (GitHub issues #2122, #2255). The framework creates its own graph schema, requiring a migration strategy for existing Octo data. LightRAG's binary-relation-only graph is less expressive than HyperGraphRAG's n-ary relations.

**Verdict: ✅ STRONG CANDIDATE, but evaluate carefully.** LightRAG could replace Octo's entire retrieval pipeline with minimal infrastructure changes. However, this is a "replace" strategy, not an "enhance" strategy. The agentic retrieval approach (Technique #7) may provide better ROI by augmenting the existing pipeline rather than replacing it. **Recommended as a comparison baseline**: deploy alongside the existing system, benchmark both, then decide.

---

### 4. MemoRAG — global memory via local model compression

**What it is.** A dual-system RAG framework using a **7B-parameter LLM** to compress an entire knowledge base into a KV-cache "memory," then generating retrieval clues from that memory to guide precise evidence retrieval. Published at **WWW 2025** (Qian et al.). 2,200 stars.

**How it works.** A lightweight LLM (memorag-qwen2-7b-inst) reads the full context and compresses it into memory tokens via beacon compression (up to 400K tokens). At query time, the memory model generates draft answers and surrogate queries, which are used to retrieve precise chunks from a FAISS index. A heavier LLM generates the final answer.

**Applicability: ❌ NONE.** **The 7B local model requirement is an absolute blocker.** MemoRAG requires **16–24 GiB GPU VRAM** for the memory model. There is no API-based alternative — the KV compression mechanism fundamentally requires local model weight access. The system uses FAISS, not PostgreSQL. Even "Lite mode" requires a T4 GPU.

**The useful insight to extract**: generating "retrieval clues" (draft answers) to improve search queries. This can be implemented as a simple HyDE-style query expansion using GPT-4o-mini in ~10 lines of code — no MemoRAG needed.

**Verdict: ❌ DO NOT IMPLEMENT.** GPU requirement is a hard blocker. Steal the clue-generation concept as a lightweight query expansion prompt.

---

### 5. RAPTOR — recursive abstractive tree indexing

**What it is.** Builds a tree structure over document chunks: leaf nodes are original chunks, intermediate nodes are LLM-generated summaries of semantically similar chunk clusters, and higher nodes are summaries of summaries. From Stanford, published at **ICLR 2024**. At query time, "collapsed tree retrieval" searches across all levels simultaneously.

**How it works.** Chunks are embedded → clustered via Gaussian Mixture Models (soft clustering, allowing overlap) → summarized by LLM → re-embedded → re-clustered → re-summarized, building 2–4 tree levels. The collapsed tree approach simply adds all summary nodes to the same pgvector table as leaf chunks, so retrieval is a standard cosine similarity query across all levels.

**Applicability: HIGH.** Fully compatible with PostgreSQL+pgvector. Summary nodes are just additional rows in the vector table. Tree structure can be stored in AGE. For ~4,500 chunks, expect ~600–1,000 summary nodes across 2–3 levels. **One-time indexing cost: ~$0.50–2.00** with GPT-4o-mini. Zero additional query-time latency.

**Key weakness: update handling.** Adding new documents requires re-clustering affected areas and potentially re-summarizing up the tree. RAPTOR's paper does not address incremental updates. Practical approach: batch periodic rebuilds (acceptable at Octo's scale).

**Verdict: ✅ MEDIUM PRIORITY.** Implement as a low-effort enhancement after the higher-priority items. Adds ~1,000 summary vectors to the existing table. Most valuable for thematic/broad queries ("What is the overall status of X across the region?"). Less impactful for entity-specific lookups.

---

### 6. ColBERT / late interaction models — token-level similarity

**What it is.** ColBERT represents documents and queries as matrices of per-token 128-dimensional embeddings, scoring via MaxSim (sum of maximum cosine similarities between each query token and all document tokens). ColBERTv2 adds residual compression reducing storage 6–10×. RAGatouille provides a Python wrapper.

**Applicability: LOW for Octo's constraints.** pgvector does not natively support multi-vector embeddings. A workaround exists via VectorChord (PostgreSQL extension storing `vector[]` arrays), but this adds significant complexity. ColBERT's official README states "a GPU is required for training and indexing." CPU inference is feasible but slow (~100–300ms per query encoding). At **4,500 chunks, the retrieval problem is easy enough** that pgvector HNSW with text-embedding-3-small already achieves high recall.

**The better alternative**: cross-encoder reranking gives **80% of ColBERT's quality benefit at 20% of the complexity**. FlashRank's MiniLM-L-12 achieves 95–98% of full cross-encoder accuracy in ~200ms on CPU for 50 documents, with no PyTorch dependency.

**Verdict: ❌ LOW PRIORITY.** Skip in favor of cross-encoder reranking. Revisit only if the corpus grows beyond 50K chunks where retrieval-stage quality becomes the bottleneck.

---

### 7. LLM-driven hybrid retrieval — the highest-impact upgrade

**What it is.** Replaces Octo's 4 hardcoded SQL templates with an LLM-driven agent that dynamically generates SQL, Cypher, and vector queries based on query analysis. This directly addresses **Gap #1** (primitive retrieval planner) and enables queries that currently cannot be answered at all.

**How it works.** A ReAct-style agent receives the user query and orchestrates retrieval through tools:

- **`semantic_entity_search(query)`** — pgvector cosine similarity on entity embeddings
- **`keyword_search(query)`** — PostgreSQL full-text search
- **`graph_traverse(entity_id, hops)`** — template-based AGE Cypher
- **`dynamic_cypher_query(description)`** — LLM-generated Cypher via AGE
- **`dynamic_sql_query(description)`** — LLM-generated PostgreSQL SQL
- **`document_chunk_search(query)`** — pgvector on chunks table

The agent decides which tools to invoke, evaluates results, and re-queries if insufficient. Schema-aware prompting provides DDL definitions, entity types, relationship types, and few-shot examples. Error-retry loops catch invalid SQL/Cypher (parse → execute → on error, feed error back to LLM → regenerate, max 3 retries). A fallback cascade ensures the existing pipeline handles failures.

**The incremental implementation path is critical** — this is not all-or-nothing:

- **Phase 1 (Week 1–2):** Replace hardcoded SQL templates with LLM-generated SQL. Build schema prompt with DDL + 20 validated examples. Add parse→execute→retry loop. Fallback to existing templates on failure.
- **Phase 2 (Week 3–4):** Add Text-to-Cypher via LangChain's Apache AGE integration. Build Cypher schema prompt from `ag_catalog` metadata. Add 10–15 validated Cypher examples.
- **Phase 3 (Week 5–6):** Build query router classifying queries into 6 categories (direct entity, relationship, attribute, aggregation, exploratory, multi-hop). Route to appropriate tool combination.
- **Phase 4 (Week 7–8):** Enable multi-tool query decomposition. Cache successful NL→SQL/Cypher mappings. Self-improving loop adds validated queries to few-shot examples.

**Key frameworks to leverage**: Vanna AI (20K stars, MIT, purpose-built for text-to-SQL with RAG, supports PostgreSQL natively), LangChain's `GraphCypherQAChain` (official Apache AGE integration), and LangGraph for state machine orchestration.

**GPT-4o-mini works for routing and simple queries** but consider GPT-4o or GPT-4.1-mini ($0.40/M input) for SQL/Cypher generation where accuracy matters. **Expected first-attempt SQL accuracy: 70–85%**, rising to 85–95% with error-retry, and 100% with fallback to existing pipeline.

**Verdict: ✅✅ HIGHEST PRIORITY.** This transforms Octo from 4 fixed query patterns to unlimited dynamic query generation. Unique advantage: SQL + Cypher + vector search all run in the same PostgreSQL instance, enabling hybrid queries no other tool supports natively. Start Phase 1 immediately.

---

## Discovered techniques from broad search

### Contextual Retrieval — the best bang-for-buck upgrade

Anthropic's technique (September 2024) prepends a short LLM-generated context snippet to each chunk before embedding, explaining the chunk's position within its source document. This means "the city" in chunk 3 carries awareness that "Berlin" was established in chunk 1. The contextualized chunks are then both embedded (for vector search) and indexed for BM25.

**Results are dramatic**: contextual embeddings alone reduce retrieval failures by **35%**. Adding contextual BM25 reaches **49%**. Adding reranking hits **67%**. Multiple community implementations confirm these results work with GPT-4o-mini, not just Claude. A Towards Data Science implementation applied it to Norwegian court rulings with GPT-4o-mini + Pinecone successfully.

**For Octo's 4,500 chunks, the one-time cost is ~$1.28** (6.75M input tokens + 450K output tokens at GPT-4o-mini rates). This is the highest-ROI technique in the entire report. It directly addresses **Gap #5** (chunks lack document context) and substantially improves both vector and keyword retrieval.

**Implementation**: batch-process each chunk with its source document through GPT-4o-mini using the prompt "Give short succinct context to situate this chunk within the overall document." Prepend the context to the chunk text. Re-embed. Add `tsvector` column for BM25. Implement RRF fusion in SQL. **Total effort: 1–2 days.**

---

### HippoRAG 2 — the graph-RAG approach that doesn't sacrifice simple QA

Published February 2025, accepted at **ICML 2025**, HippoRAG 2 is the most significant graph-augmented RAG advance since the original HippoRAG. Its key innovation: it excels at multi-hop associative queries **without degrading simple factual QA** — a problem that plagues GraphRAG, LightRAG, and RAPTOR (all lose 5–10 F1 on simple queries).

HippoRAG 2 builds a dual-node knowledge graph with both phrase nodes and passage nodes, uses **Personalized PageRank (PPR)** for traversal from query entities, and adds LLM-based "recognition memory" to filter irrelevant triples. Benchmarks: MuSiQue F1 **44.8→51.9**, 2Wiki Recall@5 **76.5→90.4%**. Crucially, it uses only **9M tokens for indexing** versus 115M for GraphRAG — making it practical for API-based setups.

**Octo's existing AGE graph (2,769 entities, 7,015 edges) is essentially what HippoRAG 2 builds from scratch.** The PPR algorithm can be implemented via iterative SQL/Cypher queries on AGE. The open-source implementation (`OSU-NLP-Group/HippoRAG`, 3.7K stars) supports GPT-4o-mini for entity extraction. **Implementation complexity: MEDIUM-HIGH (2–3 weeks)** — mainly adapting their storage layer to AGE and implementing PPR over the existing graph.

---

### CoRAG — chain-of-retrieval from Microsoft

Published January 2025 and accepted at **NeurIPS 2025**, CoRAG trains models to dynamically plan retrieval steps based on accumulated context — essentially "o1-for-RAG." The full training methodology requires local model fine-tuning, but **the iterative sub-query pattern works as pure orchestration** over OpenAI API + pgvector. CoRAG-8B surpasses Search-o1-32B on KILT benchmarks, with **>10 EM points improvement on multi-hop QA**.

The pattern for Octo: query → generate sub-query → retrieve from pgvector/AGE → extract sub-answer → reformulate next sub-query based on accumulated context → repeat until answer complete. This composes naturally with the agentic retrieval system (Technique #7).

---

### FlashRank — the CPU reranking solution

FlashRank uses ONNX Runtime with INT8 quantized models, requiring **no PyTorch or Transformers dependency**. The TinyBERT model is **~4MB** and reranks 100 documents in ~100ms on a laptop CPU. The MiniLM-L-12 model takes ~400ms for 100 documents with higher quality. FlashRank achieves **95–98% of full cross-encoder accuracy** at 10–30× faster speed. Install: `pip install flashrank`. Integration exists for LangChain via `FlashrankRerank`.

For Octo's pipeline: pgvector (top 50) + BM25 (top 50) → RRF merge → FlashRank rerank (top 20) → top 5 to LLM. **Total reranking latency: ~100–200ms on CPU.** This directly addresses **Gap #2** with near-zero infrastructure overhead.

An alternative for maximum quality: **ModernBERT-based rerankers** (gte-reranker-modernbert-base, 149M params) match 1.2B-parameter models at **83% Hit@1** and run on CPU in ~150ms for 50 documents. The IBM `granite-embedding-reranker-english-r2` is Apache 2.0 licensed.

---

### ParadeDB pg_search — true BM25 inside PostgreSQL

ParadeDB's `pg_search` extension brings real BM25 scoring (with TF-IDF and length normalization) to PostgreSQL via a Rust-based Tantivy engine. Unlike native `tsvector`/`ts_rank` (which lacks IDF weighting), pg_search provides Elasticsearch-quality search within PostgreSQL. Installation via Docker image (includes pgvector), AGPL-3.0 license.

**The hybrid search query pattern** combining pgvector + pg_search + RRF is a single SQL query:

```sql
WITH vector_results AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> $query_vec) AS rank
    FROM documents ORDER BY embedding <=> $query_vec LIMIT 40
),
bm25_results AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY paradedb.score(id) DESC) AS rank
    FROM documents WHERE content ||| $query_text LIMIT 40
)
SELECT COALESCE(v.id, b.id),
    COALESCE(1.0/(v.rank+60), 0) + COALESCE(1.0/(b.rank+60), 0) AS rrf_score
FROM vector_results v FULL OUTER JOIN bm25_results b ON v.id = b.id
ORDER BY rrf_score DESC LIMIT 10;
```

**Lightweight alternative**: PostgreSQL's built-in `tsvector` + `ts_rank_cd` with GIN index. No extra extension needed. Quality is lower (no IDF) but adequate for ~4,500 chunks. **Recommendation: start with native tsvector for a quick win, upgrade to pg_search when the benefit justifies the dependency.**

---

### Late chunking and cross-document topic alignment

**Late chunking** (Jina AI, arXiv:2409.04701) feeds entire documents through a long-context transformer before splitting into chunk embeddings, preserving cross-chunk context. Improves nDCG@10 on BeIR benchmarks versus traditional chunking. Requires a long-context embedding model (Jina v3, 8K+ context). OpenAI's 8K token limit for embedding models may not cover full documents.

**Cross-Document Topic-Aligned Chunking (CDTA)** (November 2025) goes further — discovering global topics across the entire corpus and consolidating all relevant information from multiple documents per topic. Hit Rate@1 of **88%** versus 63% for Contextual Retrieval and 56% for semantic chunking. The approach maps naturally to entity clusters in AGE.

Both are worth evaluating at the next re-indexing cycle. For now, Contextual Retrieval provides a simpler path to chunk-context improvement.

---

## Layer 1 updates on previously evaluated techniques

**HippoRAG: Major upgrade → strong recommend ⬆️.** HippoRAG 2 (ICML 2025) adds passage nodes to the KG, query-to-triple linking (+12.5% Recall@5), and LLM-based recognition memory. Only technique that improves multi-hop without degrading simple QA. Uses 9M tokens for indexing versus 115M for GraphRAG. Works with GPT-4o-mini.

**Cross-encoder reranking: ModernBERT revolution → strong recommend ⬆️.** The `gte-reranker-modernbert-base` (149M params) matches 1.2B-param models at 83% Hit@1. CPU-viable for the first time. IBM's `granite-embedding-reranker-english-r2` (Apache 2.0) is the best open-license option.

**Contextual Retrieval: Validated with non-Claude models → strong recommend ⬆️.** Community implementations confirm GPT-4o-mini works. Together AI demonstrated Llama 3.2 3B. Cost for Octo's corpus: **~$1.28 one-time**. No dependency on Anthropic.

**Hybrid BM25+Dense with RRF: Consensus unchanged ➡️.** RRF with k=60 remains the default no-tuning-needed fusion. Dynamic per-query weighting is emerging but overkill for 4,500 chunks. A March 2025 paper found fusion benefits are "largely neutralized after reranking" — confirming that a good reranker matters more than sophisticated fusion.

**CRAG: Paper withdrawn, concept absorbed ➡️.** The original paper was withdrawn from ICLR 2025 (November 2024). However, CRAG's core principle — evaluate retrieval quality before generation — is now baked into every agentic RAG framework. LangGraph includes CRAG as a standard tutorial pattern. **Implement the evaluator concept as a node in the agentic pipeline, not as a standalone system.**

**Self-RAG: Skip direct implementation ⬇️.** Requires fine-tuned LLMs with special reflection tokens. Cannot be done with API-only access. The concept is better implemented as CRAG-style document grading or Adaptive-RAG routing using standard LLM calls.

**Adaptive-RAG: Now table stakes ➡️.** Explosion of implementations in 2025. LangGraph provides an official tutorial. For Octo, a **simple 2-way router** (needs retrieval vs. direct answer) saves tokens on simple queries. Full 6-category routing as described in Technique #7 is the more impactful version.

**OG-RAG: Published EMNLP 2025, conditional recommendation ➡️.** The paper is solid but the codebase is immature (6 commits). Only implement if a formal domain ontology exists or can be created. The emerging OntologyRAG ecosystem (Feb 2025+) suggests the pattern has legs but isn't ready for production adoption.

---

## Prioritized implementation roadmap

### Quick wins (< 1 day each)

**Add BM25 via native PostgreSQL full-text search.** Add a `tsvector` generated column to the chunks table, create a GIN index, and combine `ts_rank_cd` scores with pgvector cosine similarity via RRF in a single SQL query. No new dependencies. Addresses **Gap #3**. Upgrade to ParadeDB `pg_search` later for true BM25.

**Install FlashRank for cross-encoder reranking.** `pip install flashrank`, add a reranking step after hybrid retrieval. The MiniLM-L-12 model reranks 50 documents in ~200ms on CPU. Addresses **Gap #2**. Total footprint: ~50MB.

**Add a query complexity router.** A single GPT-4o-mini call classifying queries into 6 categories (direct entity, relationship, attribute, aggregation, exploratory, multi-hop) and routing to the appropriate retrieval strategy. Adds ~200ms latency but prevents over-retrieval on simple queries and enables deep retrieval on complex ones. Addresses **Gap #6** partially.

**Add a self-evaluation loop.** After initial retrieval, ask GPT-4o-mini: "Do you have enough information to answer this question? If not, what specific information is missing?" If insufficient, reformulate the query and retrieve once more (max 1 retry). Addresses **Gap #8**.

### Next sprint (1–5 days)

**Implement Contextual Retrieval.** Batch-process all 4,500 chunks through GPT-4o-mini to generate context snippets. Re-embed contextualized chunks. Add to the BM25 index. Cost: ~$1.28. This single change is projected to reduce retrieval failures by **49%** (or 67% combined with the reranker already installed). Addresses **Gap #5**.

**Build schema-aware SQL generation (Agentic Phase 1).** Create a comprehensive DDL prompt with column descriptions, sample values, and 20 validated NL→SQL examples. Implement parse→execute→retry loop with GPT-4o-mini. Fall back to existing 4 templates on failure. Measure first-attempt accuracy. Addresses **Gap #1** partially.

**Implement query decomposition.** For multi-hop queries, decompose into 2–4 sub-queries with retrieval method annotations (semantic/keyword/graph/SQL). Execute sub-queries independently, synthesize results. Addresses **Gap #4**.

### Strategic (1–4 weeks)

**Complete the agentic retrieval pipeline (Phases 2–4).** Add Text-to-Cypher via LangChain's AGE integration. Build a LangGraph state machine with conditional routing, document grading, and query rewriting. Implement query result caching and self-improving few-shot examples. This is the full realization of Technique #7.

**Evaluate HippoRAG 2 integration.** Implement Personalized PageRank over the existing AGE graph. Add passage nodes linking chunks to entities. Test whether PPR-based retrieval improves multi-hop queries over the current 2-hop traversal. If successful, this becomes the primary graph retrieval strategy.

**Deploy DeepEval evaluation pipeline.** Create a golden set of 100–200 Q&A pairs (50 synthetic via RAGAS TestsetGenerator, 50+ human-validated). Set up automated regression testing with faithfulness ≥ 0.7, context relevancy ≥ 0.6 thresholds. Run on every retrieval pipeline change.

**Investigate LightRAG as comparison baseline.** Deploy LightRAG alongside the existing system using PostgreSQL+pgvector+AGE. Feed existing documents through its extraction pipeline. Benchmark against the enhanced existing pipeline. If LightRAG outperforms, consider migration; if not, cherry-pick its entity deduplication and profile generation algorithms.

---

## Architectural recommendations

### Embedding model: stay with text-embedding-3-small for now

At **62.26 MTEB average** and **$0.02/M tokens**, text-embedding-3-small offers the best value for price-sensitive applications. The gap to higher-ranked models is modest: Voyage-3-large scores ~66.80 at $0.06/M, text-embedding-3-large scores ~64.60 at $0.13/M. For 4,500 chunks, re-embedding costs are trivial (~$0.09), so the barrier to switching is low.

**When to upgrade**: after implementing Contextual Retrieval, benchmark retrieval quality with the evaluation pipeline. If retrieval precision remains a bottleneck, upgrade to **Voyage-3-large** (best API cost:quality ratio) or **text-embedding-3-large with Matryoshka truncation to 1536 dims** (same API, easy switch). Note: text-embedding-3-small supports Matryoshka — truncating to 768 dims would halve index size with ~1–2% quality loss, worth testing.

### Reranker service: FlashRank primary, API fallback

**Primary: FlashRank with MiniLM-L-12** — ~200ms for 50 documents, no GPU, ~50MB total footprint, zero API cost. Install alongside the application.

**Fallback: Cohere Rerank 3.5 API** — $2/1K searches, ~50–100ms including network. Higher quality than any local CPU model. Use when quality must be maximized or as an A/B test comparison.

**Future: gte-reranker-modernbert-base (149M params)** — matches 1.2B-param models, runs on CPU. Requires PyTorch (heavier footprint than FlashRank). Evaluate when FlashRank's quality ceiling is reached.

### Apache AGE Cypher vs recursive CTEs

**Keep AGE for maintainability.** At Octo's scale (~7K edges), both AGE and recursive CTEs execute in single-digit milliseconds — the performance difference is negligible. AGE's Cypher syntax is far more readable for graph traversal logic and will be generated by LLMs more reliably than hand-crafted recursive CTEs.

**Critical AGE optimizations**: create explicit BTREE indexes on `id`, `start_id`, `end_id` for all edge labels, and GIN indexes on properties. These are not created automatically. Don't attempt vector similarity within Cypher calls — run pgvector search in SQL first, then use AGE for graph expansion on the results.

### BM25 strategy: native tsvector now, ParadeDB later

PostgreSQL's built-in `tsvector` + `ts_rank_cd` + GIN index provides adequate keyword search for ~4,500 chunks with zero additional dependencies. The main limitation is the absence of IDF weighting — `ts_rank` is frequency-only. For Octo's focused domain, this may not matter much.

**Upgrade to ParadeDB pg_search** when: (a) the corpus grows significantly, (b) keyword search quality becomes a measurable bottleneck in evaluations, or (c) you're already running the ParadeDB Docker image. The AGPL license requires consideration for deployment.

### Evaluation framework: DeepEval + RAGAS

**DeepEval** for running evaluations: pytest-style CI/CD integration, 7+ RAG metrics with reasoning explanations, component-level `@observe` decorator, hyperparameter tracking, handles LLM JSON errors gracefully. **13.6K stars**, Apache 2.0, no GPU needed, works with GPT-4o-mini.

**RAGAS** for generating synthetic test sets: knowledge-graph-based approach produces diverse query types (simple, multi-hop, reasoning). Use RAGAS to generate 100–200 evaluation samples, DeepEval to run the evaluations. **Cost: ~$0.10–0.50 per 100-sample run** with GPT-4o-mini.

Skip TruLens (observability-focused, Snowflake-centric direction) and ARES (requires GPU for fine-tuning judges, needs 150+ human annotations).

---

## What NOT to implement

**MemoRAG.** Requires 16–24 GiB GPU VRAM for the memory model. This is a hard physical constraint that cannot be worked around. The useful concept (generating retrieval clues) costs 10 lines of code with GPT-4o-mini.

**ColBERT / late interaction models.** pgvector doesn't support multi-vector embeddings. At 4,500 chunks, the retrieval problem is easy enough that single-vector + reranking matches ColBERT's quality. The PyTorch dependency and separate index infrastructure are unjustified overhead. Cross-encoder reranking via FlashRank provides 80% of the benefit at 20% of the complexity.

**Full Self-RAG.** Requires fine-tuned local LLMs with special reflection tokens. The concept (adaptive retrieval decisions, self-evaluation) is valuable but should be implemented through CRAG-style document grading and Adaptive-RAG routing using standard API calls.

**Multi-agent frameworks (CrewAI, AutoGen).** Designed for enterprise-scale systems with multiple data sources and agent specializations. Overkill for Octo's single-database, ~4,500-chunk architecture. A single LangGraph state machine with tool nodes covers all needed functionality with far less complexity.

**OGRAG2 codebase.** Six commits, no PostgreSQL support, no API server, no Docker. The paper's insights about ontology-grounded retrieval are useful conceptually but the implementation is unusable. If domain ontology construction ever becomes practical, re-evaluate.

**ARES evaluation framework.** Requires GPU for fine-tuning lightweight judges, plus 150+ manually annotated examples. DeepEval + RAGAS provide comparable evaluation quality with zero GPU and minimal human annotation.

**Dynamic per-query RRF weighting.** Emerging research (DAT, Dynamic Weighted RRF) shows 2–7.5% gains, but at 4,500 chunks with a good reranker, static k=60 RRF is sufficient. The added complexity of per-query weight prediction is not justified. A March 2025 enterprise study confirmed that fusion benefits are "largely neutralized after reranking."

**Late chunking (for now).** Requires a long-context embedding model. OpenAI's 8K token limit may not cover full documents. Contextual Retrieval achieves similar goals (preserving chunk context) at lower implementation complexity and works with any embedding model. Revisit late chunking at the next major re-indexing cycle if using Jina v3 or similar long-context models.

---

## The recommended pipeline architecture

The target retrieval pipeline after implementing the roadmap:

```
User Query
    ↓
[Query Router] — GPT-4o-mini classifies complexity → fast/standard/deep path
    ↓
[Query Decomposition] — complex queries split into sub-queries with method annotations
    ↓
[Parallel Hybrid Retrieval]
    ├─ pgvector semantic search (contextualized embeddings)
    ├─ BM25 keyword search (tsvector on contextualized chunks)
    ├─ AGE graph traversal (template or LLM-generated Cypher)
    └─ Dynamic SQL (LLM-generated, with schema-aware prompting)
    ↓
[RRF Fusion] — combine results from all retrieval paths
    ↓
[FlashRank Reranking] — CPU cross-encoder, top 20 → top 5
    ↓
[Sufficiency Check] — "Is this enough to answer?" If no → reformulate → re-retrieve
    ↓
[GPT-4o-mini Generation] — with structured output, confidence scores, provenance metadata
```

**Fast path** (\<1.5s): simple entity lookups, single retrieval strategy, no decomposition.
**Standard path** (\<3s): moderate queries, parallel retrieval, RRF + reranking.
**Deep path** (\<8s): complex multi-hop, full agentic loop with iterative retrieval.

This matches the Adaptive-RAG philosophy: pay the latency cost of complex strategies only for queries that need them. Every component is independently deployable, testable via DeepEval, and runs on a single VPS with PostgreSQL as the sole data store.