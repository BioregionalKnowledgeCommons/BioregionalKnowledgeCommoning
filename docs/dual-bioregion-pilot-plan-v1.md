# Dual Bioregion Pilot Plan v1

> Superseded by `docs/dual-bioregion-pilot-plan-v2.md`.

## Summary
This pilot combines GitHub-native collaboration/discovery with KOI-net event federation for a Front Range + Salish Sea interop MVP, while standing up Cascadia immediately as a full node. The pilot runs for 8 weeks with strict consent/provenance and deterministic conflict handling.

## Scope
### In
- Cross-bioregion exchange of `Practice`, `Pattern`, `CaseStudy`, `Organization`, and `Bioregion`.
- Cascadia node deployed now as a full runtime.
- Dual-canonical operations with a field authority map.
- Opal as translation adapter.
- Murmurations profile publishing.

### Out
- Obsidian Sync integration.
- Full Murmurations protocol integration.
- Freeform dual-write without conflict arbitration.

## Success Criteria
- End-to-end propagation between bioregions under 120 seconds p95.
- No unauthorized export of non-consented records.
- Deterministic conflict handling with audit trail.
- Public demo showing cross-bioregion query and provenance.

## Tooling Decisions
| Layer | Tool | Role |
|---|---|---|
| Human authoring | GitHub | PR workflow, review, governance history |
| Federation/state sync | KOI-net | Signed NEW/UPDATE/FORGET events and edge routing |
| Translation | Opal | Adapter between model formats/contracts |
| Discovery | Murmurations | Publish-only profile |
| Vault sync transport | Obsidian Sync | Not used in pilot |

## Topology
```text
[Front Range Node]  <-->  [Salish Sea / Octo]  <-->  [Cascadia Full Node]
```

## Repository Model (Polyrepo)
1. `bkc-commons-contracts` (schemas, authority map, consent taxonomy)
2. `bkc-salish-sea-node`
3. `bkc-front-range-node`
4. `bkc-cascadia-node`
5. Optional `bkc-pilot-ops` (CI/runbooks/monitoring)

## Interfaces and Artifacts
### Shared contracts
- `schemas/entity.schema.json`
- `schemas/relationship.schema.json`
- `schemas/node-manifest.schema.json`
- `policies/field-authority-map.yaml`
- `policies/consent-tags.yaml`

### Node files
- `node/manifest.yaml`
- `node/schema.yaml`
- `node/bridge.yaml`

### Sync endpoints
- `POST /interop/github/webhook`
- `POST /interop/github/export`
- `GET /interop/sync/status`
- `GET /interop/conflicts`
- `POST /interop/conflicts/{id}/resolve`

### Opal adapter endpoints
- `POST /opal/translate/entity`
- `POST /opal/translate/relationship`
- `GET /opal/mapping/version`

## 8-Week Execution Plan
1. Week 1: contracts, consent taxonomy, CI validation gates.
2. Week 2: Front Range node bring-up and KOI handshake with Salish Sea.
3. Week 3: Cascadia full node deployment and edge policy configuration.
4. Week 4: GitHub -> KOI inbound sync and provenance logging.
5. Week 5: KOI -> GitHub outbound bot PR sync and conflict queue.
6. Week 6: Opal adapter + Murmurations profile publishing.
7. Week 7: pilot run on public + consent-tagged records.
8. Week 8: public demo, evaluation, and phase-2 decision.

## Test Matrix
1. Contract validation blocks invalid entities/relationships/manifests.
2. NEW/UPDATE/FORGET propagation works with offline catch-up.
3. Field authority map prevents unauthorized overwrites.
4. Consent enforcement blocks restricted data export.
5. Opal round-trip preserves IDs, type, and consent tags.
6. Murmurations profile validates and updates on release.
7. Observability captures lag, failures, and conflict queue size.

## Rollout and Risk Controls
- Feature flags for inbound sync, outbound sync, and Opal translation.
- Progressive type enablement (`Practice/Pattern` first).
- Alerts for lag > 5 min, sync errors > 2%, or any consent violation.
- Rollback by disabling outbound sync first, preserving read-only federation.

## Assumptions
- 8-week pilot window.
- Cascadia is full node from phase 1.
- GitHub PRs remain primary human authoring surface.
- Shared data restricted to public + consent-tagged records.
