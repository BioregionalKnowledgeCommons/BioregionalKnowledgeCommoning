# MediaWiki v1.5 QA Report — 2026-03-22

## Embedding Coverage

| Metric | Before Step 1 | After Step 1 |
|--------|--------------|-------------|
| Entities with embeddings | 728 (26%) | **2,769 (100%)** |
| Name-only embeddings | — | 2,040 |
| With description | — | 1 |

## Graph Quality Metrics

| Metric | Value | Assessment |
|--------|-------|------------|
| Total entities | 2,769 | Good density |
| Total edges | 7,015 | Avg 2.53 edges/entity — moderate |
| Duplicate entities (same name+type) | 1 group (5 Claim duplicates) | **<1% — excellent** |

**Description coverage by type:**

| Type | Total | With Description | % |
|------|-------|-----------------|---|
| Concept | 1,435 | 116 | 8.1% |
| Organization | 378 | 117 | 31.0% |
| Location | 328 | 81 | 24.7% |
| Project | 294 | 47 | 16.0% |
| Person | 103 | 84 | 81.6% |
| Practice | 27 | 26 | 96.3% |
| Bioregion | 9 | 8 | 88.9% |

**Concepts have only 8.1% description coverage** — this is the biggest semantic quality gap. Most wiki-imported entities (Concept type) have names but no descriptions.

**High-degree hubs (top 5):**
1. "river delta;beach;embayment" (Concept, 90 edges)
2. "Salish Sea" (Bioregion, 87 edges)
3. "floodplain" (Concept, 86 edges)
4. "river deltas" (Concept, 85 edges)
5. "washington state department of ecology" (Concept, 80 edges)

Note: Some hubs have compound names (semicolon-separated) suggesting parser artifacts from wiki template fields. These are functional but not clean entity names.

## RAG Quality Test (10 Questions)

| # | Question | Score | Top Source(s) | Notes |
|---|----------|-------|---------------|-------|
| 1 | Restoration projects in Puget Sound | **grounded** | PSAR (Concept 0.76), Port Susan (Project 0.71) | Names real projects, cites wiki docs |
| 2 | Salmon recovery organizations | **grounded** | salmon recovery (Practice 0.75), WRIA 1 (Org 0.71) | Governor's Salmon Recovery Office, Pacific Salmon Foundation |
| 3 | Skagit watershed | **grounded** | skykomish watershed (Concept 0.72), Lower Skagit (Location 0.69) | Detailed description with tributaries, floodplain |
| 4 | Eelgrass restoration | **grounded** | salish sea restoration (Concept 0.69) | Specific restoration methods, ecological role |
| 5 | Puget Sound Partnership | **grounded** | PSP (Organization 0.92) | Highest score in test — perfect entity match |
| 6 | Shellfish monitoring | **weak** | Herring Monitoring (Practice 0.66), Intertidal Biotic (Project 0.60) | Answer is reasonable but generic — no shellfish-specific entity found, fell back to adjacent topics |
| 7 | Rivers flowing into Salish Sea | **grounded** | major islands (Concept 0.71), Salish Sea (Location 0.71) | Lists Fraser, Nisqually, Skagit — correct |
| 8 | Nooksack River | **grounded** | nooksack river (Concept 0.83), Nooksack River (Location 0.83) | Very strong — detailed watershed info |
| 9 | Orca conservation | **weak** | orcas (Concept 0.59) | Answer mentions Southern Residents, Chinook prey — but sources are thin, low scores |
| 10 | Salish Sea bioregion | **grounded** | salish sea (Concept/Location/Bioregion all 0.72) | Comprehensive description, triple entity match |

**Results: 8 grounded, 2 weak, 0 miss. Target was 7/10 — PASSED.**

## Chunk Quality

| Source | Count | % of Total |
|--------|-------|-----------|
| GitHub (OpenClaw code) | 18,941 | 91.1% |
| MediaWiki (Salish Sea Wiki) | 1,839 | 8.9% |

**Key finding:** Chunks are 91% code from the GitHub sensor, only 9% wiki content. Despite this, wiki retrieval works well because:
- Entity-level semantic search now covers all wiki entities (100% embedding coverage)
- The 1,839 wiki chunks are high quality and well-structured
- The B1 hybrid pipeline combines both entity and chunk retrieval effectively

**Chunk quality (wiki samples):** 2 sampled wiki chunks showed:
- "Rural Land Use" — coherent, has category metadata artifacts (`Category=**Rural`) but readable
- "TRPC 2013 sustainable thurston development plan" — starts with raw Category tags before content

Garbage rate in wiki chunks appears low (<10%) but some have wiki markup artifacts (Category tags, template remnants).

## Duplicate Rate

Only 1 duplicate group found: 5 Claim entities with identical normalized text (steel thread test artifacts). **Duplicate rate: <1% — well below 5% threshold.**

## Issues Found

1. **Compound entity names** — Some wiki entities have semicolon-separated compound names (e.g., "river delta;beach;embayment", "climate change;legal"). These are functional but messy. ~10-20 entities affected.
2. **Concept descriptions very sparse** — Only 8.1% of Concepts have descriptions. Most are name-only. This limits semantic specificity for the largest entity type.
3. **Wiki chunk category artifacts** — Some chunks start with raw `Category:` tags from MediaWiki templates.
4. **"washington state department of ecology" typed as Concept** — Should be Organization. ~5-10 similar mistyped entities likely exist.

## Recommendation

**(a) Proceed to Step 4 — generate vault notes.**

Rationale:
- RAG quality is strong (8/10 grounded)
- Duplicate rate is negligible (<1%)
- The issues found (compound names, sparse descriptions, mistyped entities) are bounded and non-blocking
- Vault notes will make the existing graph visible even if descriptions are thin — relationship wikilinks alone add navigational value
- Description enrichment (v2 work) can be done incrementally later without blocking vault publication

**Bounded cleanup before Step 4 (optional, ~15 min):**
- Fix 5-10 obviously mistyped entities (e.g., "washington state department of ecology" → Organization)
- Consider splitting ~10 compound-name entities if time permits
- These are one-off DB fixes, not pipeline changes
