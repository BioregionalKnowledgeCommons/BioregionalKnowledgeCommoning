# GE / CLC Integration

How Bioregional Knowledge Commons (BKC) interfaces with Grassroots Economics (GE), the Commitment Pooling Protocol (CPP), and the Cosmo-Local Credit (CLC) DAO.

BKC provides **off-chain curation and routing intelligence**. GE/CLC provides **on-chain settlement and execution**. These docs describe the bridge between them.

## Reading Order

1. **[Compatibility Memo](./compatibility-memo.md)** — Start here. Maps BKC concepts to GE/Sarafu production patterns and CLC DAO design. Concept mapping table, contract interfaces, governance decomposition (Create/Pledge/Verify), compatibility assessment.

2. **[CLC Questions Synthesis](./clc-questions-synthesis.md)** — Formalized Q&A from whitepaper analysis. Ten questions (layering, confederation, portfolio pools, attestation, multi-objective routing, time-aware planning, onboarding, composability, mapping protocol, decision ladder) with working answers and open questions.

3. **[CLC Integration Strategy](./clc-integration-strategy.md)** — Three-phase technical roadmap. Phase 1: assetization + path construction (partially done during hackathon). Phase 2: selective on-chain representation. Phase 3: upstream intelligence provider with agent-mediated routing.

4. **[Intent Publication & Agent-Mediated Routing](./intent-publication.md)** — Proposal (draft). Generalizes the CPP whitepaper's pool-level "rebalance intents" to users and communities. Typed intents (SWAP, WANT, OFFER, CONDITIONAL), agent roles, mapping workshop integration, privacy model. Relates to DeFi intent-centric architectures (Anoma, ERC-7683, CoW) and Will Ruddick's "Physics of Intention" — convergent design from different starting points.

5. **[MVIS Pilot Spec](../../pilots/front-range-cascadia-2026/mvis-pilot-spec.md)** — Operational contract for the Cascadia pilot (May–July 2026). Scoped intent types (OFFER, WANT, SWAP), hybrid intake workflow, coordinator-vetted matching, state model, controlled vocabulary, success criteria.

## Relationship to Foundations

The [foundations/](../foundations/) docs describe BKC's own architecture — commitment pooling, flow funding, pattern language, federation, ontology. This directory describes how that architecture *interfaces with* the GE/CLC ecosystem. Cross-references flow both ways:

- Foundations → here: commitment-economy-design.md and commitment-economy-vision.md reference intent publication as the mechanism for making needs compositional.
- Here → foundations: integration strategy and questions synthesis reference commitment-pooling-foundations.md for the lifecycle model and three orthogonal operations.

## Key Principle

BKC is upstream; CLC is downstream. BKC selects *which* routes to quote (semantic scoring, bioregion fit, consent boundaries). CLC executes *how* settlement happens (token vaults, multi-hop swaps, fee waterfall). The intent publication layer sits between them — persisting desires that the synchronous router would otherwise forget.
