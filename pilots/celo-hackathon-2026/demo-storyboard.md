# Demo Storyboard — Agentic Commitment Routing

## Cutline

| Tier | Scope | Celo dependency |
|------|-------|-----------------|
| **Must-have** | Seed data + routing scorer + web form + steward review | None |
| **Should-have** | MCP draft tool + pool activation + routing viz | None |
| **Stretch** | Read-only Celo pool state + one Alfajores attestation | Alfajores testnet |

---

## Moment 1: Agent Drafts Commitment from Natural Language

**Setup**: Claude Code with personal-koi-mcp connected to Octo node.

**Action**: User types natural language describing a community commitment:

> "Regenerate Cascadia offers 200 hours of native plant restoration in the Salish Sea bioregion, valued at $8,000, April through September 2026. They want soil testing equipment access and volunteer coordination support. Limit: max 3 concurrent restoration sites."

**MCP tool** `draft_commitment_from_text` parses this into a structured draft:

```json
{
  "pledger_uri": "orn:koi-net.entity:regenerate-cascadia+...",
  "title": "Native plant restoration — 200 hours",
  "offer_type": "stewardship",
  "quantity": 200,
  "unit": "hours",
  "validity_start": "2026-04-01",
  "validity_end": "2026-09-30",
  "metadata": {
    "wants": ["soil testing equipment access", "volunteer coordination support"],
    "limits": ["max 3 concurrent restoration sites"],
    "bioregion_uri": "orn:koi-net.entity:salish-sea+...",
    "estimated_value_usd": 8000,
    "routing_tags": ["restoration", "native-plants", "labor"]
  }
}
```

**Key point**: Draft is NOT persisted. Human reviews, edits if needed, then confirms → `POST /commitments/create`.

**Alt path (web)**: Same payload submitted via structured form at `/commons/commit`. Both paths produce identical `CommitmentCreateRequest` objects.

**What viewer sees**: Natural language → structured commitment with typed offers, wants, limits. Agent makes the ancient coordination pattern (Mweria, Meitheal) legible.

---

## Moment 2: Three Orthogonal Operations — Route, Pledge, Verify

**Setup**: Commitment exists in PROPOSED state. Two pools seeded with different bioregions, need tags, and capacity.

**Key governance principle**: These are three independent operations, not a linear pipeline. A commitment can be pledged to a pool while still PROPOSED. A commitment can be VERIFIED without being in any pool. The operations compose freely.

### 2a: Route — Scorer Suggests Pool Matches

**Action**: `suggest_pool_routes` (MCP) or `POST /commitments/routing-suggestions` (API) with the commitment payload.

**Response**:

```json
{
  "suggestions": [
    {
      "pool_rid": "orn:koi-net.commitment-pool:victoria-landscape-hub-restoration-pool+...",
      "pool_name": "Victoria Landscape Hub Restoration Pool",
      "total_score": 68,
      "score_breakdown": {
        "same_bioregion": 30,
        "offer_need_overlap": 18,
        "timeframe_overlap": 10,
        "capacity_fit": 10,
        "governance_compat": 0
      },
      "hard_excludes": [],
      "recommended": true,
      "explanation": "Same bioregion (Salish Sea), strong taxonomy match (restoration + native-plants), within pool capacity, overlapping timeframe."
    },
    {
      "pool_rid": "orn:koi-net.commitment-pool:cascadia-bioregion-stewardship-pool+...",
      "pool_name": "Cascadia Bioregion Stewardship Pool",
      "total_score": 32,
      "score_breakdown": {
        "same_bioregion": 15,
        "offer_need_overlap": 7,
        "timeframe_overlap": 10,
        "capacity_fit": 0,
        "governance_compat": 0
      },
      "hard_excludes": [],
      "recommended": false,
      "explanation": "Umbrella bioregion match (Cascadia > Salish Sea), partial taxonomy overlap (stewardship), within capacity."
    }
  ]
}
```

### 2b: Pledge — Pool Curation (Independent of Verification)

**Action**: Steward selects a pool → `POST /pools/{rid}/pledge`

Pledging is pool curation: "this commitment belongs in our pool." A commitment can be pledged while still PROPOSED — the pool steward is saying "we want this," not "we've verified it." Declining a pledge is implicit (not pledged). In hackathon MVP, this is single-pool; multi-pool pledging is a post-hackathon extension.

If pool activation threshold reached → pool auto-transitions to "active."

### 2c: Verify — Trust Attestation (Independent of Pledge)

**Action**: Steward or peer attests → `PATCH /commitments/{rid}/state` (PROPOSED → VERIFIED)

Verification is an optional trust signal: "we believe this pledger can deliver." A commitment can be VERIFIED without being in any pool (verified but uncurated), or pledged to a pool without being verified (curated but unverified). Trust emerges from witnessed follow-through, not pre-approval.

### Steward workflow (web UI at `/commons/commitments`):
1. See commitments (filterable by state, pool membership)
2. Click commitment → detail panel with routing suggestions and score breakdowns
3. Pledge to pool (pool curation) — independent action
4. Verify commitment (trust attestation) — independent action
5. Pool status cards (pledge count, threshold progress, activation state)

**What viewer sees**: Three independent operations composed by stewards, not a single approval gate. The scorer suggests pools; stewards curate; peers verify. Anyone can make a promise — the question is which pools accept it.

---

## Moment 3: Proof + Settlement

### Must-have path (BKC-native)

1. Commitment advances through lifecycle: VERIFIED → ACTIVE → EVIDENCE_LINKED
2. Evidence entity linked via `POST /commitments/{rid}/link-evidence`
3. Proof of fulfillment documented in knowledge graph
4. State transitions logged in insert-only audit trail

### Should-have path (TBFF integration)

1. Settlement triggers `POST /claims/claim-from-settlement`
2. Threshold policy auto-advances based on value band
3. Receipt chain links settlement back to original commitment
4. Proof pack assembled: commitment + evidence + attestations + anchor

### Stretch path (Celo)

1. Pool activation threshold reached
2. One attestation recorded on Alfajores testnet
3. `tx_hash` recorded in proof pack
4. Viewer sees: BKC provenance + on-chain attestation in single artifact

**What viewer sees**: The full loop — sensing → committing → coordinating → proving → learning. Ancient patterns made legible in a federated knowledge graph, with optional on-chain provenance.

---

## Seeded Demo Data

### Pools (2)

| Pool | Bioregion | Threshold | Need Tags | Capacity |
|------|-----------|-----------|-----------|----------|
| Victoria Landscape Hub Restoration Pool | Salish Sea | $15K | restoration, native-plants, monitoring | $50K |
| Cascadia Bioregion Stewardship Pool | Cascadia | $25K | stewardship, watershed, community | $100K |

### Commitments (3-5)

| Pledger | Offer | Value | Tags | Pool match |
|---------|-------|-------|------|------------|
| Regenerate Cascadia | 200h native plant restoration | $8K | restoration, native-plants, labor | Victoria (68), Cascadia (32) |
| Kinship Earth | Soil monitoring equipment loan | $3K | monitoring, equipment, soil-health | Victoria (68), Cascadia (32) |
| Mycopunks | Mycoremediation pilot — 40h | $2K | mycoremediation, restoration, fungi | Victoria (68), Cascadia (32) |

### Existing Entities (already seeded)

- Victoria Landscape Hub, Regenerate Cascadia, Kinship Earth, Mycopunks (Organizations)
- Cascadia (Bioregion), Greater Victoria (Location)
- Salish Sea (Bioregion — to be confirmed/seeded if missing)

---

## Routing Scorer v0

| Factor | Weight | Logic |
|--------|--------|-------|
| Same bioregion | +30 | Exact `bioregion_uri` match between commitment and pool |
| Umbrella bioregion | +15 | Parent match via `broader` predicate in entity graph |
| Offer/need overlap | +25 | `routing_tags` ∩ pool `need_tags` / max(len) |
| Timeframe overlap | +15 | Date range intersection / commitment range |
| Capacity fit | +20 | `estimated_value_usd` fits pool `remaining_capacity_usd` |
| Governance compat | +10 | Same `governance_membrane`. **Inactive in v0** (returns 0). |
| **Hard excludes** | reject | No remaining capacity, outside timeframe entirely |

Score range: 0-105 (governance inactive). Top-K sorted by `total_score`, deterministic tie-break by `pool_rid` alphabetical.

---

## Web Pages

### `/commons/commit` — Commitment Form

Structured form with fields:
- Pledger (searchable org selector, default: show existing Victoria orgs)
- Title, description
- Offer type (labor / goods / service / knowledge / stewardship)
- Quantity + unit
- Validity dates
- Estimated value (USD)
- Wants (multi-input)
- Limits (multi-input)
- Routing tags (multi-input, suggest from pool need tags)
- Bioregion (selector from seeded bioregions)

Submit → `POST /commitments/create` via BFF → show routing suggestions inline.

### `/commons/commitments` — Review Dashboard (steward-protected)

- Commitments list (filterable by state, pool membership)
- Click commitment → detail panel with:
  - Commitment fields
  - Routing suggestions with score breakdowns
  - Pledge to Pool button (pool curation — independent of verification)
  - Verify button (trust attestation — independent of pledge)
- Pool status cards (pledge count, threshold progress, activation state)

---

## Build Sequence

| Day | Task | Owner | Depends on |
|-----|------|-------|------------|
| 1 | Seed demo data (`seed-commitment-demo.sh`) | Darren | Nothing |
| 1-2 | `POST /commitments/routing-suggestions` endpoint | Darren | Seed data (for testing) |
| 2-3 | BFF routes (commitments + routing + state + pledge) | Darren | Routing endpoint |
| 2-4 | `/commons/commit` form page | Benjamin | BFF routes |
| 3-4 | `/commons/commitments` review dashboard | Benjamin | BFF routes |
| 3-5 | MCP tools (`draft_commitment_from_text`, `suggest_pool_routes`) | Darren | Routing endpoint |
| 4-5 | Routing viz (adapt FlowCanvas) | Benjamin | Review dashboard |
| 5-8 | Celo adapter (stretch) | Darren | Core flow complete |
| 8-10 | Demo recording + submission narratives | Both | Everything |

---

## Verification Checklist

- [x] `seed-commitment-demo.sh` creates 2 pools + 3 commitments on Octo
- [x] `POST /commitments/routing-suggestions` returns scored results for seeded data (Victoria=68, Cascadia=32)
- [ ] Empty suggestion set returns `{"suggestions": []}`
- [ ] Deterministic tie-break by `pool_rid` alphabetical
- [x] Web form at `/commons/commit` submits commitment via BFF
- [x] Review dashboard shows commitments with routing suggestions
- [x] Steward pledge to pool works (independent of verification)
- [x] Steward verify works (independent of pool pledge)
- [ ] Non-steward pledge/verify → 403
- [x] Unauthenticated pledge/verify → 401
- [ ] Pool activation threshold check works on pledge
- [x] MCP `draft_commitment_from_text` returns draft (not persisted)
- [x] MCP `suggest_pool_routes` returns locked response shape
- [x] Demo works fully without live Celo connection
- [x] Passkey sign-in → Check Routes → Pledge → Verify full flow verified (manual, 2026-03-13)
- [ ] (Stretch) One Alfajores pool state fetch
- [ ] (Stretch) One testnet attestation + tx_hash in proof pack
