#!/usr/bin/env bash
# seed-build-day-entities.sh
# Priority 2: Build day community entity seeding for BKC knowledge graph
# Cutoff: Mar 3, 2026, before Gate A (12:00 PM MT)
#
# USAGE:
#   TOKEN=your-ingest-token bash seed-build-day-entities.sh
#
# Rollback: If any entity causes issues, find its URI in the log file
# and remove via the admin API or SSH to the server.

# Note: -e intentionally omitted — ingest errors are reported and script continues
set -uo pipefail

BASE_URL="https://45.132.245.30.sslip.io"
TOKEN="${TOKEN:-}"

if [[ -z "$TOKEN" ]]; then
  echo "ERROR: TOKEN env var must be set (x-ingest-token value)"
  echo "  TOKEN=your-token bash $0"
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG="seeded-uris-${TIMESTAMP}.log"
INGEST_FAILURES=0
echo "# Seeded entity URIs — ${TIMESTAMP}" > "$LOG"
echo "URI	Name	IsNew" >> "$LOG"

urlencode() {
  python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1"
}

search_node() {
  local node="$1" query="$2"
  local encoded
  encoded=$(urlencode "$query")
  echo "  [search] $node ← '$query'"
  curl -sf "$BASE_URL/commons/api/nodes/$node/search?q=$encoded" \
    | python3 -c "
import sys, json
data = json.load(sys.stdin)
hits = data.get('results', data.get('entities', []))
if hits:
    for h in hits[:3]:
        print(f\"    FOUND: {h.get('uri','?')} ({h.get('name','?')}) [{h.get('type','?')}]\")
else:
    print('    NOT FOUND — will be created')
" 2>/dev/null || echo "    (search unavailable or empty)"
}

ingest_node() {
  local node="$1" payload="$2"
  echo "  [ingest] → $node"

  # Capture body and HTTP status separately so errors are always visible
  local http_code body tmpfile
  tmpfile=$(mktemp)
  http_code=$(curl -s -o "$tmpfile" -w "%{http_code}" \
    -X POST "$BASE_URL/commons/api/nodes/$node/ingest" \
    -H "Content-Type: application/json" \
    -H "x-ingest-token: $TOKEN" \
    -d "$payload")
  body=$(cat "$tmpfile")
  rm -f "$tmpfile"

  if [[ "$http_code" != "200" ]]; then
    echo "  ✗ ERROR: HTTP $http_code from node '$node'"
    echo "  Response body: $body"
    echo "  → Fix the error above before proceeding. Common causes:"
    echo "    401 = wrong/missing TOKEN"
    echo "    400 = malformed payload or missing 'source' field"
    echo "    502 = KOI backend unreachable (SSH to server, check systemctl status koi-api)"
    echo "    503 = BFF_INGEST_TOKEN not configured on server"
    return 1
  fi

  echo "  ✓ HTTP $http_code"
  echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"

  # Log URIs for rollback
  echo "$body" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for e in data.get('canonical_entities', []):
    print(f\"    URI: {e['uri']}  is_new={e['is_new']}  name={e['name']}\")
    with open('$LOG', 'a') as f:
        f.write(f\"{e['uri']}\t{e['name']}\t{e['is_new']}\n\")
stats = data.get('stats', {})
print(f\"    stats: {stats.get('entities_processed',0)} processed, {stats.get('new_entities',0)} new, {stats.get('resolved_entities',0)} resolved\")
" 2>/dev/null || echo "  (could not parse response for URI logging)"
}

echo "=========================================="
echo " BKC Build Day Entity Seeding"
echo " $(date)"
echo " Log: $LOG"
echo "=========================================="
echo ""

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1: Dedupe checks (informational — ingest handles dedup server-side too)
# ─────────────────────────────────────────────────────────────────────────────
echo "━━━ Step 1: Dedupe checks ━━━"
echo ""
echo "Checking Octo (Salish Sea) node..."
search_node "octo-salish-sea" "Kevin Owocki"
search_node "octo-salish-sea" "Clawsmos"
search_node "octo-salish-sea" "Lucian"
echo ""
echo "Checking Front Range node..."
search_node "front-range" "Clawsmos"
search_node "front-range" "Todd Youngblood"
echo ""
echo "Review above — any FOUND entities will be resolved/merged on ingest (not duplicated)."
echo "Press Enter to continue, Ctrl-C to abort."
read -r

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2: Seed Octo (Salish Sea) node
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "━━━ Step 2: Seed Octo (Salish Sea) node ━━━"
echo ""

ingest_node "octo-salish-sea" '{
  "document_rid": "bkc:seed:build-day-community-octo:2026-03-03",
  "source": "bkc-steward-seed",
  "content": "Build day community entity seeding. Key participants in the bioregional AI swarms coalition for the Mar 5, 2026 build day.",
  "entities": [
    {
      "name": "Kevin Owocki",
      "type": "Person",
      "context": "Co-founder of Gitcoin, public goods funding pioneer, promoting bioregional AI swarms, owockibot treasury designer",
      "confidence": 1.0
    },
    {
      "name": "Gitcoin",
      "type": "Organization",
      "context": "Public goods funding platform. Gitcoin Grants (GG) rounds including GG25-29. Home of owockibot treasury.",
      "confidence": 1.0
    },
    {
      "name": "owockibot",
      "type": "Organization",
      "context": "AI treasury bot with bounded authority for public goods allocation. Designed by owocki. Bounded authority: auto under $500, multisig for larger amounts.",
      "confidence": 0.95
    },
    {
      "name": "Benjamin Life",
      "type": "Person",
      "context": "Bioregional governance researcher. Author of The Infrastructure of Belonging article on cyber-physical commons.",
      "confidence": 0.95
    },
    {
      "name": "AG Neyer",
      "type": "Person",
      "context": "Clawsmos co-founder, agent-native coordination infrastructure builder, Summarizer/Orchestrator/Moderator/Representative agent architecture",
      "confidence": 1.0
    },
    {
      "name": "Clawsmos",
      "type": "Organization",
      "context": "Agent-native coordination layer. Matrix rooms with Summarizer, Orchestrator, Moderator, Representative agents. Integration target for BKC /ingest.",
      "confidence": 1.0
    },
    {
      "name": "Lucian",
      "type": "Person",
      "context": "Astral Protocol contributor, location attestation and TEE-based location proofs",
      "confidence": 0.85
    },
    {
      "name": "Astral Protocol",
      "type": "Organization",
      "context": "Location verification and attestation protocol using TEE (Trusted Execution Environments). Near-term integration target for BKC location layer.",
      "confidence": 0.95
    },
    {
      "name": "Toucan Protocol",
      "type": "Organization",
      "context": "ReFi and on-chain carbon market protocol. Ecosystem connection to Astral Protocol.",
      "confidence": 0.85
    },
    {
      "name": "Carey Murdock",
      "type": "Person",
      "context": "Gitcoin contributor, part of the bioregional AI swarms coalition",
      "confidence": 0.85
    },
    {
      "name": "Bioregional Knowledge Commons",
      "type": "Organization",
      "context": "BKC — federated bioregional knowledge infrastructure, KOI-net federation, 4 nodes live",
      "confidence": 1.0
    }
  ],
  "relationships": [
    {"subject": "Kevin Owocki", "predicate": "founded", "object": "Gitcoin", "confidence": 1.0},
    {"subject": "Kevin Owocki", "predicate": "affiliated_with", "object": "Gitcoin", "confidence": 1.0},
    {"subject": "owockibot", "predicate": "affiliated_with", "object": "Gitcoin", "confidence": 0.9},
    {"subject": "Benjamin Life", "predicate": "affiliated_with", "object": "Bioregional Knowledge Commons", "confidence": 0.85},
    {"subject": "AG Neyer", "predicate": "affiliated_with", "object": "Clawsmos", "confidence": 1.0},
    {"subject": "Lucian", "predicate": "affiliated_with", "object": "Astral Protocol", "confidence": 0.9},
    {"subject": "Astral Protocol", "predicate": "affiliated_with", "object": "Toucan Protocol", "confidence": 0.8},
    {"subject": "Carey Murdock", "predicate": "affiliated_with", "object": "Gitcoin", "confidence": 0.9}
  ]
}' || INGEST_FAILURES=$((INGEST_FAILURES + 1))

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3: Seed Front Range node
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "━━━ Step 3: Seed Front Range node ━━━"
echo ""

ingest_node "front-range" '{
  "document_rid": "bkc:seed:build-day-community-fr:2026-03-03",
  "source": "bkc-steward-seed",
  "content": "Build day Front Range community entity seeding. Coalition members working in Front Range / Boulder-Denver bioregion.",
  "entities": [
    {
      "name": "AG Neyer",
      "type": "Person",
      "context": "Clawsmos co-founder, agent-native coordination infrastructure, Summarizer pipeline integration target",
      "confidence": 1.0
    },
    {
      "name": "Clawsmos",
      "type": "Organization",
      "context": "Agent-native coordination layer. Matrix rooms with Summarizer, Orchestrator, Moderator, Representative agents.",
      "confidence": 1.0
    },
    {
      "name": "Todd Youngblood",
      "type": "Person",
      "context": "Nou-Techne contributor. co-op.us and agent task allocation development. Front Range bioregion.",
      "confidence": 0.9
    },
    {
      "name": "Nou-Techne",
      "type": "Organization",
      "context": "Coordination technology research group. A2A protocol demos. co-op.us development. Front Range based.",
      "confidence": 0.9
    }
  ],
  "relationships": [
    {"subject": "AG Neyer", "predicate": "affiliated_with", "object": "Clawsmos", "confidence": 1.0},
    {"subject": "Todd Youngblood", "predicate": "affiliated_with", "object": "Nou-Techne", "confidence": 0.9}
  ]
}' || INGEST_FAILURES=$((INGEST_FAILURES + 1))

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4: Verification
# ─────────────────────────────────────────────────────────────────────────────
echo ""
echo "━━━ Step 4: Verification ━━━"
echo ""

echo "Spot-checking: search for 'owocki' on Octo..."
search_node "octo-salish-sea" "owocki"

echo ""
echo "Spot-checking: search for 'Todd' on Front Range..."
search_node "front-range" "Todd"

echo ""
echo "Seeded entity log:"
cat "$LOG"

echo ""
echo "=========================================="
if [[ "$INGEST_FAILURES" -eq 0 ]]; then
  echo " Seeding complete — all ingest steps PASSED."
else
  echo " Seeding finished with $INGEST_FAILURES FAILED ingest step(s)."
  echo " Review error output above. Entities from failed steps were NOT seeded."
fi
echo ""
echo " Next steps:"
echo "   1. Run: bash demo-smoke.sh   (confirm still 6/6 PASS)"
echo "   2. Query entity counts on each node to get updated totals"
echo "   3. Update entity count in telegram-gate-templates.md before Gate A post"
echo "   4. Gate A deadline: Mar 3, 12:00 PM MT"
echo "=========================================="

exit "$INGEST_FAILURES"
