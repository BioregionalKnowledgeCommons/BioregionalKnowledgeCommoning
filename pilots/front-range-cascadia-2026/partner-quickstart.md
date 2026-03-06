# Partner Quickstart: Ingesting Data into BKC

*Get structured knowledge into the Bioregional Knowledge Commons in under 15 minutes.*

---

## Prerequisites

1. **Get an ingest token** — DM Darren (`@darrenzal`) on Telegram or Matrix
2. **Have `curl`** installed (macOS/Linux have it by default)
3. **Know your source identifier** — a short slug for your pipeline (e.g., `clawsmos-summarizer`, `nou-techne-watershed`)

---

## Your First Ingest

Paste this into your terminal, replacing `<YOUR_TOKEN>` with your token:

```bash
curl -X POST 'https://salishsee.life/commons/api/nodes/octo-salish-sea/ingest' \
  -H 'Content-Type: application/json' \
  -H 'x-ingest-token: <YOUR_TOKEN>' \
  -d '{
    "document_rid": "my-pipeline:test:001",
    "source": "my-pipeline",
    "entities": [
      {
        "name": "My Test Organization",
        "type": "Organization",
        "context": "A test entity to verify the ingest pipeline works"
      }
    ],
    "relationships": []
  }'
```

### What each field means

| Field | Required | Description |
|-------|----------|-------------|
| `document_rid` | Yes | Unique ID for this ingest event. Format: `<source>:<type>:<id>`. Provides partial idempotency — resubmitting the same `document_rid` prevents duplicate entity-link rows, but a fresh receipt is generated each call. See the [full contract](../../../Octo/docs/integration/summarizer-ingest-contract.md) §5 for retry semantics. |
| `source` | Yes | Your pipeline identifier. Used for provenance tracking. |
| `content` | No | Plain text summary (for future RAG indexing). |
| `entities` | Yes | Array of entities to add to the knowledge graph. |
| `entities[].name` | Yes | Display name of the entity. |
| `entities[].type` | Yes | One of the 15 entity types (see below). |
| `entities[].context` | No | Free-text description. Helps entity resolution disambiguate similar names. |
| `entities[].confidence` | No | 0.0–1.0. How confident your pipeline is about this extraction. Default: 1.0. |
| `relationships` | No | Array of relationships between entities (see below). |
| `relationships[].subject` | Yes | Name of the source entity (must match a `name` in `entities`). |
| `relationships[].predicate` | Yes | Relationship type (see predicate table below). |
| `relationships[].object` | Yes | Name of the target entity (must match a `name` in `entities`). |
| `relationships[].confidence` | No | 0.0–1.0. Default: 1.0. |

### Expected response (200 OK)

```json
{
  "success": true,
  "canonical_entities": [
    {
      "name": "My Test Organization",
      "uri": "orn:personal-koi.entity:organization-my-test-organization-<hash>",
      "type": "Organization",
      "is_new": true,
      "merged_with": null,
      "confidence": 1.0
    }
  ],
  "receipt_rid": "orn:personal-koi.receipt:<uuid>",
  "stats": {
    "entities_processed": 1,
    "new_entities": 1,
    "resolved_entities": 0,
    "relationships_processed": 0
  }
}
```

---

## Verify It Worked

Search for your entity by name:

```bash
curl -s 'https://salishsee.life/commons/api/nodes/octo-salish-sea/search?q=My+Test+Organization'
```

You should see your entity in the results with `"name": "My Test Organization"`.

---

## Full Schema Reference

See the complete contract with error codes, idempotency details, and failure modes:
[`summarizer-ingest-contract.md`](../../../Octo/docs/integration/summarizer-ingest-contract.md)

---

## Entity Types (15)

| Type | Description |
|------|-------------|
| `Person` | An individual (name, affiliation, role context) |
| `Organization` | A group, institution, DAO, or collective |
| `Project` | A specific initiative, tool, or deliverable |
| `Location` | A geographic place (city, watershed, monitoring station) |
| `Concept` | An idea, framework, term, or topic |
| `Meeting` | A meeting, session, call, or event |
| `Practice` | An ongoing method or activity specific to a bioregion |
| `Pattern` | A trans-bioregional generalization emerging from practices |
| `CaseStudy` | A documented real-world example of a practice or pattern |
| `Bioregion` | A named bioregion defined by ecological and cultural boundaries |
| `Protocol` | A general coordination pattern (not locality-specific) |
| `Playbook` | A local implementation of a protocol in a specific context |
| `Question` | An inquiry or hypothesis driving investigation |
| `Claim` | An assertion or conclusion |
| `Evidence` | Data, observations, or measurement results |

---

## Relationship Predicates (27)

### Base KOI (10)

| Predicate | Subject | Object | Example |
|-----------|---------|--------|---------|
| `affiliated_with` | Person/Org | Organization | Darren Zal → affiliated_with → BKC |
| `attended` | Person | Meeting | AG Neyer → attended → Build Day Mar 5 |
| `collaborates_with` | Person/Org | Person/Org | BKC → collaborates_with → Clawsmos |
| `founded` | Person | Organization | Kevin Owocki → founded → Gitcoin |
| `has_founder` | Organization | Person | Gitcoin → has_founder → Kevin Owocki |
| `has_project` | Organization | Project | BKC → has_project → A2A Agent Card |
| `involves_organization` | Meeting/Project | Organization | Build Day → involves_organization → Clawsmos |
| `involves_person` | Meeting/Project | Person | Build Day → involves_person → AG Neyer |
| `knows` | Person | Person | Tommy → knows → Darren Zal |
| `located_in` | Entity | Location/Bioregion | SNOTEL Station → located_in → Front Range |

### Knowledge Commoning (4)

| Predicate | Subject | Object | Example |
|-----------|---------|--------|---------|
| `aggregates_into` | Practice | Pattern | Watershed monitoring → aggregates_into → Ecological data commoning |
| `suggests` | Pattern | Practice | Commons governance → suggests → Steward review |
| `documents` | CaseStudy | Practice | Garry Oak Restoration Study → documents → Native plant restoration |
| `practiced_in` | Practice | Bioregion | Herring monitoring → practiced_in → Salish Sea |

### Discourse Graph (7)

| Predicate | Subject | Object | Example |
|-----------|---------|--------|---------|
| `supports` | Evidence/Claim | Claim | SWE data 2026 → supports → Snowpack decline claim |
| `opposes` | Evidence/Claim | Claim | Stream gauge reading → opposes → Drought severity claim |
| `informs` | Any | Any | Watershed monitoring → informs → Water allocation policy |
| `generates` | Any | Any | Boulder Summit 2026 → generates → Coalition charter |
| `implemented_by` | Protocol | Playbook | KOI-net → implemented_by → BKC Federation Playbook |
| `synthesizes` | Claim | Evidence | Water rights reform needed → synthesizes → Streamflow decline data |
| `about` | Any | Any | Snowpack decline claim → about → Colorado River Basin |

### SKOS + Hyphal (6)

| Predicate | Subject | Object | Example |
|-----------|---------|--------|---------|
| `broader` | Concept/Bioregion | Concept/Bioregion | Front Range → broader → Colorado River Basin |
| `narrower` | Concept/Bioregion | Concept/Bioregion | Salish Sea → narrower → Cowichan Valley |
| `related_to` | Any | Any | Knowledge commoning → related_to → Plurality |
| `forked_from` | Any | Any | BKC meta-protocol → forked_from → KOI-net protocol |
| `builds_on` | Any | Any | Cosmolocal production → builds_on → Commons-based peer production |
| `inspired_by` | Any | Any | Knowledge commoning → inspired_by → Elinor Ostrom's commons theory |

---

## Common Patterns

### Meeting transcript

```json
{
  "document_rid": "my-pipeline:meeting:standup-2026-03-05",
  "source": "my-pipeline",
  "content": "Weekly standup. Discussed watershed data aggregation progress.",
  "entities": [
    {"name": "Alice Chen", "type": "Person", "context": "Watershed data lead"},
    {"name": "Watershed Data Aggregator", "type": "Project"},
    {"name": "Weekly Standup Mar 5", "type": "Meeting"}
  ],
  "relationships": [
    {"subject": "Alice Chen", "predicate": "attended", "object": "Weekly Standup Mar 5"},
    {"subject": "Watershed Data Aggregator", "predicate": "involves_person", "object": "Alice Chen"}
  ]
}
```

### Project registration

```json
{
  "document_rid": "my-pipeline:project:river-monitor-v1",
  "source": "my-pipeline",
  "entities": [
    {"name": "River Monitoring Dashboard", "type": "Project", "context": "Real-time water quality dashboard for the Front Range"},
    {"name": "Front Range Water Coalition", "type": "Organization"},
    {"name": "Front Range", "type": "Bioregion"}
  ],
  "relationships": [
    {"subject": "Front Range Water Coalition", "predicate": "has_project", "object": "River Monitoring Dashboard"},
    {"subject": "River Monitoring Dashboard", "predicate": "located_in", "object": "Front Range"}
  ]
}
```

### Person onboarding

```json
{
  "document_rid": "my-pipeline:onboard:bob-smith-2026-03",
  "source": "my-pipeline",
  "entities": [
    {"name": "Bob Smith", "type": "Person", "context": "Ecologist, specializes in riparian restoration"},
    {"name": "Colorado State University", "type": "Organization"}
  ],
  "relationships": [
    {"subject": "Bob Smith", "predicate": "affiliated_with", "object": "Colorado State University"}
  ]
}
```

---

## FAQ

**Is it safe to retry a failed request?**
Yes, if you use the same `document_rid`. Idempotency is partial: entity names are deduplicated by name+type (submitting "Alice Chen" (Person) twice resolves to the same canonical URI), and `document_rid` prevents duplicate entity-link rows. However, a fresh `receipt_rid` is generated each call and the full resolution pipeline re-runs on retry. Retry on `502` (upstream unreachable). Do NOT retry on `400` or `401` (caller error).

**What happens if an entity already exists?**
BKC runs 3-tier entity resolution: exact name match, fuzzy match (Jaro-Winkler), then semantic match (OpenAI embeddings). If your entity matches an existing one, it resolves to the canonical URI (`is_new: false`). No duplicates are created.

**Is there a rate limit?**
No hard rate limit currently. Keep it under ~10 requests/minute during build day. For bulk ingests, batch entities into a single request (the `entities` array can hold many items).

**What if I submit the wrong entity type?**
The API accepts any of the 15 types listed above. Invalid types will be rejected with a `400` error. You can correct it by submitting again with the right type and same `document_rid`.

**Can I target a different node?**
Yes — replace `octo-salish-sea` in the URL with the node slug:
- `octo-salish-sea` — Salish Sea coordinator
- `front-range` — Front Range node
- `greater-victoria` — Greater Victoria node

**What is `receipt_rid`?**
A provenance receipt for audit. It's a fresh UUID per call (not stable across retries). Use it for logging, not for deduplication.

**How do I delete an entity I created by mistake?**
Contact Darren. There is no self-service delete endpoint. Entities can be manually removed from the graph by a steward.
