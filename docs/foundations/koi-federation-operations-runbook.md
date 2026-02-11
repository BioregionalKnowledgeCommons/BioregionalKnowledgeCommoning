# KOI Federation Operations Runbook

Operational checklist for standing up and troubleshooting KOI-net federation between bioregional nodes.

## Scope
- Applies to coordinator/leaf and peer/peer KOI-net topologies.
- Focused on production issues observed in real deployment (Octo ↔ Cowichan, February 2026).

## Minimum Federation Contract

All of these must be true:

1. Public endpoint reachability
- Node advertises a peer-reachable `KOI_BASE_URL`.
- `/koi-net/*` is reachable from peers (direct bind or reverse proxy).

2. Correct POLL edge orientation
- `source_node` = node being polled (data provider).
- `target_node` = node that runs the poller.

3. Peer key registry completeness
- Each node stores the peer's `public_key` in `koi_net_nodes`.
- Signed envelopes cannot verify without this.

4. Endpoint compatibility
- Use `POST /koi-net/events/poll` and `POST /koi-net/events/confirm`.
- Do not use legacy `POST /koi-net/poll`.

5. Poll + confirm loop healthy
- Poll requests return `200`.
- Delivered events are followed by confirms.

## Bring-Up Sequence

1. Set node env
- `KOI_NET_ENABLED=true`
- `KOI_NODE_NAME=<node-slug>`
- `KOI_BASE_URL=http://<public-ip-or-domain>:<port>`

2. Start service and verify local health
- `curl http://127.0.0.1:<port>/koi-net/health`

3. Register peer node row with key
- Insert/upsert into `koi_net_nodes` including `public_key`.

4. Upsert POLL edge with explicit direction
- Insert/upsert `koi_net_edges` with correct source/target.

5. Verify traffic and confirmations
- Poll logs show `200`.
- Delivery and confirmation counters increase.

## SQL Upsert Patterns

Use upserts (not `DO NOTHING`) so reruns self-heal stale orientation/key state.

```sql
-- Peer node row
INSERT INTO koi_net_nodes (node_rid, node_name, node_type, base_url, public_key, status, last_seen)
VALUES (<rid>, <name>, 'FULL', <base_url>, <public_key>, 'active', now())
ON CONFLICT (node_rid) DO UPDATE SET
  node_name = EXCLUDED.node_name,
  node_type = EXCLUDED.node_type,
  base_url = EXCLUDED.base_url,
  public_key = COALESCE(EXCLUDED.public_key, koi_net_nodes.public_key),
  status = 'active',
  last_seen = now();

-- POLL edge row
INSERT INTO koi_net_edges (edge_rid, source_node, target_node, edge_type, status, rid_types)
VALUES (<edge_rid>, <source_node>, <target_node>, 'POLL', 'APPROVED', <rid_types>)
ON CONFLICT (edge_rid) DO UPDATE SET
  source_node = EXCLUDED.source_node,
  target_node = EXCLUDED.target_node,
  edge_type = EXCLUDED.edge_type,
  status = 'APPROVED',
  rid_types = EXCLUDED.rid_types,
  updated_at = now();
```

## Fast Diagnostics

```bash
# Node profile + base URL
curl -s http://127.0.0.1:8351/koi-net/health | python3 -m json.tool

# Edge orientation
docker exec regen-koi-postgres psql -U postgres -d <db> -c \
  "SELECT edge_rid, source_node, target_node, edge_type, status FROM koi_net_edges;"

# Peer key presence
docker exec regen-koi-postgres psql -U postgres -d <db> -c \
  "SELECT node_rid, node_name, length(public_key) AS key_len, base_url FROM koi_net_nodes;"

# Event flow
docker exec regen-koi-postgres psql -U postgres -d <db> -c \
  "SELECT count(*) FROM koi_net_events WHERE '<peer_rid>' = ANY(delivered_to);"
docker exec regen-koi-postgres psql -U postgres -d <db> -c \
  "SELECT count(*) FROM koi_net_events WHERE '<peer_rid>' = ANY(confirmed_by);"
```

## Failure Modes

1. Poll returns `400` with `No public key for <rid>`
- Cause: polled node missing poller public key in `koi_net_nodes`.
- Fix: upsert peer `public_key` or rerun handshake.

2. Poller runs but polls nothing
- Cause: edge direction flipped.
- Fix: set `source_node=<provider>`, `target_node=<self>`.

3. Poll endpoint returns `404`
- Cause: caller using legacy `/koi-net/poll`.
- Fix: use `/koi-net/events/poll`.

4. Peer unreachable or connection refused
- Cause: `KOI_BASE_URL` points to localhost/private endpoint, or `/koi-net/*` not exposed.
- Fix: set reachable `KOI_BASE_URL`; expose via bind or proxy.

5. Poll works but no events processed
- Cause: signed response cannot be verified (missing peer key), or rid type filters exclude data.
- Fix: verify key presence and `rid_types` on the edge.

