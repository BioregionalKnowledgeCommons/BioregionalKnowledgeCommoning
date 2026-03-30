---
doc_id: bkc.live-retrieval-arch
doc_kind: architecture
status: active
depends_on:
  - bkc.federated-memory-arch
---

# Live Retrieval Architecture

**Scope:** What is actually deployed on Octo production. Not aspirational, not considered-and-rejected. Every claim in this document is verifiable against the source code at the referenced SHAs.

**Distinction from related docs:**
- `federated-memory-architecture.md` describes what SHOULD BE (five core objects, four memory layers, federation trust model).
- `docs/research/rag-techniques-synthesis.md` documents what WAS CONSIDERED.
- This document describes what IS DEPLOYED.

## Deployed State

Two relevant SHAs on `regen-prod`:

| SHA | Phase | What Changed |
|-----|-------|-------------|
| `27c23daa` | B9c | Planner retrieval baseline: decision matrix, all executor logic, classifier tuning, governance closeout |
| `63bda13f` | P1 | Provider abstraction: per-surface LLM decoupling, no retrieval changes |

The planner is activated on production via `planner=true` parameter on `POST /chat`. The commons-web BFF routes pass this flag, so the planner path is live on `salishsee.life`.

## Architecture Overview

```
                                 Query
                                   |
                                   v
                    +----------------------------+
                    |   Layer 1: PolicyScope     |
                    |   (deterministic, no LLM)  |
                    |   v0: hardcoded public     |
                    +----------------------------+
                                   |
                                   v
                    +----------------------------+
                    |  Layer 2: Classifier        |
                    |  GPT-4o, 7-taxonomy,        |
                    |  confidence threshold 0.7   |
                    +----------------------------+
                           |              |
                     confidence >= 0.7    < 0.7
                           |              |
                           v              v
                    +---------------+  +------------------+
                    | Layer 3: Plan |  | Fallback to      |
                    | Assembly      |  | baseline (legacy) |
                    | (decision     |  | retrieval path    |
                    |  matrix)      |  +------------------+
                    +---------------+
                           |
            +--------------+---------------+-----------------+
            |              |               |                 |
            v              v               v                 v
    +-----------+  +-------------+  +-----------+  +-------------+
    | entity    |  | text_search |  | relation  |  | structured  |
    | _lookup   |  | BM25+vector |  | _traverse |  | _sql        |
    |           |  | RRF+rerank  |  | (gov only)|  | (roadmap    |
    +-----------+  +-------------+  +-----------+  |  only)      |
            |              |               |       +-------------+
            +--------------+---------------+-----------------+
                                   |
                                   v
                    +----------------------------+
                    | Web Source Enrichment       |
                    | (deterministic post-step,   |
                    |  runs if entity_uris found) |
                    +----------------------------+
                                   |
                                   v
                    +----------------------------+
                    | Context Assembly            |
                    | EvidenceBundle -> legacy    |
                    | 4-tuple for prompt builder  |
                    +----------------------------+
                                   |
                                   v
                    +----------------------------+
                    | LLM Answer Generation       |
                    | GPT-4o-mini (default)       |
                    +----------------------------+
                                   |
                                   v
                               Response
                     (answer + sources + plan_trace)
```

## Three-Layer Router

### Layer 1: PolicyScope (deterministic, no LLM)

- **Input:** Request context (currently no auth identity)
- **Output:** `PolicyScope(visibility_tier="public", include_node_private=false)`
- **v0 implementation:** Hardcoded public scope. Mirrors existing `node_private` filtering on `entity_registry` and `koi_memory_chunks`.
- **Future:** Will derive from `commons_memberships` + edge governance tables when WebAuthn auth identity is threaded to the retrieval path.
- **Schema:** `api/schemas/query_plan.py` `PolicyScope` model

### Layer 2: Query Classification (LLM-driven)

- **Model:** GPT-4o (upgraded from GPT-4o-mini in Phase 5b)
- **Accuracy:** 96.2% on 52-question eval set (50/52 correct)
- **Confidence threshold:** 0.7. Below this, falls back to the baseline (non-planner) retrieval path.
- **Temperature:** 0.0 (deterministic)
- **Token budget:** ~100-200 input, ~50 output, ~200ms latency
- **Implementation:** `api/query_classifier.py` `classify_query()`
- **Provider env vars:** `CLASSIFIER_PROVIDER` (default: `openai`), `CLASSIFIER_MODEL` (default: `gpt-4o`)

**7-class taxonomy** (`api/schemas/query_plan.py` `QueryTaxonomy`):

| Taxonomy | Description | Example |
|----------|-------------|---------|
| `entity_definition` | What is X? Single concept/entity lookup | "What is eelgrass?" |
| `relationship_path` | How does X relate to Y? Connections, multi-hop | "Which organizations work on restoration?" |
| `governance_policy` | Governance rules, protocols, data sovereignty | "What is the BKC meta-protocol?" |
| `roadmap_status` | Project status, milestones, deployed features | "What is the status of commitment pooling?" |
| `commitment_claim` | Pledges, claims, evidence, pools, settlements | "What commitments has Victoria Landscape Hub made?" |
| `cross_node_provenance` | Cross-node comparison, node-specific data | "What does the Front Range node know about X?" |
| `out_of_domain` | No connection to BKC domain | Immediate abstention, no retrieval |

**Post-classifier guardrail (Guard 3):** If the classifier returns `out_of_domain` but the query contains BKC domain signals (bioregion, knowledge commons, claims engine, federation, etc.), the guardrail reclassifies to the most specific matching in-domain category with reduced confidence (0.5-0.65). Guards 1 and 2 were removed after the tuned prompt made them unnecessary.

### Layer 3: Plan Assembly (deterministic, no LLM)

Decision matrix lookup from `ClassifierOutput` to ordered `PlanStep` list. No LLM involvement. Depth tier modifies step parameters.

**Implementation:** `api/query_planner.py` `assemble_plan()`

## Decision Matrix

This is the core of what is deployed. Each row maps a taxonomy classification to an ordered sequence of retrieval steps with specific parameters.

| QueryTaxonomy | Steps | Depth | Key Params | Notes |
|---------------|-------|-------|------------|-------|
| `entity_definition` | entity_lookup -> text_search | standard | el=5, top_k=8 | -- |
| `relationship_path` | entity_lookup(3) -> text_search(multi_query) | standard | el=3, top_k=8 | B9c: RELATIONSHIP_TRAVERSE removed (over-retrieval) |
| `governance_policy` | text_search(multi_query) -> entity_lookup -> relationship_traverse(hops=1) | deep | el=8, top_k=12, rt=30 | B9d/B9d.1/B9d.2 tuning attempted, none beat default. Drag accepted. |
| `roadmap_status` | entity_lookup -> structured_sql(roadmap) -> text_search | standard | el=5, sql=15, top_k=6 | -- |
| `commitment_claim` | entity_lookup(3) -> text_search(multi_query) | standard | el=3, top_k=8 | B9b.1: STRUCTURED_SQL removed (over-retrieval) |
| `cross_node_provenance` | entity_lookup -> text_search | standard | el=5, top_k=8 | -- |
| `out_of_domain` | (none) | -- | -- | Immediate abstention, no retrieval executed |

**Key:** `el` = entity_lookup max_results, `top_k` = text_search top_k after reranking, `rt` = relationship_traverse max_results, `sql` = structured_sql max_results.

### Depth Tier Overrides

The classifier may recommend a depth tier. Plan assembly applies it:

| Depth | Effect |
|-------|--------|
| `shallow` | entity_lookup steps only. Skip text_search and relationship_traverse. |
| `standard` | Use steps from decision matrix as-is. |
| `deep` | Add `multi_query=true` to all text_search steps. Increase `max_results` by 50% on all steps. |

### Governance Tuning Closeout (B9d/B9d.1/B9d.2)

Governance retrieval was the last remaining category drag (-3.4% CR vs default). Three rounds of tuning were attempted and all failed:

- **B9d** (text-search-first, remove RELATIONSHIP_TRAVERSE): -3.4% CR
- **B9d.1** (Variant A text+entity, Variant B text-only): Both lost. Revealed governance is internally mixed (definition vs policy sub-intents).
- **B9d.2** (within-category sub-routing): Definition branch improved massively (+112% avg CR on governance definition questions), but policy branch still lost to default. Net: -8.5% to -11.0% CR.

**Conclusion:** The planner's governance plan produces different retrieval composition from the default path, and no configuration of planner-controlled steps has matched default's governance performance. The overall planner still passes canonically (+6.2% CR) with governance drag included. No further governance tuning planned.

## Four Live Executors

### entity_lookup

- **Wraps:** Semantic (pgvector cosine similarity) + keyword (ILIKE) search on `entity_registry`
- **Used by:** All non-OOD categories
- **Params:** `query`, `max_results` (varies: 3, 5, or 8 per category), `include_node_private` (default false)
- **Returns:** `EvidenceBundle[]` with `source_type=LOCAL_AUTHORITATIVE`
- **Fallback:** If vector search fails (dimension mismatch, missing column), falls back to keyword search on `normalized_text`
- **Implementation:** `api/retrieval_executors.py` `entity_lookup()`

### text_search

- **Wraps:** Hybrid BM25 + vector RRF fusion + FlashRank cross-encoder reranking on `koi_memory_chunks`
- **Used by:** All non-OOD categories
- **Params:** `query`, `multi_query` (true for relationship_path, commitment_claim, governance_policy), `include_code` (default false), `top_k` (varies: 6, 8, or 12)
- **Returns:** `EvidenceBundle[]` with `source_type=LOCAL_DOCUMENT`
- **Pipeline detail:** See "Retrieval Pipeline Detail" section below
- **Implementation:** `api/retrieval_executors.py` `text_search()`

### relationship_traverse

- **Wraps:** N-hop recursive CTE on `entity_relationships` table
- **Used by:** `governance_policy` ONLY (max_hops=1, max_results=30)
- **Removed from:** `relationship_path` in B9c (over-retrieval even at 1-hop caused noise)
- **Params:** `entity_uris` (from preceding entity_lookup), `max_hops`, `max_results`
- **Returns:** `EvidenceBundle[]` with `source_type=LOCAL_AUTHORITATIVE`, text formatted as `"subject --[predicate]--> object"`
- **Confidence:** `1.0 / depth` (closer hops = higher confidence)
- **Node_private filtering:** Hardcoded in the recursive CTE (`WHERE NOT COALESCE(s.node_private, false)`)
- **Implementation:** `api/retrieval_executors.py` `relationship_traverse()`

### structured_sql

- **Wraps:** Template-driven (allowlisted) SQL queries against `commitments`, `claims`, and `entity_registry` (roadmap types)
- **Used by:** `roadmap_status` ONLY (template=`roadmap`)
- **Removed from:** `commitment_claim` in B9b.1 (over-retrieval noise)
- **Templates:** `commitment` (queries commitments + claims tables), `roadmap` (queries entity_registry for Initiative, WorkItem, Milestone, Outcome, Decision, Metric, Risk types)
- **Safety:** Never generates freeform SQL from user queries. All queries use parameterized templates with `$1`, `$2` placeholders. Unknown templates return empty.
- **Cap:** Unfiltered results (no entity_uris) capped at 5 to avoid noisy global dumps.
- **Returns:** `EvidenceBundle[]` with `source_type=LOCAL_AUTHORITATIVE`
- **Implementation:** `api/retrieval_executors.py` `structured_sql()`

### web_source_lookup (deterministic post-step)

Not dispatched via `PlanStep.op`. Always runs after all plan steps complete if any `entity_uris` were collected.

- **Wraps:** Web submissions linked to matched entities via `document_entity_links`
- **Returns:** `EvidenceBundle[]` with `source_type=LOCAL_WEB`, max 5 results
- **Implementation:** `api/retrieval_executors.py` `web_source_lookup()`

## Two Stub Executors

### graph_query

- **Purpose:** Cypher queries via Apache AGE for typed pattern matching
- **Current behavior:** Returns empty list, logs debug message
- **Implementation:** `api/retrieval_executors.py` `graph_query()`

### peer_query

- **Purpose:** Federation fan-out to eligible peers via MCP
- **Current behavior:** Returns empty list, logs debug message
- **Requires:** `PolicyScope.eligible_peers` (not in v0), `SafetyGuards.max_peer_fanout` (hardcoded to 0)
- **Implementation:** `api/retrieval_executors.py` `peer_query()`

## Retrieval Pipeline Detail

The `text_search` executor implements a multi-stage retrieval pipeline:

### Stage 1: Candidate Generation (BM25 + Vector)

Two parallel retrieval paths on `koi_memory_chunks`:

- **Vector:** pgvector cosine similarity search, top 40 candidates
- **BM25:** tsvector full-text search with `ts_rank_cd`, top 40 candidates. Index: GIN on `tsv` column (migration 073, GENERATED ALWAYS from content text + context)

Both paths apply source-aware corpus filtering: code entity chunks excluded by default (`c.content->>'entity_name' IS NULL`). Overridable via `include_code=true`.

### Stage 2: Reciprocal Rank Fusion (RRF)

FULL OUTER JOIN of vector and BM25 results on chunk `id`. RRF score: `1/(vrank+60) + 1/(brank+60)`. Top 20 candidates selected.

**BM25-only fallback:** On embedding dimension mismatch (`asyncpg.DataError`), falls back to BM25-only ranking. This handles the case where chunk embeddings were generated with a different model dimension.

### Stage 3: Multi-Query Expansion (conditional)

When `multi_query=true` (enabled for relationship_path, commitment_claim, governance_policy):

- LLM generates 3 reformulations of the original query via `expand_queries_fn`
- Each variant gets its own embedding and runs the full BM25+vector pipeline
- Cross-query RRF fusion: scores from all variants are summed per chunk (deduplication by chunk ID)
- Provider: GPT-4o-mini via `create_expansion_provider()`

### Stage 4: FlashRank Reranking

Cross-encoder reranking via `ms-marco-MiniLM-L-12-v2` (FlashRank):

- Input: Top 20 RRF candidates
- Output: Top `top_k` (varies by category: 6, 8, or 12)
- Model size: ~50MB, ~2s first call (lazy load), ~200ms subsequent
- Graceful degradation: If flashrank is not installed, reranking is skipped

### Corpus Enrichment (pre-computed, not per-query)

- **Contextual embeddings (B8):** 3,605 chunks enriched with 1-2 sentence GPT-4o-mini context describing the chunk's role in its parent document. Context stored in `content.context` JSON field and included in tsvector index.
- **Entity enrichment (B8a):** 2,524 entities re-described and re-embedded with context-rich text combining `metadata.context` + `description`.

## Provider Abstraction

Three independent LLM providers, each configurable via env vars. Factory pattern in `api/chat_provider.py`.

| Surface | Default Provider | Default Model | Env Vars |
|---------|-----------------|---------------|----------|
| Classifier | OpenAI | gpt-4o | `CLASSIFIER_PROVIDER`, `CLASSIFIER_MODEL` |
| Chat answer | OpenAI | gpt-4o-mini | `CHAT_PROVIDER`, `CHAT_MODEL` |
| Query expansion | OpenAI | gpt-4o-mini | `EXPANSION_PROVIDER`, `EXPANSION_MODEL` |

**Implementations:** `OpenAIChatProvider` and `AnthropicChatProvider`. Both implement the `ChatProvider` ABC with a single `complete()` method. The Anthropic adapter handles system message extraction and appends JSON instruction for `json_mode` (Anthropic has no native json_mode).

**Bakeoff result (P2):** 8 frozen prompt packets, OpenAI vs Anthropic side-by-side. OpenAI wins 6/8. Anthropic better only on dense commitment/mechanism questions. Decision: stay on OpenAI default. No on-node Anthropic deployment.

**Classifier is OpenAI-only:** The `create_classifier_provider()` factory only supports OpenAI because structured output behavior is sensitive to provider differences.

## Safety Guards

Enforced by `api/plan_executor.py` `execute_plan()`:

| Guard | Default | Behavior on Violation |
|-------|---------|-----------------------|
| `max_steps` | 6 | Halts execution, logs warning |
| `max_total_tokens` | 16,000 | (Budget tracked per step, not yet enforced at plan level) |
| `timeout_ms` | 15,000 | Halts execution based on wall-clock elapsed time |
| `max_peer_fanout` | 0 | v0: local only, no federation fan-out |

## Evaluation Contract

**Golden QA set:** 52 questions in `tests/eval/golden_qa.json`

**8-category taxonomy** (aligned with router, `tests/eval/eval_taxonomy.md`):

| Category | Count | QueryTaxonomy Mapping |
|----------|-------|----------------------|
| entity_definition | 20 | entity_definition |
| relationship | 15 | relationship_path |
| multi_hop | 15 | relationship_path |
| governance | 10 | governance_policy |
| roadmap_status | 10 | roadmap_status |
| commitment_claim | 10 | commitment_claim |
| thematic | 10 | entity_definition or governance_policy |
| negative | 10 | out_of_domain |

**DeepEval metrics:** faithfulness, answer_relevancy, context_relevancy, evidence_recall

**6 automated gates:**

| Gate | Threshold | Description |
|------|-----------|-------------|
| CR (context_relevancy) | Candidate >= baseline | Primary quality metric |
| In-domain AR (answer_relevancy) | Within 5% of baseline | Excludes OOD questions |
| OOD abstention | >= 80% | Out-of-domain questions correctly refused |
| Faithfulness | Candidate >= baseline | No hallucination regression |
| Classifier accuracy | >= 90% | Measured from plan_trace telemetry |
| Errors | Candidate <= baseline | No increase in execution errors |

**Judges:** Canonical: `gpt-4.1`. Dev: `gpt-4.1-mini` (agrees with canonical on direction, 90% cheaper).

**Eval runner:** `tests/eval/run_eval.py` with flags: `--ids` (subset), `--metrics` (single metric), `--rescore` (offline rescoring), `--planner` (enable planner path), `--eval-model` (judge model override).

**Canonical A/B result (gpt-4.1 judge, 52/52 both paths, v7 planner vs frozen v5 default):**

| Gate | Result | Value |
|------|--------|-------|
| CR | PASS | 0.3835 -> 0.4071 (+6.2%) |
| In-domain AR | PASS | 0.9441 -> 0.9439 (-0.02%) |
| OOD abstention | PASS | 100% (6/6) |
| Faithfulness | PASS | 0.984 -> 0.9888 (+0.5%) |
| Classifier accuracy | PASS | 96.2% |
| Errors | PASS | 0, 0 |

## Context Assembly

After all executors return `EvidenceBundle[]`, the plan executor hands the flat list to `evidence_bundles_to_legacy_format()` which partitions into a 4-tuple consumed by the prompt builder:

| Partition | Source | Used In Prompt As |
|-----------|--------|-------------------|
| `sources` | entity_lookup + structured_sql + web | Entity descriptions and structured data |
| `relationships_ctx` | relationship_traverse | Formatted edge strings |
| `doc_chunks` | text_search | Document excerpts with context |
| `web_sources` | web_source_lookup | Web submission summaries |

**Implementation:** `api/retrieval_executors.py` `evidence_bundles_to_legacy_format()`

## Source Files

| File | Role |
|------|------|
| `api/schemas/query_plan.py` | 13 Pydantic models (QueryPlan, PolicyScope, ClassifierOutput, EvidenceBundle, etc.) |
| `api/chat_provider.py` | ChatProvider ABC + OpenAI/Anthropic implementations + 3 factory functions |
| `api/query_classifier.py` | Layer 2: GPT-4o classifier with tuned prompt and OOD-recovery guardrail |
| `api/query_planner.py` | Layer 3: Decision matrix lookup, depth tier overrides, plan assembly |
| `api/plan_executor.py` | Plan execution: step dispatch, safety guards, web enrichment post-step |
| `api/retrieval_executors.py` | 4 live executors + 2 stubs + web_source_lookup + legacy adapter |
| `docs/specs/b9a-query-plan-spec.md` | Primary spec: decision matrix, router contract, tuning history |
| `tests/eval/golden_qa.json` | 52 golden QA questions |
| `tests/eval/run_eval.py` | Eval runner with A/B comparison, category reporting, gate verdicts |
| `tests/eval/eval_taxonomy.md` | 8-category taxonomy, labeling rubric, evidence recall metric |
