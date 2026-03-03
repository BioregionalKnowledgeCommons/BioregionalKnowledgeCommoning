#!/usr/bin/env bash
# sync-roadmap-to-web.sh
# Copies semantic-roadmap.json into the web app's public directory so the
# /commons/roadmap dashboard reads the latest data on next build/refresh.
#
# Usage (from BioregionKnwoledgeCommons meta-repo root):
#   bash BioregionalKnowledgeCommoning/scripts/sync-roadmap-to-web.sh
#
# After running, commit both files and push, then on the server:
#   cd /root/bioregional-commons-web && git pull && cd web && npm run build && systemctl restart commons-web

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

SRC="${REPO_ROOT}/BioregionalKnowledgeCommoning/docs/roadmap/semantic-roadmap.json"
DST="${REPO_ROOT}/bioregional-commons-web/web/public/roadmap-data.json"

if [[ ! -f "$SRC" ]]; then
  echo "ERROR: Source not found: $SRC" >&2
  exit 1
fi

cp "$SRC" "$DST"
echo "✓ Copied semantic-roadmap.json → bioregional-commons-web/web/public/roadmap-data.json"
echo "  Node count: $(python3 -c "import json,sys; d=json.load(open('$DST')); print(len(d['nodes']))" 2>/dev/null || echo '(python3 not available)')"
echo ""
echo "Next steps:"
echo "  git add BioregionalKnowledgeCommoning/docs/roadmap/semantic-roadmap.json bioregional-commons-web/web/public/roadmap-data.json"
echo "  git commit -m 'sync: update roadmap-data.json from semantic-roadmap.json'"
echo "  git push"
echo "  ssh root@45.132.245.30 'cd /root/bioregional-commons-web && git pull && cd web && npm run build && systemctl restart commons-web'"
