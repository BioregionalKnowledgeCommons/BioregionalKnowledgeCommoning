# Semantic Roadmap

- Program: **Bioregional Knowledge Commons**
- Roadmap ID: `bkc.roadmap.2026.part-b`
- Version: `0.1.0`
- As of: `2026-02-27`
- Generated: `2026-02-27 09:36 UTC`

## Status Summary

| Status | Count |
|---|---|
| `in_progress` | 3 |
| `planned` | 21 |
| `blocked` | 0 |
| `done` | 2 |
| `deprecated` | 0 |

## Outcomes

| ID | Title | Status | Priority | Horizon | Owner |
|---|---|---|---|---|---|
| `outcome.showcase-reliable` | Showcase reliability remains high across 4 nodes | `in_progress` | `P0` | `0-30d` | `owner.darren` |
| `outcome.policy-governed-sharing` | Consent and policy are enforceable in runtime behavior | `planned` | `P0` | `0-30d` | `owner.darren` |
| `outcome.secure-federation-ops` | Federation security controls are tested and drillable | `planned` | `P0` | `0-30d` | `owner.darren` |
| `outcome.eval-driven-kg-chat` | KG chat roadmap decisions are evaluation-driven | `planned` | `P1` | `30-90d` | `owner.darren` |

## Initiatives

| ID | Title | Status | Priority | Horizon | Owner |
|---|---|---|---|---|---|
| `initiative.part-b-kg-chat` | Part B knowledge-graph chat roadmap | `in_progress` | `P0` | `0-30d` | `owner.darren` |
| `initiative.part-b-security-addendum` | Part B security and governance addendum | `planned` | `P0` | `0-30d` | `owner.darren` |
| `initiative.tbff-knowledge-flow-pilot` | Knowledge to flow funding pilot integration | `planned` | `P1` | `30-90d` | `owner.darren` |

## Work Items

| ID | Title | Status | Priority | Horizon | Owner |
|---|---|---|---|---|---|
| `work.s2-security-lane` | Add security lane to operational checkpoints | `planned` | `P0` | `0-30d` | `owner.darren` |
| `work.b5-eval-gates` | Define B5 chat evaluation gates | `planned` | `P0` | `0-30d` | `owner.darren` |
| `work.s1-data-class-matrix` | Define and publish data-class policy matrix | `planned` | `P0` | `0-30d` | `owner.darren` |
| `work.s6-evidence-grading` | Introduce evidence grading in architecture decisions | `planned` | `P0` | `0-30d` | `owner.darren` |
| `work.s3-key-lifecycle-runbook` | Publish key lifecycle and incident runbook | `planned` | `P0` | `0-30d` | `owner.darren` |
| `work.b4-tbff-flow-integration` | Implement TBFF flow write-back loop | `planned` | `P1` | `30-90d` | `owner.darren` |
| `work.b3-federated-chat-policy` | Implement federated chat policy boundaries | `planned` | `P1` | `30-90d` | `owner.darren` |
| `work.b2-graphrag-v1` | Prototype GraphRAG v1 | `planned` | `P1` | `30-90d` | `owner.darren` |
| `work.s5-tee-spike` | TEE confidential RAG spike | `planned` | `P1` | `30-90d` | `owner.darren` |
| `work.s4-ucan-bridge-spike` | UCAN bridge spike | `planned` | `P1` | `30-90d` | `owner.darren` |

### Dependency Execution Order (depends_on)

1. `work.b4-tbff-flow-integration` — Implement TBFF flow write-back loop (planned)
2. `work.b5-eval-gates` — Define B5 chat evaluation gates (planned)
3. `work.s1-data-class-matrix` — Define and publish data-class policy matrix (planned)
4. `work.s3-key-lifecycle-runbook` — Publish key lifecycle and incident runbook (planned)
5. `work.s6-evidence-grading` — Introduce evidence grading in architecture decisions (planned)
6. `work.b2-graphrag-v1` — Prototype GraphRAG v1 (planned)
7. `work.s4-ucan-bridge-spike` — UCAN bridge spike (planned)
8. `work.s5-tee-spike` — TEE confidential RAG spike (planned)
9. `work.s2-security-lane` — Add security lane to operational checkpoints (planned)
10. `work.b3-federated-chat-policy` — Implement federated chat policy boundaries (planned)

## Risks and Mitigations

- `risk.low-rigor-sources`: Architecture drift from low-rigor sources | mitigated by: `work.s6-evidence-grading`
- `risk.auth-migration-regression`: Auth regression during UCAN migration exploration | mitigated by: `work.s2-security-lane`
- `risk.chat-latency-regression`: Latency regression from privacy-heavy runtime changes | mitigated by: `work.s5-tee-spike`

## Milestones

| ID | Title | Status | Priority | Horizon | Owner |
|---|---|---|---|---|---|
| `milestone.part-b-p0-complete` | Part B P0 controls complete | `planned` | `P0` | `0-30d` | `owner.darren` |
| `milestone.part-b-spikes-reviewed` | UCAN and TEE spikes reviewed | `planned` | `P1` | `30-90d` | `owner.darren` |

## Decisions

| ID | Title | Status | Priority | Horizon | Owner |
|---|---|---|---|---|---|
| `decision.node-sovereign-default` | Keep node-sovereign runtime as default | `done` | `P0` | `0-30d` | `owner.darren` |
| `decision.bff-control-plane` | Use BFF as external control plane boundary | `done` | `P0` | `0-30d` | `owner.darren` |

## Metrics

| ID | Title | Status | Priority | Horizon | Owner |
|---|---|---|---|---|---|
| `metric.security-preflight-runtime` | Security preflight runtime | `planned` | `P0` | `0-30d` | `owner.darren` |
| `metric.chat-p95-latency` | Federated chat p95 latency | `planned` | `P1` | `30-90d` | `owner.darren` |

## Canonical Sources

- Machine model: `docs/roadmap/semantic-roadmap.json`
- Schema: `docs/roadmap/semantic-roadmap.schema.json`
- JSON-LD context: `docs/roadmap/semantic-roadmap.context.json`
