# Ontology Commoning Ops v0.1

## Purpose

Translate the ontology-commoning philosophy into an operational workflow for BKC pilots.

This document explains how local concepts, mapping proposals, and ontology extensions should move through review and publication.

## Operating Position

- the current BKC / Octo ontology is the shared bridge layer
- local and domain ontologies remain valid and visible
- mapping is negotiated, not imposed
- ontology growth should emerge from repeated practice and comparison
- no auto-publication of unreviewed ontology decisions

## Roles

### Source steward
Owns the local context and determines what can be shared.

### Extractor or proposer
Produces the initial mapping proposal from transcript, note, packet, or dataset.

### Reviewer
Evaluates mapping quality, consent boundaries, and semantic fit.

### Publisher
Applies approved mappings in shared artifacts or interoperable packets.

## Core Artifacts

Every ontology-commoning workflow should be able to produce these artifacts:

1. source profile
2. mapping proposal
3. review packet
4. decision record
5. extension candidate, if needed

## Recommended Pilot Storage Pattern

For pilot work, use these repo paths when the artifacts are shareable:

- `pilots/front-range-cascadia-2026/mappings/proposals/`
- `pilots/front-range-cascadia-2026/mappings/decisions/`
- summary of accepted decisions in `pilots/front-range-cascadia-2026/decision-log.md`

Restricted artifacts should remain local-first and private.

## Mapping Proposal Shape

A mapping proposal should include:

- source artifact identifier
- source ontology identifier
- source term
- local type
- proposed canonical type
- proposed relation mappings if relevant
- confidence
- rationale
- consent notes
- reviewer status

## Allowed Mapping Outcomes

- `equivalent`
- `narrower`
- `broader`
- `related`
- `unmapped`
- `proposed_extension`

## Decision Rules

### Use `equivalent` when

- the source concept and bridge concept are close enough in meaning and use
- downstream use will not distort the source concept

### Use `narrower` when

- the source concept is more specific than the bridge concept

### Use `broader` when

- the source concept is more general than the bridge concept

### Use `related` when

- there is meaningful conceptual overlap but not safe equivalence

### Use `unmapped` when

- no bridge concept is good enough
- forcing a mapping would erase important meaning

### Use `proposed_extension` when

- the concept recurs across sources or bioregions
- the concept matters for interoperability or repeated analysis
- the current bridge ontology is missing something genuinely useful

## What Can Be Auto-Suggested

Allowed for automation:

- exact string matches to existing mapped concepts
- previously approved mappings reused with the same source ontology profile
- low-risk suggestions for reviewer consideration

Not allowed for automation:

- automatic publication of new mappings
- automatic publication of extension proposals
- automatic flattening of Indigenous or sensitive concepts
- automatic cross-boundary publication of restricted concepts

## Triggers for Review

A mapping review must be triggered when:

- a new `local_type` appears
- a concept is marked `unmapped`
- a concept is marked `proposed_extension`
- consent status is unclear
- a low-confidence canonical mapping would affect publication
- a local concept might be important across multiple bioregions

## Review Workflow

1. profile the source artifact or source ontology
2. generate mapping proposal
3. triage low-risk and high-risk items
4. run human review
5. record decisions with rationale
6. publish only the approved bridge-compatible subset
7. queue unresolved or extension items for later review

## Consent Intersections

Ontology review is not separate from governance.

Before a concept crosses boundaries, review must check:

- whether the concept is allowed to cross the boundary at all
- whether the mapped form changes the meaning in a harmful way
- whether the source community or steward has approved that level of abstraction

If the answer is no, keep the concept local.

## When a Local Type Should Stay Local

A local type should remain local when:

- it is meaningful only within a specific local governance or cultural context
- mapping would produce false equivalence
- publication would violate consent or sovereignty expectations
- cross-bioregion interoperability benefit is weak compared with semantic loss

Remaining local is a valid and successful outcome.

## Extension Candidate Rules

A `proposed_extension` should only move toward the bridge ontology when all are true:

- it appears repeatedly across artifacts, not just once
- it matters to cross-bioregion learning or interoperability
- reviewers can articulate what problem it solves
- the extension does not collapse important local distinctions
- there is reviewer sign-off recorded with rationale

## Publication Rule

Only the bridge-compatible projection of an artifact should cross bioregion boundaries by default.

The source layer should remain preserved alongside:

- `source_ontology`
- `local_type`
- `canonical_type`
- `mapping_status`
- `mapping_notes`
- decision rationale

## Operational Metrics

Use these simple metrics to see whether ontology-commoning is healthy:

- number of new local types encountered
- number of approved mappings
- number of `unmapped` concepts preserved
- number of extension proposals raised
- review turnaround time
- number of rejected mappings due to consent or semantic distortion

## Success Criteria

This ops model is working if:

- local concepts are preserved instead of erased
- reviewers can explain why a mapping was chosen
- collaborators can contribute without adopting one total ontology
- the bridge ontology evolves from repeated practice rather than speculation alone
