# MVIS Operator Runbook

**Audience:** Technical operator running the MVIS intent registry for the Cascadia pilot. Coordinator-facing steps are marked **[Coordinator]**; node-operator diagnostics are marked **[Ops]**.

**First cohort:** Run as a single compressed cycle (one day), not the weekly cadence. The weekly cadence below is the target for ongoing operations once the first cohort validates the workflow.

**API base URL:** `http://localhost:8351`

---

## 1. Preflight Checks

**[Ops]** Run before each operating cycle.

```bash
# Backend health
curl -sf localhost:8351/health | python3 -m json.tool

# Intent tables accessible
curl -sf localhost:8351/intents/stats | python3 -m json.tool

# Landscape groups present
curl -sf localhost:8351/intents/groups | python3 -c "import sys,json; groups=json.load(sys.stdin); print(f'{len(groups)} groups loaded')"

# Vocabulary loaded
curl -sf localhost:8351/intents/vocabulary | python3 -c "import sys,json; v=json.load(sys.stdin); print(f'{len(v)} vocab items')"
```

**[Ops]** Federation check (if NUC is a peer):
```bash
ssh dobby "psql -d personal_koi -c 'SELECT count(*) FROM intent_discovery_cache;'"
```

**Pass criteria:** All endpoints return valid JSON. Group count >= 10. Vocabulary includes the asset keys you'll use.

---

## 2. Normalize Vocabulary with Coordinator

**[Coordinator + Ops]** Before the first cohort, review the controlled vocabulary with the coordinator.

```bash
curl -sf localhost:8351/intents/vocabulary | python3 -m json.tool
```

Matching is **exact on `asset_key`** — if a scribe enters `soil_monitor` but the vocabulary has `soil_monitoring`, matching will fail silently. Agree on exact keys before ingest.

**Adding vocabulary mid-session is an exception, not the norm.** If a new asset type surfaces during a live cohort, add it, but capture it in the after-action memo as a vocabulary miss.

```bash
# Add a new vocabulary item (exception-only during live cohort)
curl -s -X POST localhost:8351/intents/vocabulary \
  -H "Content-Type: application/json" \
  -d '{"assetKey":"new_asset","displayName":"New Asset","category":"category"}'
```

---

## 3. Ingest Drafts

**[Coordinator]** After a workshop or from scribe notes. Each intent starts as `draft`.

```bash
curl -s -X POST localhost:8351/intents/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "intentKey": "unique-key-for-this-intent",
    "intentType": "OFFER",
    "publisherName": "Sarah Chen",
    "publisherContact": "sarah@example.org",
    "landscapeGroup": "olympic_peninsula",
    "assetOffered": "restoration_labor",
    "quantity": "200 hours",
    "description": "Field crew available April-September",
    "captureMethod": "manual",
    "enteredBy": "scribe-name"
  }'
```

**Intent types:** `OFFER` (has asset_offered), `WANT` (has asset_wanted), `SWAP` (has both).

**Key rules:**
- `intentKey` must be unique — use a descriptive slug like `sarah-offer-restoration-2026q2`
- `assetOffered` / `assetWanted` must exactly match a vocabulary `asset_key`
- All intents start as `draft` — nothing is visible in discovery or matching until reviewed

---

## 4. Review and Promote

**[Coordinator]** Review all drafts for your landscape group, then promote approved ones.

```bash
# List drafts for your group
curl -sf "localhost:8351/intents/detail?status=draft&landscape_group=olympic_peninsula" | python3 -m json.tool

# Promote a draft to active
curl -s -X POST "localhost:8351/intents/sarah-offer-restoration-2026q2/review" \
  -H "Content-Type: application/json" \
  -d '{"reviewedBy": "coordinator-name"}'

# Verify it appears in discovery
curl -sf "localhost:8351/intents/?landscape_group=olympic_peninsula" | python3 -m json.tool
```

The `draft → active` transition is the quality gate. Once active, the intent is visible in matching and (if `visibility: "regional"`) in federation.

---

## 5. Run Matching

**[Ops]** Run after all intended intents are promoted to active.

```bash
# Local-only matching (first cohort default)
curl -s -X POST localhost:8351/intents/match \
  -H "Content-Type: application/json" \
  -d '{"landscapeGroup": "olympic_peninsula"}' | python3 -m json.tool

# Cross-landscape matching (subsequent cohorts, when multiple groups have active intents)
# curl -s -X POST localhost:8351/intents/match \
#   -H "Content-Type: application/json" \
#   -d '{"landscapeGroup": "olympic_peninsula", "includeRegional": true}' | python3 -m json.tool
```

**First cohort: run local-only.** The `includeRegional` flag defaults to `false`. Cross-landscape matching is for later cohorts once multiple landscape groups have active intents with `visibility: "regional"`.

Each returned proposal has `offer_intent_rid`, `want_intent_rid`, `score`, and `status: "candidate"`.

---

## 6. Generate Coordinator Digest

**[Ops → Coordinator]** Generate and send to the coordinator.

```bash
curl -sf "localhost:8351/intents/digest/olympic_peninsula" | python3 -m json.tool
```

**Response format:** JSON with a `digest` field containing a markdown string. Copy the `digest` value and send to the coordinator via email/Slack/etc. The digest includes:
- **Local matches** with contact info and descriptions
- **Cross-landscape opportunities** (if any regional intents exist)
- **Unmet needs** — active WANTs with no matching OFFERs
- **Stale intents** — intents approaching decay floor

The digest uses `IntentCoordinatorResponse` format, which includes publisher contact info. Participants never see this view.

---

## 7. Follow Up on Proposals

**[Coordinator]** After introductions, update proposal status.

```bash
# List current proposals
curl -sf localhost:8351/intents/proposals | python3 -m json.tool

# After introducing parties
curl -s -X PATCH "localhost:8351/intents/proposals/<proposal_rid>" \
  -H "Content-Type: application/json" \
  -d '{"status": "introduced"}'

# After both parties confirm
curl -s -X PATCH "localhost:8351/intents/proposals/<proposal_rid>" \
  -H "Content-Type: application/json" \
  -d '{"status": "accepted", "resolvedBy": "coordinator-name"}'
# → Both intents auto-transition to "fulfilled"

# If one party declines
curl -s -X PATCH "localhost:8351/intents/proposals/<proposal_rid>" \
  -H "Content-Type: application/json" \
  -d '{"status": "declined", "resolvedBy": "coordinator-name"}'
# → Intents stay "active" for future matching
```

---

## 8. Refresh / Archive

**[Coordinator]** End-of-cycle maintenance.

```bash
# Refresh a still-valid intent (resets priority to 100)
curl -s -X POST "localhost:8351/intents/sarah-offer-restoration-2026q2/refresh"

# Archive a withdrawn intent
curl -s -X PATCH "localhost:8351/intents/sarah-offer-restoration-2026q2" \
  -H "Content-Type: application/json" \
  -d '{"status": "archived"}'
```

---

## 9. Troubleshooting

**[Ops]**

| Symptom | Check |
|---------|-------|
| Backend won't start | `cat ~/.config/personal-koi/koi-server.log` on NUC; `bash ~/.config/personal-koi/start.sh` |
| Matching returns empty | Verify intents are `active` (not `draft`), same `landscape_group`, OFFER/WANT use same `asset_key` |
| Digest missing matches | Matching must be run first (`POST /intents/match`); digest reads existing proposals |
| Federation cache empty | `ssh dobby "psql -d personal_koi -c 'SELECT * FROM intent_discovery_cache LIMIT 5;'"` |
| Federation handler errors | See `docs/foundations/koi-federation-operations-runbook.md` |

---

## Target Weekly Cadence (after first cohort validates)

| Day | Activity |
|-----|----------|
| Monday | Ingest and review new intents from workshop/scribe notes |
| Tuesday | Run matching and send coordinator digest |
| Wednesday–Thursday | Coordinator introductions and follow-up |
| Friday | Refresh/archive stale intents; verify federation health |
