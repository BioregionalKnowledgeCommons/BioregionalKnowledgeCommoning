# Interview-to-Graph MVP v0.1

## Purpose

Define the first BKC interview-to-graph pipeline that supports the Practices & Patterns project without requiring major new runtime infrastructure.

Goal: process one interview end to end.

`recording -> transcript -> QA -> extraction bundle -> mapping review -> governed ingest -> searchable graph`

## Why This Matters Now

The BKC CoIP Practices & Patterns project is not just a research effort. It is one of the main drivers of ontology emergence, pattern discovery, and cross-bioregion learning.

A working interview-to-graph path would:

- turn interview knowledge into reusable graph artifacts
- make practices comparable across bioregions
- surface ontology differences instead of hiding them
- create a durable substrate for later mapping, pattern mining, and evidence loops

## Design Constraints

- raw recordings and sensitive transcripts stay local-first
- no auto-publication without consent metadata
- ontology mappings are proposed, not asserted as final truth
- use existing BKC and KOI surfaces where possible
- ship an MVP around one real interview, not a generalized platform

## Existing Building Blocks

### Already available

- BKC transcription pipeline doc
- `darren-workflow` transcript retrieval and meeting-note patterns
- `darren-workflow` entity extraction and linking workflow
- `personal-koi-mcp` support for BKC entity types
- existing BKC `/ingest` contract and partner quickstart
- live KOI graph and search surfaces
- provenance receipts from ingest

### Still missing

- BKC-specific interview intake record
- explicit consent validation step before extraction and publication
- ontology review queue for local-to-canonical mappings
- local-first storage policy for interview artifacts
- clear operator workflow tying all pieces together

## MVP Scope

### In scope

- one interview processed end to end
- transcript with speaker attribution where available
- human QA pass
- extraction of practices, patterns, questions, claims, evidence, organizations, projects, locations, concepts
- ontology review for `local_type` and `canonical_type`
- governed ingest of approved subset
- resulting entities searchable in BKC / KOI

### Out of scope

- full interview management system
- auto-publication of all extracted content
- automated pattern approval
- automatic ontology extension publication
- new public API endpoints

## Canonical Data Position

The canonical target is the existing BKC graph using the current shared bridge ontology and mapping workflow.

The interview does not create ontology truth directly. It creates:

- candidate entities
- candidate relationships
- candidate practices and patterns
- candidate ontology mappings
- candidate extension proposals

## Pipeline Stages

## Stage A: Intake

Purpose:
register the interview before any processing.

Required metadata:

- `interview_id`
- date
- participants and roles
- bioregion
- project or cohort
- consent tier (`public`, `restricted`, `community_only`, or `private`)
- allowed uses
- reviewer identity
- source location of recording or transcript

Output:
- intake record
- permission to proceed or hold

Human gate:
- yes

Decision rule:
- if consent metadata is incomplete, stop here
- consent tier determines downstream visibility: `community_only` and `private` produce entities with `node_private = true`, hidden from all public search, chat, API, and federation endpoints

## Stage B: Transcript Acquisition

Purpose:
produce a usable transcript package from the available source.

Allowed sources:

- MacWhisper file
- Otter transcript
- manually supplied transcript
- future external transcript provider

Required output:

- transcript text
- timestamps where available
- speaker attribution where available
- transcript source metadata

Reuse from existing tooling:
- `darren-workflow` transcript retrieval patterns

Human gate:
- no, unless source ambiguity needs resolution

## Stage C: QA and Redaction

Purpose:
clean the transcript before extraction or publication.

Tasks:

- correct speaker names
- correct obvious transcription errors
- redact sensitive passages if required
- mark passages that cannot cross boundaries

Required output:

- reviewed transcript
- review timestamp
- reviewer name
- redaction notes

Human gate:
- yes

Decision rule:
- only the reviewed transcript proceeds to extraction

## Stage D: Structured Extraction

Purpose:
produce a candidate graph bundle from the reviewed transcript.

Extract:

- `Person`
- `Organization`
- `Project`
- `Location`
- `Concept`
- `Practice`
- `Pattern`
- `Protocol`
- `Playbook`
- `Question`
- `Claim`
- `Evidence`
- `Meeting` or interview-session entity if useful

Also extract:

- candidate relationships
- candidate `local_type` values
- candidate `canonical_type` values
- low-confidence items
- repeated local terms that may need review

Required output:
- extraction bundle JSON
- confidence notes
- unresolved terms list

Reuse from existing tooling:
- `darren-workflow` extraction and entity-linking patterns
- `personal-koi-mcp` entity vocabulary

Human gate:
- no at extraction time, yes before publication

## Stage E: Ontology and Mapping Review

Purpose:
review how local concepts relate to the current bridge ontology.

Review decisions:

- `equivalent`
- `narrower`
- `broader`
- `related`
- `unmapped`
- `proposed_extension`

Required review artifacts:

- approved entities
- approved relationships
- rejected entities with rationale
- unresolved items queue
- extension candidates queue

Human gate:
- yes

Decision rules:

- no forced canonicalization
- `unmapped` is valid
- sensitive concepts may remain local even if technically mappable
- repeated local terms can be elevated to `proposed_extension`

## Stage F: Governed Ingest

Purpose:
write the approved graph-compatible subset into BKC.

Transport target:
- current BKC `/ingest`

Submitted subset:

- `document_rid`
- `source`
- `content`
- approved `entities`
- approved `relationships`

Preserved outside the current endpoint:

- consent and review metadata
- source ontology profile
- local type detail
- mapping rationale
- unresolved items

Required output:

- canonical entities response
- `receipt_rid`
- searchable graph entries

Human gate:
- yes, because approval precedes ingest

## Stage G: Publication and Projection

Purpose:
make the approved knowledge usable.

Possible outputs from the same canonical graph:

- graph view
- map view
- table / review view
- Quartz narrative summary
- later pattern cards or case study pages

Human gate:
- yes for public publication where consent requires it

## Storage Policy

### Local-first private layer
Keep these outside the public repo by default:

- raw recordings
- raw transcripts
- unredacted reviewed transcripts
- restricted consent artifacts

### Publishable shared layer
Allow these to enter shared repo or graph if approved:

- approved mapping packets
- approved extraction bundles
- approved summary notes
- decision records and mapping rationale

## Suggested MVP Outputs

A successful first run should produce:

1. one intake record
2. one reviewed transcript
3. one extraction bundle
4. one mapping review packet
5. one approved ingest call
6. one set of searchable graph entries
7. one short public or semi-public summary artifact

## Suggested Implementation Path

### Phase 1: Operator-run MVP
Use existing tools manually or semi-manually.

- operator gathers transcript
- operator runs extraction workflow
- human reviews mapping packet
- operator submits approved subset to `/ingest`

### Phase 2: BKC-specific orchestration
Only after one successful run, decide whether to productize as:

- new workflow in `darren-workflow`
- new shared command or skill
- lightweight adapter around KOI ingest

## Success Criteria

The MVP succeeds if:

- one interview is processed end to end
- consent metadata is present and validated
- at least one `Practice` and one `Question` are extracted and approved
- at least one local term survives review without forced flattening
- approved entities are searchable in BKC after ingest
- publication blocks if consent metadata is missing

## Failure Modes

| Failure mode | Expected response |
|---|---|
| missing consent metadata | stop before extraction or publication |
| transcript quality too low | hold for correction or manual transcript |
| ambiguous ontology mapping | mark `unmapped` or `related`, do not force |
| sensitive concept cannot cross boundary | preserve locally, exclude from ingest |
| repeated duplicate entities | rely on current entity resolution and review |

## Consent Tier Enforcement

The consent tier set at intake (Stage A) determines how published entities are treated by the infrastructure:

| Tier | `visibility_scope` | Public API | Federation | Quartz |
|---|---|---|---|---|
| `public` | `public` | Visible | Eligible | Published |
| `restricted` | `public` | Visible | Eligible | Published |
| `community_only` | `node_private` | Hidden | Blocked | Workspace only |
| `private` | `node_private` | Hidden | Blocked | Workspace only |

This is enforced at the database level via `node_private = true` on `entity_registry`. All public query paths (`/entity-search`, `/chat`, `/entities`, `/stats`, GraphRAG) filter out `node_private` entities. No `koi_rid` is assigned to `community_only` or `private` entities, so they never enter federation.

See `Octo/docs/interview-commoning-mvp.md` for implementation details.

## Relationship to the Current Bridge Ontology

This MVP does not replace the current BKC / Octo ontology.

It uses that ontology as the bridge layer and adds the operational review workflow needed to support ontological commoning in practice.
