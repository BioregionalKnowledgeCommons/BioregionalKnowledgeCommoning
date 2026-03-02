# BKC Summarizer Vanguard Architecture
Date: 2026-03-02
Owner: Darren Zal
Status: Draft for Mar 5 build-day execution

## Purpose

BKC should lead the Summarizer implementation pattern for the coalition.
We do not wait for external teams to define transcript-to-graph quality standards.
We provide the reference path, contract, and validation harness; partners integrate to it.

## Strategic Position

The coalition has strong coordination energy, but no shared production-grade Summarizer reference.
BKC already has the core pieces in production:

- Transcript-to-structured-note pipeline and entity extraction discipline
- Multi-tier entity resolution with contextual disambiguation
- Quality gates before ingestion
- Contracted ingest endpoint with auth and idempotency semantics
- Provenance receipts and federated graph availability

This means BKC can show and teach, not just propose.

## What We Reuse (No Reinvention)

1. `darren-workflow`: meeting pipeline and extraction discipline
2. `Octo`: resolver, ingest, quality gates, provenance, federation
3. `yonearth-gaia-chatbot`: dual-signal relationship evaluation and reflector loop
4. `RegenAI`: quality-audit and threshold calibration patterns

## Reference Pipeline (v1)

1. Capture
- Input: transcript (`.whisper`, Otter export, or meeting note body).
- Normalize into a deterministic text envelope with source metadata.

2. Structured Extraction
- Extract:
  - `entities[]`: person/org/project/concept/location/meeting/bioregion/etc.
  - `relationships[]`: typed edges in BKC predicate vocabulary
  - `action_items[]` and `decisions[]` for operational follow-through
- Output is schema-valid JSON, not free text.

3. Resolution
- Resolve each entity using multi-tier strategy:
  - exact normalized match
  - alias match
  - contextual co-occurrence + phonetic boost
  - fuzzy match with token-overlap guard
  - semantic match (pgvector)
  - deterministic new URI generation if unresolved

4. Quality Gates
- Run pre-ingest checks:
  - confidence thresholding
  - entity-quality filtering (pronouns/placeholders/noise)
  - duplicate handling
  - source relevance policy

5. Ingest Contract
- Send normalized payload to BKC `/ingest` via BFF:
  - auth header: `x-ingest-token`
  - required: `document_rid`, `source`, `entities`
  - optional: `content`, `relationships`
- Preserve stable `document_rid` across retries.

6. Provenance + Federation
- Record receipt chain and operation stats.
- Make new entities queryable in node and available for federation.

7. Verification
- Confirm:
  - ingest success
  - expected entities resolvable via search
  - expected relationship visibility
  - receipt existence
  - no duplicate entity-link rows for same `document_rid`

## Contract Surface (Canonical)

Use the frozen contract in:
- `Octo/docs/integration/summarizer-ingest-contract.md`

Contract principles:
- Strict required fields, no implicit source
- Stable `document_rid` for partial idempotency
- Explicit retry policy (retry upstream failures, not caller errors)
- Token shared out-of-band

## Golden Fixture Set (for this week)

Create three fixtures and expected outcomes:

1. Clean transcript
- Well-formed names, orgs, and meeting title.
- Expect mostly exact/alias resolution.

2. Noisy transcript
- Filler words, fragmented grammar.
- Expect quality gates to reject noise entities.

3. Typo-heavy names
- Misspellings/phonetic variants.
- Expect contextual + fuzzy + semantic tiers to recover true matches.

Each fixture should include:
- `input.json` (transcript envelope)
- `expected_entities.json`
- `expected_relationships.json`
- `expected_stats.json`

## Demo-Ready Teaching Sequence (5-10 min)

1. Show payload contract (schema and required fields).
2. Run one fixture through adapter to `/ingest`.
3. Show resolved entities and stats in response.
4. Query graph/chat to prove persistence and grounding.
5. Show one provenance/receipt artifact.
6. Give partner quickstart: "send this payload, receive this response, verify with this command."

## Execution Plan (Mar 2-5)

### Mar 2
- Finalize this architecture note.
- Lock fixture schema and expected-output template.

### Mar 3
- Build fixture pack (3 cases) and run against live endpoint.
- Post Gate A scope lock; run Gate B contract checks.

### Mar 4
- Rehearse teach sequence with timer.
- Freeze prompts/payload mappings after Gate C.

### Mar 5
- Deliver live teach segment.
- Capture one partner commitment to wire their Summarizer against BKC contract.

## Non-Negotiables

- BKC remains protocol-neutral but quality-opinionated.
- No auto-ingest of unreviewed low-quality extraction.
- Every demo claim maps to a live check.
- Separate direct `/ingest` write path from staged commons-governance path in narrative.

## Success Criteria

By end of build day:
- One external collaborator can execute a valid payload to BKC `/ingest`.
- At least one fixture demonstrates contextual disambiguation value.
- The coalition can explain the Summarizer path as a reusable contract, not a one-off integration.

---

## Appendix: Code Paths and Function Signatures

Each pipeline stage references exact locations in the BKC codebase:

### Stage 1 — Capture
- **MacWhisper ingestion:** `darren-workflow/skills/meeting-notes/SKILL.md` — transcript extraction from `.whisper` files
- **Otter.ai ingestion:** via MCP `otter_*` tools
- **Attendee resolution:** Google Calendar + Gmail lookup (including spam folder for invite correlation)

### Stage 2 — Structured Extraction
- **Entity extraction with context:** `darren-workflow/skills/process-note/SKILL.md` — extracts entities with `associated_people`, `associated_organizations` per entity
- **Task extraction:** owner parsing, slug generation, backend registration via `POST /tasks/ingest`
- **Relationship frontmatter:** wikilink insertion with aliased links
- **Dual-signal quality evaluation:** `yonearth-gaia-chatbot/scripts/extract_kg_v3_2_2.py`
  - Signal 1: Text confidence (how explicitly stated in source)
  - Signal 2: Knowledge plausibility (world-knowledge consistency)
  - Conflict detection when signals disagree
  - Calibrated `p_true` score (0.0–1.0)

### Stage 3 — Resolution
- **Core resolver:** `RegenAI/koi-processor/api/personal_ingest_api.py:693-941`
  ```python
  async def resolve_entity(
      conn: asyncpg.Connection,
      entity: ExtractedEntity,
      context: Optional[ResolutionContext] = None
  ) -> Tuple[CanonicalEntity, bool]:
      """Resolve an entity against the knowledge base. Returns (CanonicalEntity, is_new)."""
  ```
  - Tier 1: Exact normalized match → confidence 1.0
  - Tier 1.1: Alias match (TEXT[] column) → confidence 1.0
  - Tier 1.5: Contextual co-occurrence + phonetic boost for Person → combined_score ≥ 0.6 (phonetic) / ≥ 0.75 (without)
  - Tier 2a: Fuzzy Jaro-Winkler + token overlap guard + length ratio → per-type thresholds: Person 0.92, Org 0.90, Practice 0.80
  - Tier 2b: Semantic embeddings via pgvector HNSW + OpenAI → per-type thresholds: Person 0.92, Concept 0.88
  - Tier 3: Create new entity with deterministic URI (`orn:{scope}.{type}:{slug}`)
- **Schema-driven config:** `RegenAI/koi-processor/api/entity_schema.py`
  ```python
  @dataclass
  class EntityTypeConfig:
      type_key: str; label: str; folder: str
      phonetic_matching: bool = False
      phonetic_stopwords: Set[str] = field(default_factory=set)
      type_aliases: List[str] = field(default_factory=list)
      min_context_people: int = 2
      similarity_threshold: float = 0.85   # Jaro-Winkler threshold (per-type: Person 0.92, Org 0.90)
      semantic_threshold: float = 0.92     # pgvector cosine threshold (per-type: Person 0.92, Concept 0.88)
      require_token_overlap: bool = True
  # Constants: MIN_TOKEN_OVERLAP_RATIO = 0.5, MIN_TOKEN_OVERLAP_COUNT = 2
  ```

### Stage 4 — Quality Gates
- **OpenAI availability check:** `personal_ingest_api.py:306`
  ```python
  def check_openai_availability() -> bool:
      """Check if OpenAI API key is configured"""
      return bool(OPENAI_API_KEY)
  ```
- **Pre-ingest validation helpers:**
  ```python
  def normalize_entity_text(text: str) -> str:
      """Normalize entity text for comparison (lowercase, strip, collapse whitespace)"""

  def passes_token_overlap_check(text1: str, text2: str, entity_type: str) -> bool:
      """Check if two texts pass the token overlap requirement for merge safety.
         Types with require_token_overlap=False bypass multi-word check,
         but single-word entities ALWAYS require JW >= 0.95."""
  ```
- **4-stage pipeline:** `Octo/koi-processor/` quality gate implementation
  - Confidence thresholding (per-type minimum `p_true`)
  - Entity-quality filtering: reject pronouns (8.6% of V4 issues), list targets (11.5%), vague entities (4.1%)
  - Duplicate handling via `document_entity_links` UNIQUE constraint
  - Bad merge detection + automatic alias maintenance

### Stage 5 — Ingest Contract
- **Contracted endpoint:** `RegenAI/koi-processor/api/personal_ingest_api.py:1645-1795`
  ```python
  @app.post("/ingest", response_model=IngestResponse)
  async def ingest_extraction(request: IngestRequest):
      """Ingest pre-extracted entities. Deduplicates, assigns canonical URIs, stores, returns resolved entities."""

  class IngestRequest(BaseModel):
      document_rid: str
      content: Optional[str] = None
      entities: List[ExtractedEntity]
      relationships: List[ExtractedRelationship] = []
      source: str = "obsidian-vault"
      context: Optional[ResolutionContext] = None

  class IngestResponse(BaseModel):
      success: bool
      canonical_entities: List[CanonicalEntity]
      receipt_rid: str
      stats: IngestStats  # entities_processed, new_entities, resolved_entities, failed_entities

  class ResolutionContext(BaseModel):
      associated_people: Optional[List[str]] = None
      project: Optional[str] = None
      organizations: Optional[List[str]] = None
      topics: Optional[List[str]] = None
  ```
  - Idempotent via `document_entity_links` UNIQUE constraint
  - Auth: `x-ingest-token` header
  - Required fields: `document_rid`, `source`, `entities[]`
  - Optional: `content`, `relationships[]`
  - Resolution context: `associated_people`, `organizations`, `topics` for disambiguation
- **Frozen contract doc:** `Octo/docs/integration/summarizer-ingest-contract.md`

### Stage 6 — Provenance + Federation
- **CAT receipts:** `orn:personal-koi.receipt:{uuid}` — generated per ingest operation
- **Stats response:** `entities_processed`, `new_entities`, `resolved_entities`, `failed_entities`
- **KOI-net federation:** ECDSA-signed envelopes, consent-gated cross-node sharing

### Stage 7 — Verification
- **Golden test infrastructure:** `RegenAI/koi-sensors/knowledge_graph/tests/test_golden.py`
  - F1 score target ≥ 0.80 for entity + statement extraction
  - Precision/recall calculations with normalization
  - Expected fixture structure: `golden/documents/` + `golden/expected/`
- **Bidirectional linking verification:** `POST /entities/mentioned-in` — batch query for entity backlinks
- **Post-run verification gate:** YAML validity, wikilink completeness, mentionedIn propagation, nested link detection

### Frontier (Not Yet Deployed)
- Pass 2.5 post-processing: pronoun resolution, list splitting, context enrichment (designed in V5 report, reduces quality issues from 26.8% → <5%)
- Per-source confidence baselines (transcripts vs web URLs vs meeting notes)
- Automated precision/recall reporting pipeline
- GraphRAG community detection layer (hierarchical abstraction)
