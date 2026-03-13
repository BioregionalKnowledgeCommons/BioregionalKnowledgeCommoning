# Foundations

Cross-pilot frameworks that can be reused across bioregional knowledge commoning efforts.

## Core Layered Docs
- [Pattern language v0.1](./pattern-language-for-bioregional-knowledge-commoning-v0.1.md): reusable commoning design patterns (participation, consent boundaries, emergent bridging, holonic nesting).
- [Meta-protocol v0.1](./knowledge-commoning-meta-protocol-v0.1.md): thin interoperability commitments and conformance levels.
- [CommonsChange reference profile v0.1](./commonschange-reference-profile-v0.1.md): optional, implementable event/snapshot exchange profile.
- [Node participation profiles](./node-participation-profiles.md): non-KOI, KOI full, and KOI gateway/partial participation options.
- [Holonic swarm reference architecture](./holonic-swarm-reference-architecture.md): nested coordinator/leaf boundaries and external interface behavior.
- [Rights/licensing/consent policy slots](./rights-licensing-consent-policy-slots.md): required policy metadata slots without universal value mandates.
- [Bioregion onboarding playbook](./bioregion-onboarding-playbook.md): practical 30/60/90 day onboarding tracks and readiness gates.

## Capital Coordination
- [Commitment pooling foundations](./commitment-pooling-foundations.md): philosophical foundations, technical model (Sarafu/CLC DAO tiers, state machine), integration seams (TBFF/owockibot/co-op.us/KOI-net/GE), and governance guidance. Ontology types: `Commitment`, `CommitmentPool`, `CommitmentAction`. API: `/commitments/` and `/pools/`.
- [Flow funding foundations](./flow-funding-foundations.md): two-track capital allocation — Bioregional Flow Funding (Hub Cultivator / Regenerate Cascadia, trust-based) and TBFF (MycoFi / Mycopunks, algorithmic threshold overflow). Integration architecture: both tracks write Evidence entities with CAT receipt chains to the knowledge graph. Bridge to commitment pools via `proves_commitment` predicate.

## Existing Operational Docs
- [Ontology commoning framework](./ontology-commoning-framework.md): mapping lifecycle, governance, and approval rules.
- [Ontology commoning ops v0.1](./ontology-commoning-ops-v0.1.md): operational workflow for mapping proposals, review, extension triggers, and publication rules.
- [Transcription and processing pipeline](./transcription-and-processing-pipeline.md): consent-aware interview-to-knowledge workflow.
- [Interview-to-graph MVP v0.1](./interview-to-graph-mvp-v0.1.md): operator-first design for turning interviews into reviewed graph artifacts using existing tools.
- [KOI federation operations runbook](./koi-federation-operations-runbook.md): operational peering, bootstrap, and troubleshooting for KOI nodes.

## Graph-First Mapping
- [Bioregional mapping model v0.1](./bioregional-mapping-model-v0.1.md): graph-first profile over the current BKC / Octo bridge ontology.
- [Bioregional mapping intake contract v0.1](./bioregional-mapping-intake-contract-v0.1.md): docs-level canonical packet plus transport guidance for the current `/ingest` endpoint.
