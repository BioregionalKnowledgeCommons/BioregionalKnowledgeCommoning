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

## Moment 2: Routing Suggestion + Steward Approval

**Setup**: Commitment exists in PROPOSED state. Two pools seeded with different bioregions, need tags, and capacity.

**Action**: `suggest_pool_routes` (MCP) or `POST /commitments/routing-suggestions` (API) with the commitment payload.

**Response**:

```json
{
  "suggestions": [
    {
      "pool_rid": "orn:koi-net.commitment-pool:victoria-landscape-hub-restoration-pool+...",
      "pool_name": "Victoria Landscape Hub Restoration Pool",
      "total_score": 85,
      "score_breakdown": {
        "same_bioregion": 30,
        "offer_need_overlap": 25,
        "timeframe_overlap": 15,
        "capacity_fit": 15,
        "governance_compat": 0
      },
      "hard_excludes": [],
      "recommended": true,
      "explanation": "Same bioregion (Salish Sea), strong taxonomy match (restoration + native-plants), within pool capacity, overlapping timeframe."
    },
    {
      "pool_rid": "orn:koi-net.commitment-pool:cascadia-bioregion-stewardship-pool+...",
      "pool_name": "Cascadia Bioregion Stewardship Pool",
      "total_score": 55,
      "score_breakdown": {
        "same_bioregion": 15,
        "offer_need_overlap": 15,
        "timeframe_overlap": 15,
        "capacity_fit": 10,
        "governance_compat": 0
      },
      "hard_excludes": [],
      "recommended": false,
      "explanation": "Umbrella bioregion match (Cascadia > Salish Sea), partial taxonomy overlap (stewardship), within capacity."
    }
  ]
}
```

**Steward workflow** (web UI at `/commons/commitments`):
1. See pending PROPOSED commitments
2. Click commitment → see routing suggestions with score breakdowns
3. Approve → `PATCH /commitments/{rid}/state` (PROPOSED → VERIFIED)
4. Select pool → `POST /pools/{rid}/pledge`
5. If pool activation threshold reached → pool auto-transitions to "active"

**What viewer sees**: Transparent routing scores. Steward reviews and decides — the scorer suggests, humans approve. Trust through witnessed governance.

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
| Regenerate Cascadia | 200h native plant restoration | $8K | restoration, native-plants, labor | Victoria (85), Cascadia (55) |
| Kinship Earth | Soil monitoring equipment loan | $3K | monitoring, equipment, soil-health | Victoria (70), Cascadia (40) |
| Mycopunks | Mycoremediation pilot — 40h | $2K | mycoremediation, restoration, fungi | Victoria (65), Cascadia (50) |

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

- Pending commitments list (filterable by state)
- Click commitment → detail panel with:
  - Commitment fields
  - Routing suggestions with score breakdowns
  - Approve / Reject buttons
  - Pool pledge selector
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

- [ ] `seed-commitment-demo.sh` creates 2 pools + 3 commitments on Octo
- [ ] `POST /commitments/routing-suggestions` returns scored results for seeded data
- [ ] Empty suggestion set returns `{"suggestions": []}`
- [ ] Deterministic tie-break by `pool_rid` alphabetical
- [ ] Web form at `/commons/commit` submits commitment via BFF
- [ ] Review dashboard shows pending commitments with routing suggestions
- [ ] Steward approve → VERIFIED state transition
- [ ] Non-steward approve → 403
- [ ] Unauthenticated approve → 401
- [ ] Pool pledge + threshold check works
- [ ] MCP `draft_commitment_from_text` returns draft (not persisted)
- [ ] MCP `suggest_pool_routes` returns locked response shape
- [ ] Demo works fully without live Celo connection
- [ ] (Stretch) One Alfajores pool state fetch
- [ ] (Stretch) One testnet attestation + tx_hash in proof pack
