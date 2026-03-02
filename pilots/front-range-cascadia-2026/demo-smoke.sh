#!/usr/bin/env bash
# demo-smoke.sh — Canonical smoke test for Mar 5 build day demo readiness
# Run from workspace root: INGEST_TOKEN=<token> bash BioregionalKnowledgeCommoning/pilots/front-range-cascadia-2026/demo-smoke.sh
set -uo pipefail

BFF="https://45.132.245.30.sslip.io"
PASS=0
FAIL=0
TOTAL=6
TS=$(date +%s)

# --- Helpers ---

red()   { printf '\033[0;31m%s\033[0m\n' "$*"; }
green() { printf '\033[0;32m%s\033[0m\n' "$*"; }
bold()  { printf '\033[1m%s\033[0m\n' "$*"; }

check_pass() { PASS=$((PASS + 1)); green "  PASS: $1"; }
check_fail() { FAIL=$((FAIL + 1)); red   "  FAIL: $1"; }

# Retry wrapper: try once, on failure wait 3s and try again
# Writes response body to tmpfile and returns 0 on HTTP 2xx, 1 otherwise
retry_curl() {
  local tmpfile="$1"; shift
  local http_code
  http_code=$(curl -sS -o "$tmpfile" -w "%{http_code}" "$@" 2>/dev/null) || http_code="000"
  if [[ "$http_code" =~ ^2 ]]; then
    return 0
  fi
  sleep 3
  http_code=$(curl -sS -o "$tmpfile" -w "%{http_code}" "$@" 2>/dev/null) || http_code="000"
  [[ "$http_code" =~ ^2 ]]
}

# --- Pre-flight ---

if [ -z "${INGEST_TOKEN:-}" ]; then
  red "ERROR: INGEST_TOKEN env var is required."
  red "Usage: INGEST_TOKEN=<token> bash $0"
  exit 1
fi

bold "=== BKC Demo Smoke Test ($(date -u '+%Y-%m-%d %H:%M:%S UTC')) ==="
echo ""

# --- Check 1: A2A Agent Card (15 tools) ---

bold "Check 1: A2A Agent Card"
TMP1=$(mktemp)
if retry_curl "$TMP1" -m 10 "${BFF}/.well-known/agent-card.json"; then
  TOOL_COUNT=$(python3 -c "import json; d=json.load(open('$TMP1')); print(len(d.get('skills',d.get('tools',d.get('capabilities',[])))))" 2>/dev/null || echo 0)
  if [ "$TOOL_COUNT" -ge 15 ]; then
    check_pass "Agent card has $TOOL_COUNT tools (>= 15)"
  else
    check_fail "Agent card has $TOOL_COUNT tools (expected >= 15)"
  fi
else
  check_fail "Could not fetch agent card"
fi
rm -f "$TMP1"

# --- Check 2: Entity Search — Octo (AG Neyer) ---

bold "Check 2: Entity Search — Octo (AG Neyer)"
TMP2=$(mktemp)
if retry_curl "$TMP2" -m 10 "${BFF}/commons/api/nodes/octo-salish-sea/search?q=AG+Neyer"; then
  RESULT_COUNT=$(python3 -c "import json; d=json.load(open('$TMP2')); print(d.get('count',0))" 2>/dev/null || echo 0)
  if [ "$RESULT_COUNT" -ge 1 ]; then
    check_pass "Found $RESULT_COUNT result(s) for 'AG Neyer' on Octo"
  else
    check_fail "No results for 'AG Neyer' on Octo"
  fi
else
  check_fail "Entity search on Octo failed"
fi
rm -f "$TMP2"

# --- Check 3: Entity Search — FR (Clawsmos) ---

bold "Check 3: Entity Search — Front Range (Clawsmos)"
TMP3=$(mktemp)
if retry_curl "$TMP3" -m 10 "${BFF}/commons/api/nodes/front-range/search?q=Clawsmos"; then
  RESULT_COUNT=$(python3 -c "import json; d=json.load(open('$TMP3')); print(d.get('count',0))" 2>/dev/null || echo 0)
  if [ "$RESULT_COUNT" -ge 1 ]; then
    check_pass "Found $RESULT_COUNT result(s) for 'Clawsmos' on Front Range"
  else
    check_fail "No results for 'Clawsmos' on Front Range"
  fi
else
  check_fail "Entity search on Front Range failed"
fi
rm -f "$TMP3"

# --- Check 4: Chat Grounding (4 nodes, 0 errors, rationale) ---

bold "Check 4: Chat Grounding (4-node fanout)"
TMP4=$(mktemp)
if retry_curl "$TMP4" -m 30 -X POST "${BFF}/commons/api/chat" \
    -H 'Content-Type: application/json' \
    -d '{"query":"What organizations are part of the bioregional knowledge commons?","limit":3}'; then
  CHAT_RESULT=$(python3 -c "
import json
d = json.load(open('$TMP4'))
nodes = len(d.get('node_responses', []))
has_answer = bool(d.get('answer'))
rationale = bool(d.get('selection_rationale'))
# Count error responses (nodes with error field or missing answer)
error_nodes = sum(1 for nr in d.get('node_responses', []) if nr.get('error'))
print(f'{nodes},{has_answer},{rationale},{error_nodes}')
" 2>/dev/null || echo "0,False,False,-1")
  IFS=',' read -r CHAT_NODES CHAT_HAS_ANSWER CHAT_RATIONALE CHAT_ERROR_NODES <<< "$CHAT_RESULT"
  if [ "$CHAT_NODES" -ge 4 ] && [ "$CHAT_HAS_ANSWER" = "True" ] && [ "$CHAT_RATIONALE" = "True" ] && [ "$CHAT_ERROR_NODES" = "0" ]; then
    check_pass "Chat: $CHAT_NODES nodes, answer=yes, rationale=yes, error_nodes=$CHAT_ERROR_NODES"
  else
    check_fail "Chat: nodes=$CHAT_NODES (want >=4), answer=$CHAT_HAS_ANSWER, rationale=$CHAT_RATIONALE, error_nodes=$CHAT_ERROR_NODES (want 0)"
  fi
else
  check_fail "Chat endpoint unreachable"
fi
rm -f "$TMP4"

# --- Check 5: 4-Node Health ---

bold "Check 5: 4-Node Health"
TMP5=$(mktemp)
if retry_curl "$TMP5" -m 15 "${BFF}/commons/api/nodes"; then
  HEALTH_RESULT=$(python3 -c "
import json
d = json.load(open('$TMP5'))
nodes = d.get('nodes', [])
required = {'octo-salish-sea', 'greater-victoria', 'front-range', 'cowichan-valley'}
healthy_ids = set()
for n in nodes:
    nid = n['node_id']
    st = n.get('status', n.get('health',{}).get('status','unknown'))
    print(f'  {nid}: {st}')
    if st == 'healthy':
        healthy_ids.add(nid)
missing = required - healthy_ids
if missing:
    print(f'FAIL|{len(healthy_ids)}|{len(nodes)}|missing: {sorted(missing)}')
else:
    print(f'PASS|{len(healthy_ids)}|{len(nodes)}|')
" 2>/dev/null || echo "FAIL|0|0|parse error")
  # Last line is the verdict
  VERDICT_LINE=$(echo "$HEALTH_RESULT" | tail -1)
  # Print per-node status (all lines except last)
  echo "$HEALTH_RESULT" | sed '$d'
  IFS='|' read -r HEALTH_VERDICT HEALTHY_COUNT NODE_COUNT HEALTH_DETAIL <<< "$VERDICT_LINE"
  if [ "$HEALTH_VERDICT" = "PASS" ]; then
    check_pass "All 4 required nodes healthy ($HEALTHY_COUNT/$NODE_COUNT)"
  else
    check_fail "Required nodes not all healthy: $HEALTH_DETAIL"
  fi
else
  check_fail "Could not fetch node list"
fi
rm -f "$TMP5"

# --- Check 6: Segment 4 Summarizer Flow ---

bold "Check 6: Segment 4 — Summarizer Ingest Round-Trip"

# Built-in fixture with timestamped entity names
SMOKE_ORG="SmokeOrg-${TS}"
SMOKE_PERSON="SmokePerson-${TS}"
SMOKE_DOC_RID="smoke:segment4:${TS}"

PAYLOAD=$(cat <<EOFPAYLOAD
{
  "document_rid": "${SMOKE_DOC_RID}",
  "source": "demo-smoke-test",
  "entities": [
    {"name": "${SMOKE_ORG}", "type": "Organization"},
    {"name": "${SMOKE_PERSON}", "type": "Person"}
  ],
  "relationships": [
    {"subject": "${SMOKE_PERSON}", "predicate": "affiliated_with", "object": "${SMOKE_ORG}"}
  ]
}
EOFPAYLOAD
)

# Step 6a: Ingest
TMP6=$(mktemp)
INGEST_OK=false
RESOLVED_URI=""
RESOLVED_NAME=""
if retry_curl "$TMP6" -m 15 -X POST "${BFF}/commons/api/nodes/octo-salish-sea/ingest" \
    -H 'Content-Type: application/json' \
    -H "x-ingest-token: ${INGEST_TOKEN}" \
    -d "$PAYLOAD"; then
  INGEST_RESULT=$(python3 -c "
import json
d = json.load(open('$TMP6'))
success = d.get('success', False)
entities = d.get('canonical_entities', [])
processed = len(entities)
stats = d.get('stats', {})
rels = stats.get('relationships_processed', 0)
# Get the first Organization entity's resolved URI and name
org = next((e for e in entities if e.get('type') == 'Organization'), None)
uri = org['uri'] if org else ''
name = org['name'] if org else ''
print(f'{success}|{processed}|{uri}|{name}|{rels}')
" 2>/dev/null || echo "False|0|||0")
  IFS='|' read -r INGEST_SUCCESS ENTITIES_PROCESSED RESOLVED_URI RESOLVED_NAME RELS_PROCESSED <<< "$INGEST_RESULT"
  if [ "$INGEST_SUCCESS" = "True" ] && [ "$ENTITIES_PROCESSED" -ge 1 ] && [ "${RELS_PROCESSED:-0}" -ge 1 ]; then
    echo "  Ingest: success=$INGEST_SUCCESS, entities=$ENTITIES_PROCESSED, relationships=$RELS_PROCESSED"
    echo "  Resolved org: ${RESOLVED_NAME} (${RESOLVED_URI})"
    INGEST_OK=true
  else
    echo "  Ingest response: success=$INGEST_SUCCESS, entities=$ENTITIES_PROCESSED, relationships=${RELS_PROCESSED:-0}"
    if [ "$INGEST_SUCCESS" = "True" ] && [ "$ENTITIES_PROCESSED" -ge 1 ] && [ "${RELS_PROCESSED:-0}" -lt 1 ]; then
      echo "  WARNING: Entities ingested but relationship (affiliated_with) was not processed"
    fi
  fi
else
  echo "  Ingest HTTP request failed"
fi
rm -f "$TMP6"

# Step 6b: Entity search verification — search for the resolved entity name
SEARCH_OK=false
if $INGEST_OK && [ -n "$RESOLVED_NAME" ]; then
  sleep 1  # brief settle
  SEARCH_TERM=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${RESOLVED_NAME}'))" 2>/dev/null)
  TMP6B=$(mktemp)
  if retry_curl "$TMP6B" -m 10 "${BFF}/commons/api/nodes/octo-salish-sea/search?q=${SEARCH_TERM}"; then
    SEARCH_RESULT=$(python3 -c "
import json
d = json.load(open('$TMP6B'))
results = d.get('results', [])
found = any('${RESOLVED_URI}' == r.get('uri','') for r in results)
print(f'{found},{len(results)}')
" 2>/dev/null || echo "False,0")
    IFS=',' read -r FOUND_URI SEARCH_COUNT <<< "$SEARCH_RESULT"
    if [ "$FOUND_URI" = "True" ]; then
      echo "  Search: found ${RESOLVED_NAME} by URI ($SEARCH_COUNT results)"
      SEARCH_OK=true
    else
      echo "  Search: URI ${RESOLVED_URI} not in $SEARCH_COUNT results"
    fi
  else
    echo "  Search HTTP request failed"
  fi
  rm -f "$TMP6B"
fi

# Step 6c: Chat verification (informational only — not part of pass/fail)
if $INGEST_OK; then
  TMP6C=$(mktemp)
  if retry_curl "$TMP6C" -m 30 -X POST "${BFF}/commons/api/chat" \
      -H 'Content-Type: application/json' \
      -d "{\"query\":\"What do you know about ${SMOKE_ORG}?\",\"limit\":1}"; then
    CHAT_ANSWER=$(python3 -c "
import json
d = json.load(open('$TMP6C'))
answer = d.get('answer', d.get('response', ''))[:120]
print(answer)
" 2>/dev/null || echo "(no answer)")
    echo "  Chat (informational): $CHAT_ANSWER"
  else
    echo "  Chat (informational): endpoint unreachable (not scored)"
  fi
  rm -f "$TMP6C"
fi

# Final verdict for Check 6
if $INGEST_OK && $SEARCH_OK; then
  check_pass "Ingest + search round-trip verified (doc_rid: ${SMOKE_DOC_RID})"
else
  if ! $INGEST_OK; then
    check_fail "Ingest failed for ${SMOKE_DOC_RID}"
  else
    check_fail "Search verification failed for ${SMOKE_ORG}"
  fi
fi

# --- Summary ---

echo ""
bold "=================================="
if [ "$FAIL" -eq 0 ]; then
  green "PASS: ${PASS}/${TOTAL}"
  bold "=================================="
  exit 0
else
  red "FAIL: $((TOTAL - FAIL))/${TOTAL} passed, ${FAIL} failed"
  bold "=================================="
  exit 1
fi
