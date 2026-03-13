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
- `consent_tier`: local governance-defined exposure class. Current values: `public`, `restricted`, `community_only`, `private`.
- `steward_authority`: who can approve/revoke sharing.
- `allowed_uses` / `restricted_uses`: machine-actionable permissions.
- `review_or_expiry_policy`: whether access terms are permanent, periodic, or time-bound.
- `provenance_evidence`: references to decision records, meeting records, or policy artifacts.

### Technical Enforcement of consent_tier

The `consent_tier` slot is not advisory — it is enforced at the database level in the KOI backend:

- `public` and `restricted`: entities are registered with `visibility_scope = "public"` and `node_private = false`. They appear in public search, chat, API responses, and are eligible for federation.
- `community_only` and `private`: entities are registered with `visibility_scope = "node_private"` and `node_private = true`. They are hidden from all public query endpoints (`/entity-search`, `/chat`, `/entities`, `/stats`, GraphRAG), excluded from federation (no `koi_rid` assigned), and not published to the Quartz site. Node operators can still query them directly in the database.

This enforcement is implemented in the interview-commoning plugin and the `/register-entity` backend endpoint. See `Octo/docs/interview-commoning-mvp.md` for the full tier-to-visibility mapping.

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
