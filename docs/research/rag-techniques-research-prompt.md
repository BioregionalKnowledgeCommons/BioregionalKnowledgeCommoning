# Research Prompt: State-of-the-Art RAG Techniques for Knowledge Graph Retrieval

## Instructions

Run this prompt against a frontier model (Claude, GPT-4, Gemini Deep Research, etc.) with **web search enabled**. The prompt is structured in three layers: prior research summary, seed techniques not yet evaluated, and an open discovery mandate. The goal is a report that builds on what we know and discovers what we don't.

---

## Prompt

I'm building a bioregional knowledge commons chatbot called Octo. I need a comprehensive research report evaluating state-of-the-art RAG (Retrieval-Augmented Generation) techniques for my specific architecture. **This is not a survey — it's a decision document.** I need to know what to implement next.

### My Current Architecture

**Database:** PostgreSQL with pgvector (HNSW index) and Apache AGE (graph extension)

**Data model:**
- `entity_registry` — 2,769 entities across 23 types (Concept, Organization, Project, Location, Person, Practice, Bioregion, etc.) with 1536-dim embeddings (text-embedding-3-small)
- `entity_relationships` — 7,015 edges with typed predicates (related_to, broader, located_in, involves_organization, etc.)
- `koi_memory_chunks` — ~4,500 document chunks with 1536-dim embeddings, section-aware chunked from a MediaWiki wiki (salishsearestoration.org) and GitHub repos
- `koi_memories` — document-level records linking to chunks

**Current retrieval pipeline (B1 hybrid):**
1. Semantic entity search (pgvector cosine similarity on entity_registry.embedding)
2. Keyword fallback (ILIKE matching on normalized_text)
3. 2-hop relationship traversal (recursive CTE on entity_relationships)
4. Document chunk search (pgvector cosine on koi_memory_chunks, LIMIT 8, threshold 0.3)
5. Web source lookup (via document_entity_links bridge)
6. Template-based structured graph queries (4 SQL templates for entity/relationship lookup with entity resolution)
7. LLM prompt assembly (entities + relationships + graph query results + chunks + web sources)
8. GPT-4o-mini generates answer

**Experimental B2 (GraphRAG):** Community-aware retrieval using Louvain community detection + betweenness centrality. Not in production yet.

**What's working well:** Semantic entity search + chunk retrieval + structured graph templates provide grounded answers for most queries. Section-aware chunking improved granularity. 8/10 grounded on a 10-question QA evaluation.

**Known gaps:**
- No reranking (cross-encoder or otherwise)
- No BM25 or keyword-based retrieval beyond simple ILIKE
- No query reformulation or decomposition
- No multi-hop reasoning beyond the 2-hop CTE
- Entity descriptions are sparse (92% of Concepts are name-only embeddings)
- No contextual embedding (chunks are embedded without document-level context)
- Fixed retrieval limits (8 chunks, 5 entities) — no adaptive retrieval
- No agentic retrieval (system can't decide to search more, reformulate, or use tools)
- **LLM-as-retrieval-planner is primitive:** We have 4 hardcoded SQL templates triggered by keyword heuristics. The LLM doesn't decide the retrieval strategy, doesn't generate queries, and doesn't evaluate whether results are sufficient. The natural evolution is: LLM analyzes the question → decides what mix of semantic search, graph traversal, and structured queries to run → generates the queries → evaluates results → iterates if needed. This is the most important gap given our rich structured graph.

**Current infrastructure (not hard constraints — we are open to evolving):**
- Single VPS (45.132.245.30), currently no GPU
- PostgreSQL with pgvector + Apache AGE (Cypher-capable graph extension, installed but unused in retrieval)
- LLM: OpenAI API (GPT-4o-mini for chat, text-embedding-3-small for embeddings, 1536-dim)
- Re-embedding the full corpus (2,769 entities + 4,500 chunks) costs ~$0.05 and takes ~30 minutes — embedding model swaps are cheap

**What we're open to changing:**
- Adding a dedicated vector DB (Qdrant, Weaviate, Milvus, etc.) if it meaningfully improves retrieval
- Replacing or supplementing Apache AGE with a proper graph DB (Neo4j, etc.) if the query patterns justify it
- Using a GPU (renting a GPU instance, or adding one to the server) for local model inference (reranking, embedding, small LLMs)
- Switching embedding models (Nomic, Jina, Voyage, Cohere, etc.)
- Using different or multiple LLMs (Claude, Gemini, local models via Ollama, etc.)
- Flexible budget — willing to invest in infrastructure that demonstrably improves quality
- Multi-server architecture if needed

**Real constraints (actually hard):**
- Must remain self-hostable (no vendor lock-in to a single cloud provider)
- Must work with the existing PostgreSQL data model as the source of truth (can add other DBs as indexes/caches, but PostgreSQL stays)
- Production system serving real users — changes must be deployable without extended downtime

### Layer 1: Prior Research (already evaluated — build on this, don't retread)

We have a prior 430-line synthesis document evaluating ~20 techniques. Key conclusions already reached:

**High priority (decided to implement):**
- **HippoRAG** — Personalized PageRank associative memory. Prior finding: 20% improvement, 10-30x cost reduction vs GraphRAG. Fits PostgreSQL natively. **Status: not yet implemented.**
- **Hybrid BM25 + dense retrieval with RRF** — Reciprocal Rank Fusion combining sparse + dense. Prior finding: meaningful improvement on multi-hop queries, robust across query types. **Status: we have a reference implementation from the YonEarth Gaia chatbot (rank-bm25 + cross-encoder + category-first fusion).**
- **Cross-encoder reranking** — ms-marco-MiniLM-L-6-v2. Prior finding: consistently improves precision. Concern: latency on CPU-only server. **Status: not yet implemented.**
- **Contextual Retrieval** (Anthropic) — Prepending document context to chunks before embedding. Prior finding: 49% reduction in retrieval failures. **Status: not yet implemented.**

**Medium priority (evaluated, deferred):**
- **CRAG (Corrective RAG)** — Self-evaluation of retrieval quality with corrective web search. Deferred due to complexity.
- **Self-RAG** — Model decides when/whether to retrieve. Deferred — requires fine-tuned model or careful prompting.
- **OG-RAG** — Ontology-grounded chunking. Prior finding: 40% correctness, 55% fact recall improvement. Relevant given our BKC ontology. **Not implemented.**
- **Adaptive-RAG** — Query complexity classification routing to different retrieval strategies. Interesting but deferred.
- **DSPy** — Declarative prompt optimization. Evaluated, not adopted.

**Researched but deprioritized (with reasons — do not re-argue for these unless something fundamental has changed):**
- AL4RAG — needs annotation infrastructure we don't have
- SimRAG — requires fine-tuning infrastructure
- MAO-ARAG — over-engineered for single-VPS deployment
- KG2RAG — promising (ACL 2025) but requires graph expansion infrastructure
- RLKGF — requires RL training loop, too heavy for our scale
- GNN-RAG — graph neural network inference adds significant complexity
- GraphRAG (Microsoft) — community detection + map-reduce; expensive for our scale, HippoRAG preferred

### Layer 2: Seed Techniques (on our radar, not yet evaluated against current architecture)

Evaluate these against our current architecture and recommend whether they work with it as-is or require infrastructure evolution:

1. **OGRAG2** (Microsoft, github.com/microsoft/ograg2) — ontology-grounded RAG, successor to OG-RAG
2. **HyperGraphRAG** (LHRLAB, github.com/LHRLAB/HyperGraphRAG) — hypergraph-structured retrieval with hyperedges
3. **LightRAG** (github.com/HKUDS/LightRAG) — lightweight graph-augmented retrieval
4. **MemoRAG** (github.com/qhjqhj00/MemoRAG) — memory-augmented retrieval with global memory and clue generation
5. **RAPTOR** — recursive abstractive processing for tree-organized retrieval (hierarchical summarization)
6. **ColBERT / late interaction models** — token-level similarity, between bi-encoder and cross-encoder in cost/quality
7. **LLM-driven hybrid retrieval (Text-to-SQL + semantic + graph traversal)** — we have 4 hardcoded SQL templates triggered by keyword heuristics. The next step is an LLM that: (a) analyzes the question to determine what retrieval strategy to use, (b) generates SQL/Cypher queries dynamically, (c) combines structured results with semantic search, (d) evaluates whether the results are sufficient and iterates. Evaluate the full spectrum: simple Text-to-SQL, agentic query planning (ReAct-style), multi-step retrieval with self-evaluation, and tool-use patterns where the LLM calls the knowledge graph as a tool.

### Layer 3: Open Discovery Mandate

**This is the most important part.** Do not stop at the techniques listed above. Use web search to find and evaluate:

- **Techniques published 2024-2026** that are not in our seed list — especially anything with benchmark results on knowledge-graph-augmented retrieval
- **Agentic RAG / LLM-as-retrieval-planner** — This is our highest-priority research area. Systems where the LLM orchestrates retrieval: deciding what combination of semantic search, structured queries (SQL/Cypher), graph traversal, and web search to execute for each question. Look for: ReAct-style retrieval agents, tool-augmented LLMs that call databases as tools, multi-step retrieval with self-evaluation, query planning and decomposition, and architectures where the LLM generates and executes structured queries against knowledge graphs. Specific patterns to find: LLM → SQL generation → execution → result evaluation → re-query if insufficient.
- **Routing-based retrieval** — systems that classify queries and route to different retrieval strategies (semantic vs keyword vs graph vs structured)
- **Late chunking / chunk-free approaches** — alternatives to traditional chunk-and-embed
- **Tool-augmented retrieval** — retrieval systems that can call external tools (search engines, databases, APIs) as part of the retrieval step
- **Recursive / iterative retrieval** — systems that retrieve, reason, then retrieve again based on what was found
- **Speculative RAG** — generating multiple candidate answers from different retrieval paths
- **PostgreSQL-native innovations** — anything specifically designed for pgvector, Apache AGE, or PostgreSQL-based knowledge graphs
- **Embedding model innovations** — newer models (e.g., Nomic, Cohere, Jina, Voyage) that might outperform text-embedding-3-small for domain-specific retrieval
- **Structured output from retrieval** — returning not just text but typed entities, confidence scores, provenance chains
- **Compound AI systems** — architectures that combine multiple retrieval and reasoning steps (e.g., DSPy-style pipelines, LangGraph agents)
- **RAG evaluation frameworks** — automated answer quality scoring, retrieval relevance measurement, hallucination detection (RAGAS, ARES, TruLens, DeepEval). Our current QA is manual (10 questions, scored by hand). We need automated evaluation to measure the impact of each technique we implement.
- **Apache AGE / Cypher-native RAG patterns** — we have Apache AGE installed but use recursive CTEs instead of Cypher for graph traversal. Are there AGE-native retrieval patterns that would be more expressive or performant?

**Search broadly.** Look at arXiv papers from 2024-2026, conference proceedings (ACL, EMNLP, NeurIPS, ICLR), blog posts from AI labs (Anthropic, Google DeepMind, Meta FAIR, Microsoft Research), and open-source implementations on GitHub. I want to learn about techniques I don't know about yet.

### Output Format

1. **Executive Summary** — top 5-7 techniques recommended for Octo, ranked by impact × feasibility. State which of our known gaps each addresses.
2. **Seed Technique Evaluations** — detailed analysis of Layer 2 techniques using the 7-point template:
   - What it is (2-3 sentences)
   - How it works (key algorithmic steps)
   - Applicability to Octo (fit with current architecture, or what infrastructure changes needed)
   - Implementation complexity (Low/Medium/High + effort estimate)
   - Expected impact (which gaps it addresses)
   - Prerequisites (architecture changes needed)
   - Trade-offs (latency, cost, maintenance)
3. **Discovered Techniques** — techniques found via Layer 3 search that we hadn't considered. Same 7-point evaluation.
4. **Layer 1 Updates** — for techniques in our prior research, note any significant developments since March 2026 — new papers, new implementations, or changed recommendations. Don't re-evaluate from scratch.
5. **Prioritized Roadmap** — 3 tiers:
   - **Quick wins** (<1 day, significant impact)
   - **Next sprint** (1-5 days, substantial capability gain)
   - **Strategic** (1-4 weeks, architectural evolution)
6. **Architectural Recommendations** — any fundamental changes to consider (embedding model swap, adding a reranker service, using Apache AGE Cypher instead of recursive CTEs, etc.)
7. **What NOT to implement** — techniques that sound appealing but are wrong for our constraints. Explain why.

### Evaluation Criteria (weighted)

- **Impact on answer quality** (40%) — does this fix a real retrieval gap?
- **Implementation feasibility** (25%) — complexity, dependencies, migration effort from current architecture
- **Maintenance burden** (20%) — ongoing cost, reindexing needs, model hosting
- **Composability** (15%) — does this combine well with other techniques already in our pipeline?
