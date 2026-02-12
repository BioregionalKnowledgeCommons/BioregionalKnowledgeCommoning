# Knowledge Commoning Meta-Protocol v0.1

## Purpose
Define the minimum interoperability commitments for bioregional knowledge commoning without imposing a single stack or ontology.

This is a thin protocol layer, not a full data model.

## Core Invariants
Any artifact shared across boundaries must answer three questions:
1. What is shared?
2. Who attests to it?
3. Who can use it, and how?

## Required Artifact Fields (Abstract)
Every conforming artifact must include:
- `artifact_id`: stable identifier within the source context
- `payload`: content or reference to content
- `attestations`: provenance statements (author/contributor/reviewer/system process)
- `rights_and_consent`: usage and access metadata
- `published_at`: publication or change timestamp

Optional but recommended:
- `local_type`
- `canonical_type`
- `mapping_context`
- `valid_from` / `valid_to`

## Exchange Modes

### 1. Event Mode
Use when a node emits changes over time.
- Expected semantics: create/update/delete style events.
- Useful for near-real-time sync.

### 2. Snapshot Mode
Use when a node publishes state/catalog exports.
- Expected semantics: periodic full or partial state publication.
- Useful for static or low-frequency systems.

A conforming participant may support one mode or both.

## Conformance Levels

### L0: Declaration
- Publicly declares intent to conform.
- Documents how it satisfies the three invariants.

### L1: Machine-Readable Exchange
- Emits machine-readable artifacts with required fields.
- Supports at least one exchange mode.

### L2: Bidirectional Interoperability
- Can ingest and emit interoperable artifacts.
- Has conflict handling + audit trail for cross-boundary updates.

## Non-Goals
- Defining one universal ontology.
- Requiring KOI, GitHub, Opal, Murmurations, or any specific transport.
- Defining universal rights/licensing values.

## Governance Hooks
This meta-protocol requires the presence of rights/consent metadata but does not prescribe local values.

Community governance determines:
- valid value vocabularies
- who can approve publication
- reclassification and revocation rules

## Relationship to Reference Profiles
Reference profiles (for example `CommonsChange`) are concrete ways to implement this meta-protocol.

Passing a reference profile implies meta-protocol compatibility; meta-protocol compatibility does not require a specific reference profile.

## Versioning
- Version: `v0.1`
- Compatibility policy: backward compatibility at invariant level; profile-level breaking changes are versioned separately.
