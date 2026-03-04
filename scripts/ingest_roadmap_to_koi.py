#!/usr/bin/env python3
"""
Ingest semantic roadmap into KOI knowledge graph.

Uses direct PostgreSQL access (matching the KOI entity_registry schema)
to upsert roadmap nodes as entities with OpenAI embeddings, create
relationships from edges, and clean up stale data via mark/sweep.

Usage:
    # Preview (no DB changes)
    python ingest_roadmap_to_koi.py --db octo_koi --dry-run

    # Apply to Octo node
    python ingest_roadmap_to_koi.py --db octo_koi --apply

    # Apply with smoke checks (requires KOI API to be running)
    python ingest_roadmap_to_koi.py --db octo_koi --apply --smoke --api http://localhost:8351

    # Specify custom roadmap file and DB connection
    python ingest_roadmap_to_koi.py --db octo_koi --apply \
        --roadmap /path/to/roadmap-data.json \
        --host localhost --port 5432 --user postgres --password postgres

Environment:
    OPENAI_API_KEY  — Required for embedding generation
    POSTGRES_HOST   — DB host (default: localhost)
    POSTGRES_PORT   — DB port (default: 5432)
    POSTGRES_USER   — DB user (default: postgres)
    POSTGRES_PASSWORD — DB password (default: postgres)
    EMBEDDING_MODEL — OpenAI model (default: text-embedding-ada-002)
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Map roadmap node kinds to KOI entity types
KIND_TO_TYPE = {
    "outcome": "Outcome",
    "initiative": "Initiative",
    "work_item": "WorkItem",
    "decision": "Decision",
    "risk": "Risk",
    "milestone": "Milestone",
    "metric": "Metric",
}

# Predicate mapping (roadmap edge types → KOI predicates)
EDGE_TO_PREDICATE = {
    "delivers": "delivers",
    "depends_on": "depends_on",
    "mitigates": "mitigates",
    "measures": "measures",
    "informs": "informs",
    "blocks": "blocks",
    "references": "references",
}

ROADMAP_URI_PREFIX = "roadmap:"
ROADMAP_SOURCE = "roadmap-ingest"


def uri_for_node(node_id: str) -> str:
    return f"{ROADMAP_URI_PREFIX}{node_id}"


def normalize_text(text: str) -> str:
    """Normalize entity text (matches KOI's normalize_entity_text)."""
    text = text.lower().strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def content_hash(data: dict) -> str:
    """SHA-256 of the JSON roadmap data for change detection."""
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


# ---------------------------------------------------------------------------
# Embedding generation
# ---------------------------------------------------------------------------

def generate_embedding(text: str, model: str) -> Optional[list[float]]:
    """Generate embedding via OpenAI API."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        import requests
        resp = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"model": model, "input": normalize_text(text)},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()["data"][0]["embedding"]
    except Exception as e:
        log.warning(f"  Embedding generation failed for '{text[:50]}': {e}")
        return None


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------

def get_db_connection(args):
    """Create a psycopg2 connection from CLI args + env vars."""
    import psycopg2
    return psycopg2.connect(
        host=args.host or os.getenv("POSTGRES_HOST", "localhost"),
        port=args.port or int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=args.db,
        user=args.user or os.getenv("POSTGRES_USER", "postgres"),
        password=args.password or os.getenv("POSTGRES_PASSWORD", "postgres"),
    )


def upsert_entity(cur, uri: str, entity_type: str, name: str, text: str,
                  metadata: dict, embedding: Optional[list[float]],
                  has_embeddings_table: bool = False) -> bool:
    """Upsert a roadmap entity into entity_registry (+ entity_embeddings if available)."""
    normalized = normalize_text(name)
    metadata_json = json.dumps(metadata)

    try:
        if embedding:
            embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
            cur.execute("""
                INSERT INTO entity_registry (
                    fuseki_uri, entity_text, entity_type, normalized_text,
                    source, first_seen_rid, metadata, embedding
                ) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb, %s::vector)
                ON CONFLICT (fuseki_uri) DO UPDATE SET
                    entity_text = EXCLUDED.entity_text,
                    entity_type = EXCLUDED.entity_type,
                    normalized_text = EXCLUDED.normalized_text,
                    metadata = EXCLUDED.metadata,
                    embedding = EXCLUDED.embedding
            """, (uri, name, entity_type, normalized, ROADMAP_SOURCE,
                  f"roadmap:{metadata.get('roadmap_version', 'unknown')}",
                  metadata_json, embedding_str))
        else:
            cur.execute("""
                INSERT INTO entity_registry (
                    fuseki_uri, entity_text, entity_type, normalized_text,
                    source, first_seen_rid, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb)
                ON CONFLICT (fuseki_uri) DO UPDATE SET
                    entity_text = EXCLUDED.entity_text,
                    entity_type = EXCLUDED.entity_type,
                    normalized_text = EXCLUDED.normalized_text,
                    metadata = EXCLUDED.metadata
            """, (uri, name, entity_type, normalized, ROADMAP_SOURCE,
                  f"roadmap:{metadata.get('roadmap_version', 'unknown')}",
                  metadata_json))

        # Also upsert into entity_embeddings if table exists and embedding was generated
        if embedding and has_embeddings_table:
            embedding_str = "[" + ",".join(str(x) for x in embedding) + "]"
            cur.execute("""
                INSERT INTO entity_embeddings (entity_uri, embedding)
                VALUES (%s, %s::vector)
                ON CONFLICT (entity_uri) DO UPDATE SET
                    embedding = EXCLUDED.embedding
            """, (uri, embedding_str))

        return True
    except Exception as e:
        log.error(f"  Failed to upsert {uri}: {e}")
        return False


def create_relationship(cur, subject_uri: str, predicate: str, object_uri: str) -> bool:
    """Create a relationship in entity_relationships."""
    if subject_uri == object_uri:
        log.warning(f"  Skipping self-referential: {subject_uri} --{predicate}--> {object_uri}")
        return False

    try:
        cur.execute("""
            INSERT INTO entity_relationships (subject_uri, predicate, object_uri, source)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (subject_uri, predicate, object_uri) DO NOTHING
        """, (subject_uri, predicate, object_uri, ROADMAP_SOURCE))
        return True
    except Exception as e:
        log.warning(f"  Failed to create rel {subject_uri} --{predicate}--> {object_uri}: {e}")
        return False


def sweep_stale_entities(cur, upserted_uris: set[str],
                        has_embeddings_table: bool = False) -> int:
    """Delete roadmap entities not in the current upsert set."""
    # Find all existing roadmap URIs
    cur.execute("""
        SELECT fuseki_uri FROM entity_registry
        WHERE fuseki_uri LIKE %s
    """, (f"{ROADMAP_URI_PREFIX}%",))
    existing_uris = {row[0] for row in cur.fetchall()}

    stale = existing_uris - upserted_uris
    if not stale:
        log.info("  No stale entities found")
        return 0

    log.info(f"  Found {len(stale)} stale roadmap entities to remove")
    stale_list = list(stale)

    for uri in stale_list:
        log.info(f"    Removing: {uri}")

    # Delete from entity_embeddings first (only if table exists)
    if has_embeddings_table:
        cur.execute("""
            DELETE FROM entity_embeddings WHERE entity_uri = ANY(%s)
        """, (stale_list,))

    # Delete relationships where both sides are roadmap URIs
    cur.execute("""
        DELETE FROM entity_relationships
        WHERE source = %s
          AND (subject_uri = ANY(%s) OR object_uri = ANY(%s))
    """, (ROADMAP_SOURCE, stale_list, stale_list))

    # Delete the entities
    cur.execute("""
        DELETE FROM entity_registry WHERE fuseki_uri = ANY(%s)
    """, (stale_list,))

    return len(stale)


def check_entity_embeddings_table(cur) -> bool:
    """Pre-flight: verify entity_embeddings table exists."""
    try:
        cur.execute("SELECT 1 FROM entity_embeddings LIMIT 0")
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Main ingest
# ---------------------------------------------------------------------------

def ingest_roadmap(args, roadmap_path: str, dry_run: bool = True) -> dict:
    """Main ingest function."""
    roadmap_file = Path(roadmap_path)
    if not roadmap_file.exists():
        log.error(f"Roadmap file not found: {roadmap_path}")
        sys.exit(1)

    with open(roadmap_file) as f:
        roadmap = json.load(f)

    version = roadmap.get("version", "unknown")
    data_hash = content_hash(roadmap)
    nodes = roadmap.get("nodes", [])
    edges = roadmap.get("edges", [])

    log.info(f"Roadmap v{version} — {len(nodes)} nodes, {len(edges)} edges (hash: {data_hash[:12]})")

    embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
    has_openai = bool(os.getenv("OPENAI_API_KEY"))
    if has_openai:
        log.info(f"Embedding model: {embedding_model}")
    else:
        log.warning("OPENAI_API_KEY not set — entities will be stored without embeddings")

    if dry_run:
        log.info("=== DRY RUN — no DB changes ===")
        stats = {"entities_upserted": 0, "entities_failed": 0,
                 "rels_created": 0, "rels_failed": 0, "stale_removed": 0}
        for node in nodes:
            entity_type = KIND_TO_TYPE.get(node["kind"])
            if entity_type:
                log.info(f"  [DRY RUN] Would upsert {uri_for_node(node['id'])} ({entity_type}): {node['title']}")
                stats["entities_upserted"] += 1
        for edge in edges:
            predicate = EDGE_TO_PREDICATE.get(edge["type"])
            if predicate:
                log.info(f"  [DRY RUN] Would create: {uri_for_node(edge['from'])} --{predicate}--> {uri_for_node(edge['to'])}")
                stats["rels_created"] += 1
        log.info(f"  Would upsert {stats['entities_upserted']} entities, {stats['rels_created']} relationships")
        return stats

    # Connect to DB
    import psycopg2
    conn = get_db_connection(args)
    conn.autocommit = False
    cur = conn.cursor()

    # Pre-flight checks
    has_embeddings_table = check_entity_embeddings_table(cur)
    conn.rollback()  # reset any error state from check
    if not has_embeddings_table:
        log.warning("entity_embeddings table not found — embeddings will be stored in entity_registry only")

    upserted_uris: set[str] = set()
    stats = {"entities_upserted": 0, "entities_failed": 0,
             "rels_created": 0, "rels_failed": 0, "stale_removed": 0}

    try:
        # --- Upsert entities ---
        log.info("--- Upserting entities ---")
        for node in nodes:
            entity_type = KIND_TO_TYPE.get(node["kind"])
            if not entity_type:
                log.warning(f"  Unknown kind '{node['kind']}' for node {node['id']}, skipping")
                continue

            uri = uri_for_node(node["id"])
            name = node["title"]
            summary = node.get("summary", "")
            text = f"{name} — {summary}" if summary else name

            metadata: dict[str, Any] = {
                "roadmap_node_id": node["id"],
                "roadmap_kind": node["kind"],
                "roadmap_status": node.get("status"),
                "roadmap_priority": node.get("priority"),
                "roadmap_horizon": node.get("horizon"),
                "roadmap_owner": node.get("owner"),
                "roadmap_version": version,
            }
            if node.get("due_date"):
                metadata["due_date"] = node["due_date"]
            if node.get("tags"):
                metadata["roadmap_tags"] = node["tags"]

            # Generate embedding
            embedding = generate_embedding(text, embedding_model) if has_openai else None

            ok = upsert_entity(cur, uri, entity_type, name, text, metadata, embedding,
                              has_embeddings_table=has_embeddings_table)
            if ok:
                stats["entities_upserted"] += 1
                upserted_uris.add(uri)
            else:
                stats["entities_failed"] += 1

        # --- Delete old roadmap relationships before re-creating ---
        log.info("--- Clearing old roadmap relationships ---")
        cur.execute("""
            DELETE FROM entity_relationships WHERE source = %s
        """, (ROADMAP_SOURCE,))
        deleted_rels = cur.rowcount
        log.info(f"  Cleared {deleted_rels} old roadmap relationships")

        # --- Create relationships ---
        log.info("--- Creating relationships ---")
        for edge in edges:
            predicate = EDGE_TO_PREDICATE.get(edge["type"])
            if not predicate:
                log.warning(f"  Unknown edge type '{edge['type']}', skipping")
                continue

            subject_uri = uri_for_node(edge["from"])
            object_uri = uri_for_node(edge["to"])

            ok = create_relationship(cur, subject_uri, predicate, object_uri)
            if ok:
                stats["rels_created"] += 1
            else:
                stats["rels_failed"] += 1

        # --- Mark/sweep cleanup ---
        log.info("--- Mark/sweep cleanup ---")
        stats["stale_removed"] = sweep_stale_entities(cur, upserted_uris,
                                                       has_embeddings_table=has_embeddings_table)

        # Commit
        conn.commit()
        log.info("--- Committed to database ---")

    except Exception as e:
        conn.rollback()
        log.error(f"Transaction failed, rolled back: {e}")
        raise
    finally:
        cur.close()
        conn.close()

    # Summary
    log.info("--- Summary ---")
    log.info(f"  Entities: {stats['entities_upserted']} upserted, {stats['entities_failed']} failed")
    log.info(f"  Relationships: {stats['rels_created']} created, {stats['rels_failed']} failed")
    log.info(f"  Stale entities removed: {stats['stale_removed']}")

    return stats


# ---------------------------------------------------------------------------
# Smoke checks (use KOI API)
# ---------------------------------------------------------------------------

def run_smoke_checks(api_base: str, expected_count: int, args=None):
    """Post-ingest verification via KOI API + direct DB checks."""
    import requests
    log.info("--- Smoke checks ---")

    # 1. Entity search (entity_type is a valid param on /entity-search)
    try:
        result = requests.get(
            f"{api_base}/entity-search",
            params={"query": "bioregional swarm", "entity_type": "Outcome"},
            timeout=15,
        ).json()
        count = len(result.get("results", []))
        status = "PASS" if count >= 1 else "WARN"
        log.info(f"  [{status}] Entity search 'bioregional swarm' (Outcome): {count} results")
    except Exception as e:
        log.warning(f"  [FAIL] Entity search: {e}")

    # 2. Chat retrieval (uses /chat endpoint)
    try:
        result = requests.post(
            f"{api_base}/chat",
            json={"query": "What are the BKC outcomes?"},
            timeout=30,
        ).json()
        sources = result.get("sources", [])
        roadmap_sources = [s for s in sources
                          if str(s.get("uri", s.get("fuseki_uri", ""))).startswith("roadmap:")]
        status = "PASS" if len(roadmap_sources) >= 1 else "WARN"
        log.info(f"  [{status}] Chat retrieval: {len(roadmap_sources)} roadmap sources in answer")
    except Exception as e:
        log.warning(f"  [FAIL] Chat retrieval: {e}")

    # 3. Embedding count (direct DB query)
    if args:
        try:
            conn = get_db_connection(args)
            cur = conn.cursor()

            # Count roadmap entities in entity_registry
            cur.execute("""
                SELECT count(*) FROM entity_registry
                WHERE fuseki_uri LIKE %s
            """, (f"{ROADMAP_URI_PREFIX}%",))
            entity_count = cur.fetchone()[0]
            status = "PASS" if entity_count == expected_count else "WARN"
            log.info(f"  [{status}] Entity count in registry: {entity_count} (expected {expected_count})")

            # Count embeddings in entity_embeddings (if table exists)
            has_ee = check_entity_embeddings_table(cur)
            conn.rollback()  # reset any error state
            if has_ee:
                cur.execute("""
                    SELECT count(*) FROM entity_embeddings
                    WHERE entity_uri LIKE %s
                """, (f"{ROADMAP_URI_PREFIX}%",))
                embed_count = cur.fetchone()[0]
                status = "PASS" if embed_count == expected_count else "WARN"
                log.info(f"  [{status}] Embedding count in entity_embeddings: {embed_count} (expected {expected_count})")
            else:
                log.info("  [SKIP] entity_embeddings table not found — checking registry embeddings")
                cur.execute("""
                    SELECT count(*) FROM entity_registry
                    WHERE fuseki_uri LIKE %s AND embedding IS NOT NULL
                """, (f"{ROADMAP_URI_PREFIX}%",))
                embed_count = cur.fetchone()[0]
                status = "PASS" if embed_count == expected_count else "WARN"
                log.info(f"  [{status}] Embeddings in entity_registry: {embed_count} (expected {expected_count})")

            cur.close()
            conn.close()
        except Exception as e:
            log.warning(f"  [FAIL] DB embedding check: {e}")
    else:
        log.info(f"  [SKIP] No DB args available for embedding count check (expected {expected_count})")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Ingest semantic roadmap into KOI knowledge graph")
    parser.add_argument("--db", required=True, help="PostgreSQL database name (e.g. octo_koi)")
    parser.add_argument("--host", default=None, help="DB host (default: env POSTGRES_HOST or localhost)")
    parser.add_argument("--port", default=None, type=int, help="DB port (default: env POSTGRES_PORT or 5432)")
    parser.add_argument("--user", default=None, help="DB user (default: env POSTGRES_USER or postgres)")
    parser.add_argument("--password", default=None, help="DB password (default: env POSTGRES_PASSWORD)")
    parser.add_argument("--roadmap", default=None, help="Path to roadmap-data.json (auto-detected if not set)")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--apply", action="store_true", help="Apply changes")
    parser.add_argument("--smoke", action="store_true", help="Run smoke checks after ingest")
    parser.add_argument("--api", default=None, help="KOI API base URL for smoke checks (e.g. http://localhost:8351)")

    args = parser.parse_args()

    if not args.dry_run and not args.apply:
        log.error("Must specify --dry-run or --apply")
        sys.exit(1)

    # Auto-detect roadmap path
    if args.roadmap:
        roadmap_path = args.roadmap
    else:
        script_dir = Path(__file__).parent
        candidates = [
            script_dir.parent / "docs" / "roadmap" / "semantic-roadmap.json",
            script_dir.parent.parent / "bioregional-commons-web" / "web" / "public" / "roadmap-data.json",
        ]
        roadmap_path = None
        for c in candidates:
            if c.exists():
                roadmap_path = str(c)
                break
        if not roadmap_path:
            log.error("Could not find roadmap data. Use --roadmap to specify path.")
            sys.exit(1)

    log.info(f"Using roadmap: {roadmap_path}")
    stats = ingest_roadmap(args, roadmap_path, dry_run=args.dry_run)

    if args.smoke and args.apply:
        api_base = args.api
        if not api_base:
            log.warning("--smoke requires --api <url>. Skipping smoke checks.")
        else:
            run_smoke_checks(api_base, stats["entities_upserted"], args=args)


if __name__ == "__main__":
    main()
