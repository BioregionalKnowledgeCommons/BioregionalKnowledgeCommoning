# GV↔CV Direct Peering — Federation Proof (2026-03-12)

## Overview

Established and verified bidirectional direct peering between Greater Victoria (GV) and Cowichan Valley (CV) KOI nodes, proving the federation membrane operates correctly for leaf-to-leaf communication without routing through the Octo coordinator.

## Node Details

| Node | Host | Port |
|------|------|------|
| Greater Victoria (GV) | 37.27.48.12 | 8351 |
| Cowichan Valley (CV) | 202.61.242.194 | 8351 |

## Setup

### Edge Creation
Used `connect-koi-peer.sh` to create POLL edges on both sides:
- GV side: edge targeting CV (`source=GV, target=CV`)
- CV side: edge targeting GV (`source=CV, target=GV`)

### Edge Approval
Reciprocal POLL edge approval via `admin-edges.sh` membrane approval flow on both nodes.

## Bidirectional Share Proofs

### GV → CV
- **Share RID**: `orn:gv-cv.share:zephyr-68569d94-20260312023349`
- **Status on CV**: `received`
- **Result**: Produced unresolved cross-ref on CV (expected — entity not yet in CV's graph)

### CV → GV
- **Share RID**: `orn:cv-gv.share:cedar-8e3431c4-20260312023721`
- **Status on GV**: `received`
- **Result**: Produced unresolved cross-ref on GV (expected — entity not yet in GV's graph)

## CV Environment Drift Fix

**Blocker**: CV was missing two migrations that had been applied to GV and Octo:
- `057_encryption_key.sql` — ECDSA key encryption support
- `060_multi_peer_sync.sql` — Multi-peer synchronization tables

**Resolution**: Applied both migrations to CV's database. After migration, edge handshake and share exchange completed successfully.

**Root cause**: Environment drift, not plan drift — the migrations existed but hadn't been applied to the CV node during its last deployment.

## Significance

This proves that the KOI-net federation infrastructure supports direct leaf-to-leaf peering without coordinator intermediation. The holonic architecture allows any two nodes to establish direct edges when needed, while still maintaining the coordinator-mediated topology for default operations.

## Network Topology After Proof

```
[Greater Victoria]  ←──direct──→  [Cowichan Valley]
  37.27.48.12                       202.61.242.194
        ↘                                ↙
     [Octo / Salish Sea Coordinator]
          45.132.245.30
          ↕
     [Front Range]
     :8355 (local)
```
