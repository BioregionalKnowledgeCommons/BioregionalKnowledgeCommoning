# Pattern Language for Bioregional Knowledge Commoning v0.1

## Purpose
This document captures reusable design patterns for bioregional knowledge commoning.

A pattern language is not a rigid standard. It is a set of recurring solutions that can be adapted by each bioregion.

## Relationship to Protocol Work
This repository uses three layers:
1. Pattern Language (human and governance layer)
2. Meta-Protocol (minimum interoperability commitments)
3. Reference Profiles (implementable technical serializations)

Patterns inform protocol design. Protocols make selected patterns operational.

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

## Versioning
- Version: `v0.1`
- Change rule: material pattern additions/changes require decision issue and decision-log entry.
