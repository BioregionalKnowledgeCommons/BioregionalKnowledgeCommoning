# Rights, Licensing, and Consent Policy Slots

## Purpose
Provide required governance metadata slots for interoperability without prescribing universal values.

This is a slot framework, not a universal rights framework.

## Required Slots
Every publishable artifact should include:
- `consent_tier`
- `steward_authority`
- `allowed_uses`
- `restricted_uses`
- `attribution_requirements`
- `review_or_expiry_policy`
- `provenance_evidence`

Optional but recommended:
- `jurisdiction`
- `community_protocol_ref`
- `revocation_process_ref`

## Slot Semantics
- `consent_tier`: local governance-defined exposure class.
- `steward_authority`: who can approve/revoke sharing.
- `allowed_uses` / `restricted_uses`: machine-actionable permissions.
- `review_or_expiry_policy`: whether access terms are permanent, periodic, or time-bound.
- `provenance_evidence`: references to decision records, meeting records, or policy artifacts.

## Governance Process Requirements
Before publishing across boundaries, each pilot/node must define:
1. How consent tiers are assigned.
2. Who can approve tier changes.
3. How reclassification/revocation occurs.
4. How audit evidence is recorded.

## Indigenous Sovereignty Integration Points
This framework must be compatible with community-led application of:
- FPIC workflows
- OCAP-aligned governance constraints
- CARE-aligned stewardship principles
- TK labels/notices where applicable

The framework does not prescribe specific values for these systems.

## Non-Goals
- Defining one global license taxonomy.
- Assuming CC licenses are always appropriate.
- Encoding governance outcomes in code before communities define them.

## Minimum Validation
- Required slots present.
- No artifact published externally without steward authority value.
- No artifact published externally without consent tier value.
