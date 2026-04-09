---
doc_id: bkc.pattern-language
doc_kind: foundations
status: active
depends_on:
  - bkc.project-vision
  - spore.mycelial-holarchy-architecture
---

# Pattern Language for Bioregional Knowledge Commoning v0.1

> **Upstream reference:** `spore.mycelial-holarchy-architecture` carries the general holonic coordination grammar. This doc applies bioregional-specific commoning patterns.

## Purpose
This document captures reusable design patterns for bioregional knowledge commoning.

A pattern language is not a rigid standard. It is a set of recurring solutions that can be adapted by each bioregion.

## Relationship to Protocol Work
This repository uses three layers:
1. Pattern Language (human and governance layer)
2. Meta-Protocol (minimum interoperability commitments)
3. Reference Profiles (implementable technical serializations)

Patterns inform protocol design. Protocols make selected patterns operational.

The project also works across four artifact roles that should not be collapsed:
- Practices are local and situated.
- Patterns are descriptive abstractions derived from multiple practices.
- Protocols are prescriptive coordination structures selected from patterns.
- Playbooks are local implementations that re-instantiate protocols in context.

The quality test for abstraction here is not maximum portability. It is whether an abstraction helps another place learn without stripping away the context, provenance, consent, and local judgment that made the original practice viable.

## Pattern Template
Use this template when adding new patterns:
- Context: Where this pattern applies.
- Problem: The recurring challenge.
- Forces: Tensions that make this difficult.
- Solution: The reusable response.
- Tradeoffs: What this improves and what it constrains.
- Implementation Signals: Evidence that the pattern is active.
- Anti-Patterns: Common failure modes.

## Core Patterns

### 1. Participation Spectrum
- Context: New bioregions have different technical capacity and governance readiness.
- Problem: One onboarding path excludes many participants.
- Forces: Inclusion vs consistency; speed vs quality.
- Solution: Support multiple participation profiles (non-KOI, KOI full, KOI gateway/partial) under one meta-protocol.
- Tradeoffs: More adapters and docs to maintain.
- Implementation Signals: Distinct onboarding tracks and profile selection docs.
- Anti-Patterns: "Everyone must run the same stack."

### 2. Thin Contract
- Context: Tool diversity is unavoidable.
- Problem: Full schema standardization harms plurality; no contract harms interop.
- Forces: Tech agnosticism vs machine interoperability.
- Solution: Require only three invariants for shared artifacts: what is shared, who attests, who can use/how.
- Tradeoffs: Thin contracts need adapters for richer use cases.
- Implementation Signals: Meta-protocol conformance checks succeed across mixed stacks.
- Anti-Patterns: Hidden stack-specific assumptions in canonical fields.

### 3. Consent Boundary
- Context: Multi-level sharing across local, regional, and trans-regional networks.
- Problem: Knowledge can leak across levels without explicit authorization.
- Forces: Discovery value vs sovereignty protection.
- Solution: Default to opt-in boundary crossing with explicit consent metadata and policy checks at each boundary.
- Tradeoffs: Slower propagation for sensitive artifacts.
- Implementation Signals: Boundary policy defined for local to coordinator to external flows.
- Anti-Patterns: Implicit global sharing by default.

### 4. Emergent Bridge
- Context: Bioregions use different ontologies and vocabularies.
- Problem: Hard-mapping everything up front is slow and brittle.
- Forces: Translation quality vs onboarding speed.
- Solution: Allow local types and propose mappings iteratively with human review.
- Tradeoffs: Early cross-region search quality may be uneven.
- Implementation Signals: Unmapped concepts are preserved and queued for mapping review.
- Anti-Patterns: Auto-flattening local concepts into a fixed ontology.

### 5. Holonic Nest
- Context: Sub-bioregions operate inside larger bioregions.
- Problem: Flat federation models do not match social reality.
- Forces: Local autonomy vs regional coherence.
- Solution: Nested coordinators where internal complexity is locally governed and externally represented through agreed boundary rules.
- Tradeoffs: Additional governance and routing complexity.
- Implementation Signals: Coordinator policies for upstream publication and external query response.
- Anti-Patterns: Central node override of local stewardship decisions.

### 6. Governance Slot
- Context: Rights/licensing frameworks vary by community.
- Problem: Hard-coded universal governance values are unsafe and often unjust.
- Forces: Need machine-actionable controls without imposing one worldview.
- Solution: Define required governance metadata slots, while allowing local value vocabularies and local decision authority.
- Tradeoffs: More heterogeneity in policy values.
- Implementation Signals: Required slots present; values tied to local governance process.
- Anti-Patterns: "Default CC license" assumptions for all knowledge.

### 7. Local-First, Federate-Selective
- Context: Most work starts locally and only some outputs should federate.
- Problem: Systems optimized for external sharing can erode local trust.
- Forces: Local relevance vs trans-local learning.
- Solution: Local-first storage and workflow with selective publication/export paths.
- Tradeoffs: More deliberate publication pipelines.
- Implementation Signals: Distinct internal and federated output paths.
- Anti-Patterns: Treating all local artifacts as globally addressable.

### 8. Situated Transfer
- Context: A pattern or protocol that worked in one bioregion may appear relevant in another.
- Problem: Abstractions travel faster than the conditions that made them work, leading to cargo-cult adoption or extractive reuse.
- Forces: Reuse vs situated judgment; legibility vs fidelity; trans-local learning vs sovereignty.
- Solution: Recommend patterns and protocols only with explicit context packets: source practices/case studies, ecological and governance preconditions, rights/consent constraints, contraindications, and required local playbook adaptation. Keep descriptive pattern matches distinct from prescriptive protocol recommendations.
- Tradeoffs: More metadata to maintain and slower recommendation loops.
- Implementation Signals: Recommendations cite their sources, explain why similarity was computed, surface fit and misfit signals, and require local steward review before operational adoption.
- Anti-Patterns: One-click replication, ranking by semantic similarity alone, and treating protocols as universal recipes.

## Pattern to Protocol Mapping
| Pattern | Meta-Protocol Need | Profile/Implementation Need |
|---|---|---|
| Participation Spectrum | Conformance levels | Node participation profiles |
| Thin Contract | Three invariants | Reference profile + adapters |
| Consent Boundary | Required consent/rights slots | Policy checks in gateways/coordinators |
| Emergent Bridge | Local type allowance | Mapping queue and review workflows |
| Holonic Nest | Boundary-aware publication semantics | Coordinator policies and swarm topology |
| Governance Slot | Required policy fields | Local governance vocabulary bindings |
| Local-First, Federate-Selective | Snapshot + event modes | Publish/export workflows |
| Situated Transfer | Provenance, fit, and rights signals on shared artifacts | Recommendation workflows + local playbook review |

## Versioning
- Version: `v0.1`
- Change rule: material pattern additions/changes require decision issue and decision-log entry.
