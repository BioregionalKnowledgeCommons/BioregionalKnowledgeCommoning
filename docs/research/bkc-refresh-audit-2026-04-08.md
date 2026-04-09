---
doc_id: bkc.refresh-audit-2026-04-08
doc_kind: research
status: active
depends_on:
  - bkc.project-vision
  - bkc.federation-overview
  - bkc.federated-memory-arch
  - bkc.commitment-economy-vision
  - bkc.coordination-stack
---

# BKC Refresh Audit

## Scope

This memo records the first bounded-context audit after substantial upstream work in Spore and Intelligence Commons. It does not revise BKC canon directly. It establishes what BKC now appears to own, what should remain upstream, and the recommended sequence for a BKC repo refresh.

## Current Read

BKC is no longer the upstream grammar layer. Spore now carries more of the abstract coordination grammar, and Intelligence Commons now carries more of the intelligence-primitives layer. BKC still matters, but its center of gravity is now more specific:

- bioregional knowledge commoning
- reference profiles and implementation-facing federation docs
- commitment economy and capital-layer application in bioregional settings
- pilots, operational evidence, and public proving-ground surfaces
- concrete deployment seams across knowledge, coordination, and capital planes

That is a strong bounded context. It does not need to compete with Spore or IC by being more abstract than they are.

## What BKC Should Likely Own

### 1. Bioregional deployment framing

BKC should explain how commons infrastructure lands in real bioregional settings:

- landscape groups
- pilot structures
- onboarding and participation profiles
- knowledge sovereignty in place
- public/commoning interfaces

### 2. Reference profiles and implementation contracts

BKC is a good home for:

- meta-protocol application in bioregional deployments
- CommonsChange and other profile work
- mapping intake contracts
- consent/data-classification operationalization
- federation runbooks and deployment guidance

### 3. Commitment economy in situated use

BKC should likely keep the commitment-economy layer where it is tied to:

- bioregional coordination
- pilot structures
- threshold-based redistribution and local pools
- evidence loops tied to actual regional work

### 4. Operational and public proving grounds

BKC/Octo should remain the place where:

- public surfaces are tested
- pilots generate evidence
- real coordination artifacts are exposed
- operational commitments eventually become visible

## What Should Stay Upstream

### Spore

Spore should remain authoritative for:

- abstract coordination grammar
- general learning membrane pattern
- claims / evidence / attestation grammar
- federation grammar at the most general level
- broad multi-agent / collective-agency philosophy

### Intelligence Commons

IC should remain authoritative for:

- retrieval and memory layer abstractions
- grounding / evidence primitives for intelligent systems
- agentic control and intelligence-specific patterns
- general intelligence architecture not specific to bioregional commoning

## Current BKC Risks

### 1. Overlap drift

Several BKC docs appear to carry language that now overlaps with Spore and IC without clearly naming the authority boundary. That is manageable, but it creates drift risk if BKC continues to restate upstream abstractions instead of referencing them.

### 2. Mixed registers

The repo contains:

- active canon docs
- research synthesis and external-model notes
- operations material
- public-facing positioning
- pilot artifacts

That is not inherently bad, but the repo entry points need to distinguish these layers more clearly.

### 3. Dirty worktree

There are already uncommitted edits and new files in the repo, including:

- `docs/foundations/CLAUDE.md`
- `docs/ops/technique-ledger.md`
- `docs/coordination-stack.md`
- several new `CLAUDE.md` files

Any refresh pass needs to work with those changes rather than steamrolling them.

## Recommended Refresh Sequence

### Step 1. Index BKC into KOI and establish a baseline

Do this first so review work is queryable across the portfolio.

### Step 2. Review the entry points

Audit and likely refresh these first:

- `README.md`
- `docs/project-vision.md`
- `docs/coordination-stack.md`
- `docs/foundations/README.md`

Goal:

- make BKC’s bounded context explicit
- reduce ambiguity about what is upstream in Spore / IC
- clarify public/proving-ground vs canon vs research material

### Step 3. Review core foundation docs by disposition

For each major foundation doc, choose one:

- keep and refresh in BKC
- narrow to bioregional/deployment scope
- retain but add explicit upstream references
- archive / deprecate

Priority candidates:

- `federated-memory-architecture.md`
- `federation-overview.md`
- `knowledge-commoning-meta-protocol-v0.1.md`
- `commitment-economy-vision.md`
- `commitment-economy-design.md`
- `commitment-pooling-foundations.md`
- `live-retrieval-architecture.md`

### Step 4. Clean canon hygiene

- missing or weak `depends_on`
- cross-repo references to Spore / IC where appropriate
- status normalization (`active`, `draft`, etc.)
- roadmap/doc-graph consistency

### Step 5. Reindex and rerun health

After the review pass, rerun KOI indexing and the portfolio knowledge health report to establish the post-refresh baseline.

## Immediate Recommendation

Treat BKC as:

- downstream from Spore for coordination grammar
- downstream from IC for intelligence primitives
- primary for bioregional application, reference profiles, pilots, and proving-ground implementation

That framing is strong enough to justify a repo refresh now.

## Guardrails

- do not erase the bioregional specificity by making BKC a thin mirror of Spore
- do not let BKC continue to carry upstream abstractions as if it owns them
- preserve operational/public proving-ground value
- prefer explicit references to Spore and IC over silent duplication
- respect existing in-progress edits during the refresh pass
