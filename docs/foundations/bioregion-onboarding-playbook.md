# Bioregion Onboarding Playbook

## Purpose
Provide practical onboarding guidance for new bioregions using the layered model:
- Pattern language
- Meta-protocol
- Optional reference profiles

## Recommended Default
Start with one node and make it swarm-ready.

Use swarm-from-start only when governance roles and operating capacity are already established.

## Track A: Single Node First (Recommended)

### 0-30 Days
- Identify local stewards and decision process.
- Select participation profile (non-KOI, KOI full, KOI gateway/partial).
- Define consent/rights slot values for initial publication tiers.
- Publish first L1 artifact set in event or snapshot mode.

### 31-60 Days
- Add adapter/profile translation if needed.
- Establish mapping review queue for local_type to canonical_type.
- Run first cross-bioregion exchange test with one peer.

### 61-90 Days
- Harden audit and conflict handling.
- Define coordinator-readiness criteria for becoming/joining a swarm.
- Document lessons and update decision log.

## Track B: Swarm from Start (Advanced)

### Prerequisites
- Confirmed local node stewards for at least two sub-regions.
- Confirmed coordinator steward team.
- Written boundary policies (visibility, consent, conflict).

### 0-30 Days
- Stand up sub-nodes + coordinator topology.
- Configure upstream opt-in sharing defaults.
- Validate coordinator boundary checks.

### 31-60 Days
- Test external single-node appearance behavior.
- Run cross-level conflict and consent scenarios.
- Validate provenance chain through coordinator.

### 61-90 Days
- Pilot trans-regional exchange with one external peer.
- Tune boundary and mapping policies.
- Publish governance retrospective.

## Profile Selection Decision Tree
1. Need fastest setup with existing tools? -> Non-KOI node.
2. Need native signed event federation now? -> KOI full node.
3. Need compatibility with KOI peers but keep existing core stack? -> KOI gateway/partial.

## Minimum Artifact Checklist
- Pilot charter
- Pilot plan
- Tooling/authority map
- Decision log
- Consent/rights slot definitions
- Participation profile selection
- Boundary policy statement

## Readiness Gates

### Gate 1: Local Publish Ready
- Rights/consent slots defined.
- First artifacts published with attestations.

### Gate 2: Interop Ready
- Event or snapshot exchange validated with peer.
- Mapping and conflict review paths defined.

### Gate 3: Swarm Ready
- Coordinator boundary policies documented.
- Sub-node to coordinator and coordinator to external flow tested.

## Anti-Patterns
- Starting with global federation before local governance is clear.
- Treating protocol setup as a substitute for stewardship agreements.
- Publishing sensitive artifacts without boundary checks.
