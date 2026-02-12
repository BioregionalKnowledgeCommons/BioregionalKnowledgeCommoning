# Holonic Swarm Reference Architecture

## Purpose
Describe how nested bioregional swarms can interoperate while preserving local sovereignty.

A holonic swarm treats each node as both:
- a whole (locally sovereign system)
- a part (participant in larger regional/meta-regional exchange)

## Reference Topology
```text
[Cowichan Node]   [Victoria Node]   [WSANEC Node]
        \             |             /
         \            |            /
          [Salish Sea Coordinator]
                    |
            [Cascadia Coordinator]
                    |
            [External Peers]
```

## Boundary Types

### 1. Visibility Boundary
Defines what is visible at each level.
- Local artifacts are not implicitly globally visible.
- Coordinators expose only policy-permitted summaries/artifacts.

### 2. Consent Boundary
Defines what may cross local -> regional -> external boundaries.
- Default: opt-in crossing.
- Sensitive tiers require explicit authorization before each broader publication level.

### 3. Conflict Boundary
Defines where conflicts are resolved.
- Local conflicts resolved locally.
- Cross-node shared-field conflicts routed to designated coordinator queue.
- No coordinator may rewrite local authoritative fields without policy basis.

## Coordinator Responsibilities
- Enforce boundary policies before forwarding/publication.
- Preserve provenance chains.
- Preserve local_type for unmapped concepts.
- Provide externally coherent responses without exposing restricted internals.

## External Single-Node Appearance
A swarm may appear as one node externally when:
- coordinator publishes a policy-compliant aggregated interface
- internal node boundaries remain auditable
- provenance includes contributing sources where consent allows

## Default Safe Policies
- Upstream sharing: opt-in.
- External sharing from coordinator: opt-in and review-gated.
- Unmapped ontology terms: preserve and annotate, do not flatten.

## Query Handling Rules
1. External query arrives at coordinator.
2. Coordinator evaluates consent/visibility policy.
3. Coordinator dispatches to eligible sub-nodes.
4. Coordinator aggregates allowed responses.
5. Coordinator emits response with provenance and boundary notes.

## Non-Goals
- Defining one universal swarm governance model.
- Requiring all swarms to expose identical interfaces.
