---
doc_id: bkc.federated-memory-arch
doc_kind: architecture
status: draft
depends_on:
  - bkc.project-vision
primary_for:
  - federated-memory
  - retrieval-architecture
  - agentic-retrieval
---

# Federated Memory Architecture

Canonical architecture for BKC's knowledge retrieval, agent memory, and federated reasoning layers. This doc sits between the [project vision](../project-vision.md) (why) and the [RAG techniques synthesis](../research/rag-techniques-synthesis.md) (subsystem spec for retrieval implementation).

## Scope

This document covers:
- Core domain objects that structure retrieval and reasoning
- The memory layer model and consistency semantics
- Federation trust and peer routing
- Graph-model stance (when to use what)
- Safety boundaries and anti-patterns

This document does NOT cover:
- Specific retrieval technique rankings (see [rag-techniques-synthesis.md](../research/rag-techniques-synthesis.md))
- KOI protocol mechanics (see [federation-overview.md](./federation-overview.md))
- Interoperability invariants (see [knowledge-commoning-meta-protocol-v0.1.md](./knowledge-commoning-meta-protocol-v0.1.md))
- Commitment economy design (see [commitment-economy-vision.md](./commitment-economy-vision.md))

## Layer model

```
Application        Chat, routing viz, flow funding, ingest UI
   ↕
Agent Memory       QueryPlan execution, ClaimSet reasoning, interaction cache
   ↕
Retrieval          Hybrid search, reranking, graph traversal, CRAG gate
   ↕
Interoperability   BKC ontology, meta-protocol conformance, exchange modes
   ↕
Protocol           KOI-net signed envelopes, RIDs, FUN events, edge governance
```

Each layer depends only on the layer below it. The protocol layer is documented in [federation-overview.md](./federation-overview.md). The interoperability layer is governed by the [meta-protocol](./knowledge-commoning-meta-protocol-v0.1.md). This document primarily covers the retrieval, agent memory, and application boundary layers.

## Core primitives

### PolicyScope

Trusted system constraint derived from caller identity, system policy, and membrane governance. Deterministic — never LLM-authored.

```
PolicyScope:
  visibility_tier: public | authorized | node_private
  eligible_peers: [node_ids from bioregion + edge approvals]
  consent_constraints: [from caller identity + governance rules]
```

The planner operates **within** a PolicyScope. It cannot widen scope — only request operations that the scope permits. This is the first routing decision: before any agentic complexity, the system determines what the caller is allowed to see.

### QueryPlan IR

A typed retrieval plan emitted by the planner and executed by trusted tool runners. Contains both the plan and its execution trace.

```
QueryPlan:
  policy_scope: PolicyScope
  query_taxonomy: entity_definition | relationship_path | governance_policy |
                  roadmap_status | commitment_claim | cross_node_provenance |
                  out_of_domain
  entities: [{name, type, candidates: [uri]}]
  steps: [{op, target, params, budget}]
  safety_guards: [max_steps, max_tokens, timeout]
```

The LLM emits typed operations (entity_lookup, relationship_traverse, text_search, graph_query). Trusted executors compile these to SQL, Cypher, or MCP tool calls. The LLM never writes raw SQL.

### EvidenceBundle

Internal evidence unit with provenance. Produced by retrieval stages, consumed by the reasoning layer.

```
EvidenceBundle:
  source_uri: str
  source_type: local_authoritative | local_document | trusted_peer | public_peer | web
  source_node: node_id
  retrieval_strategy: str
  confidence: float
  text: str
  provenance:
    visibility_tier: str
    freshness: datetime
```

Internal through Phase 2. External exposure deferred to Phase 4 (B12) after schema stabilization.

### ClaimSet

Claim-level reasoning layer assembled from EvidenceBundles. Where conflict detection, abstention, and answer grading happen.

```
ClaimSet:
  claims: [{assertion, evidence: [EvidenceBundle], confidence}]
  contradictions: [{claim_a, claim_b, nature}]
  overall_confidence: float
```

Contradictions are structural, not bugs. When local and federated evidence disagree, the system surfaces the disagreement with provenance rather than flattening to consensus. Immutable once assembled.

### PeerCapabilityRecord

Live peer state for routing decisions. Combines MCP capability discovery, A2A agent cards, and operational telemetry.

```
PeerCapabilityRecord:
  node_id: str
  mcp_endpoint: url
  a2a_card_url: url
  bioregions: [str]
  entity_types: [str]
  trust_tier: local_authoritative | trusted_peer | public_peer
  last_seen: datetime
  p50_latency_ms: int
  p95_latency_ms: int
  error_rate_7d: float
  capabilities_hash: str
```

Refreshed on connect, invalidated on peer change. Designed for 50-100+ nodes.

## Memory layers

| Layer | Stores | Consistency | Federated? |
|-------|--------|-------------|------------|
| **Epistemic** | Claims, evidence, provenance, conflict state | Append-only; conflicts preserved | Yes — signed envelopes |
| **Operational** | Roadmap, commitments, decisions, metrics, risk | Mutable; entity-type-aware freshness | Yes — event bridge |
| **Relational** | Entities, roles, stewards, peer capabilities | Slow-changing; re-embed on enrichment | Yes — entity exchange |
| **Interaction** | Prior queries, QueryPlans, cached EvidenceBundles | Ephemeral, TTL-based | Never |

**Entity-type-aware freshness**: Recency weighting applies only to time-bounded types — Commitment, WorkItem, Decision, Milestone, Metric, Risk. NOT to Concept, Pattern, Practice, Protocol, Bioregion, Location. Ecological knowledge and Indigenous practices are not penalized for age.

## Two-layer routing

Retrieval routing has two layers, applied in order:

1. **Deterministic policy/scope layer**: PolicyScope constrains visibility, eligible peers, consent. This is fast, cacheable, and never involves the LLM.
2. **Agentic taxonomy/depth layer**: The LLM classifies the query into a domain taxonomy and selects retrieval depth/budget. This is where query expansion, multi-tool orchestration, and peer selection happen.

The three routing axes:
- **PolicyScope** → what is the caller allowed to see?
- **QueryTaxonomy** → what kind of question is this? (7 types above)
- **Depth/Budget** → how much retrieval effort is warranted?

### CRAG corrective gate

After initial retrieval, a corrective gate evaluates whether the evidence is sufficient:

1. **Cheap signals first**: Score gaps, diversity metrics, entity coverage
2. **LLM judge for borderline**: Only when cheap signals are ambiguous
3. **Three-way decision**: CORRECT (proceed) / AMBIGUOUS (expand retrieval) / INCORRECT (reformulate or abstain)

## Graph-model stance

**Polyglot semantic architecture. PostgreSQL-first, storage-agnostic.**

Do not choose a single graph substrate. Different graph traditions serve different needs:

| Technology | Role in BKC | Status |
|------------|-------------|--------|
| **Apache AGE** (Postgres + openCypher) | Graph storage, path traversal, GraphRAG, neighborhood queries | Production |
| **pgvector** | Embedding storage, semantic similarity | Production |
| **JSON-LD** (`bkc-ontology.jsonld`) | Cross-system interoperability bridge — JSON that CAN be read as RDF without requiring RDF tooling | Production |
| **RDF / SHACL** | Formal ontology alignment, FAIR data interop, semantic web integration | JSON-LD now; no RDF-native toolchain or workflows today. RDF-native workflows become relevant when triggered (see below) |
| **AD4M / Coasys** | Personal subjective overlays, agent-local perspectives | Candidate concept — the Perspectives model is the right *idea* for sovereign agent memory; whether AD4M is the right *implementation* depends on their roadmap (SPARQL support is planned, not shipped; runtime uses SurrealDB) |
| **GQL (ISO 39075:2024)** | Standard direction for property graphs | Not actionable yet — AGE uses openCypher; GQL conformance is partial across vendors |

**AGE specifics**: AGE is a Postgres extension, not a standalone database. Cypher queries run inside SQL via `cypher()` function calls. Hybrid SQL+Cypher works — Cypher results can participate in CTEs, JOINs, IN, and EXISTS clauses. You cannot write arbitrary SQL inside Cypher directly; SQL-in-Cypher requires user-defined functions.

**When to use what**:
- **Traversal, path queries, entity neighborhoods, GraphRAG** → AGE / Cypher
- **Cross-system ontology metadata, schema publication** → JSON-LD (current), RDF/SHACL (if formal alignment needed)
- **Subjective agent-local knowledge, personal overlays** → AD4M Perspectives model (concept); implementation TBD
- **Embedding search, hybrid retrieval** → pgvector + BM25 via tsvector

**Escape hatch**: If corpus exceeds ~50K entities and dynamic community detection becomes critical (LazyGraphRAG territory), the architecture supports swapping to Neo4j or JanusGraph. The QueryPlan IR abstracts over the storage layer.

**One-line summary**: Property graphs are the retrieval/execution language; JSON-LD is the current interop bridge; RDF becomes relevant at formal ontology boundaries; AD4M is a future candidate for sovereign agent memory.

**RDF adoption triggers** — RDF-native workflows move from aspirational to planned when any of:
1. Formal ontology exchange with external systems (Solid pods, linked open data catalogs, FAIR data repositories)
2. AD4M/Coasys integration requiring RDF/SPARQL compatibility at the agent-memory boundary
3. Cross-node shared profiles (claims, evidence, commitments) need SHACL validation beyond what JSON Schema provides

## Federation trust model

Five protocols, layered:

| Protocol | Role | Status |
|----------|------|--------|
| **KOI-net** | Signed envelopes, RIDs, edge governance | Production |
| **MCP** | Live capability truth (tool discovery) | Production |
| **A2A Agent Cards** | Peer catalog discovery | Production |
| **OpenTelemetry** | Routing signals (latency, error rates) | Phase 2 |
| **OAuth metadata (RFC 9728)** | Auth discovery at scale | Phase 4 |

Trust tiers for evidence ranking:

1. **Local authoritative** — entities/claims created and verified on this node
2. **Local documents** — ingested content (wiki, web, transcripts)
3. **Trusted peer** — nodes with approved edges and verified track record
4. **Public peer** — nodes with edges but limited history
5. **Web** — external web content, lowest trust

## Safety boundaries

### Permission-aware abstention

When a query touches content restricted by visibility scope, the system uses a **metadata-level shadow signal**: it knows restricted content *exists* for this topic (from aggregate type metadata) but never discloses individual records, counts, or denied-hit information. The response includes a note like "additional information may be available with appropriate authorization."

### Write-back gates

- **Interaction layer**: Auto-cache permitted (TTL-based, ephemeral)
- **Relational layer**: Auto-update from enrichment pipelines (entity re-embedding, capability refresh)
- **Operational layer**: Requires steward review for state changes (commitment advancement, roadmap updates)
- **Epistemic layer**: Always requires human gate (new claims, evidence, attestations)

## Anti-patterns

1. **No raw LLM SQL.** All database queries pass through typed operations, allowlist validation, parameterization, and budget guards.
2. **No planner-authored scope widening.** The LLM requests operations within PolicyScope. It cannot escalate its own permissions.
3. **No global recency bias.** Freshness weighting is entity-type-aware. Ecological concepts, patterns, and practices are not penalized for age.
4. **No blind federation fan-out.** Peer queries are targeted by bioregion, entity coverage, and trust tier — not broadcast to all peers.
5. **No untrusted content in execution path.** Federated and web content informs answers. It never drives tool calls, plan execution, or scope changes.
6. **No automatic write-back to epistemic/operational memory.** Interaction caching is automatic; everything else requires a steward gate.
7. **No consensus-flattening.** Cross-node disagreement is preserved and surfaced with provenance, not merged into a single answer.
8. **No fine-tuned models for retrieval grading.** CRAG-style cheap signals first; LLM judge only for borderline cases.
9. **No direct exposure of internal EvidenceBundle metadata.** Visibility tier and consent constraints are stripped at the API boundary until Phase 4.

## Implementation phases

**Phase 1** (B5-B8, deployed): Eval pipeline, hybrid BM25+RRF, FlashRank reranking, contextual retrieval. Context relevancy 0.18 → 0.38. Closing: B8a entity enrichment + re-embedding, B8b multi-query expansion.

**Phase 2** (B9, next): QueryPlan IR + two-layer router → schema-aware SQL → text-to-Cypher → CRAG gate → multi-tool orchestrator with ClaimSet reasoning. PeerCapabilityRecord as first-class contract.

**Phase 3** (B2, B11): HippoRAG2 PPR for associative graph memory. RAPTOR hierarchical summarization. Entity-type-aware freshness. Graph substrate hardening.

**Phase 4** (B12): Federated QueryPlan execution via MCP tool contracts. EvidenceBundle external API. Cross-node conflict-preserving answering. Permission-aware abstention. AD4M optional integration (B13).

See [rag-techniques-synthesis.md](../research/rag-techniques-synthesis.md) for technique evaluations and implementation sequencing. See [semantic-roadmap.json](../roadmap/semantic-roadmap.json) for execution tracking.
