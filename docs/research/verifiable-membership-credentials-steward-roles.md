---
doc_id: bkc.connection.verifiable-membership-credentials-steward-roles
doc_kind: research
status: draft
disposition: implementation hypothesis
depends_on:
  - bkc.meta-protocol
  - bkc.commitment-pooling
  - bkc.federated-memory-arch
  - bkc.live-retrieval-arch
relates_to:
  - spore.connection.decentralized-trust-graph-credential-pairs
  - bkc.connection.neighbourhoods-runtime-layer
  - bkc.federation-overview
concepts:
  - membership-credential
  - authority-credential
  - steward-authority
  - consent-tier
  - revocation-quorum
  - verifiable-trust-community
external_sources:
  - title: "Trust over IP Explainer with Kaliya Young (Protocols of Place workshop)"
    url: https://youtu.be/AelpLS2pY18
    published: "2026-10-04"
  - title: "OpenVTC Ecosystem Overview"
    url: https://openvtc.github.io/wiki/overview
    published: "2026-10-08"
  - title: "Verifiable Relationship Credentials (VRCs), ToIP Decentralized Trust Graph WG"
    url: https://lf-toip.atlassian.net/wiki/spaces/HOME/pages/258113643
    published: "2025-09-24"
  - title: "Sideways Verifiable Community, Specifications Document v1.2"
    url: https://github.com/SidewaysEarth/VerifiableCommunity
    published: "2025-07-01"
  - title: "Sideways: Verifiable Community"
    url: https://sideways.earth/verifiable-community/
    published: "2024-06-01"
  - title: "Project Weave: technical depth"
    url: https://projectweave.tech/technical-depth.html
  - title: "Free Our Groups: From Platforms to Protocols (Kaliya Young)"
    url: https://identitywoman.net/free-our-groups-from-platforms-to-protocols/
    published: "2026-07-07"
  - title: "Who Is Tending the Digital Substrate for Bioregional Movements? (Kaliya Young and David Hodgson)"
    url: https://identitywoman.net/who-is-tending-the-digital-substrate-for-bioregional-movements/
    published: "2026-05-25"
---

# Membership and role credentials as the referent for BKC's community and steward slots

## Why this note exists

This note reads the Decentralized Trust Graph (DTG) work that Kaliya Young and Drummond Reed presented in a public
[Trust over IP explainer](https://youtu.be/AelpLS2pY18) (video published 2026-10-04) against two
of BKC's governance slots. It uses the public specifications and implementation pages the talk
points to. It concerns community membership and roles only. Person-to-person trust is discussed
only where it shapes membership.

## Two slots that name a set of people

The [meta-protocol](../foundations/knowledge-commoning-meta-protocol-v0.1.md#core-invariants)
requires every shared artifact to answer "Who attests to it?" and "Who can use it, and how?"
(lines 22-23). It leaves "who can approve publication" and "reclassification and revocation
rules" to community governance
([Governance Hooks](../foundations/knowledge-commoning-meta-protocol-v0.1.md#governance-hooks),
lines 75-78). The [policy slots](../foundations/rights-licensing-consent-policy-slots.md#slot-semantics)
make two of those answers concrete: `consent_tier` includes `community_only` (line 24), and
`steward_authority` is "who can approve/revoke sharing" (line 25). `revocation_process_ref` is
optional (line 21). Every node profile must "define steward authority" and a
"reclassification/revocation workflow" before cross-node publication
([node-participation-profiles](../foundations/node-participation-profiles.md#governance-prerequisite-all-profiles),
lines 73-74).

Both slots name a set of people, and today both resolve inside one node.

- `community_only` and `private` are enforced identically. Both become
  `visibility_scope = "node_private"`, hidden from every public endpoint and queryable by node
  operators in the database (policy slots, line 35). The enforcement has no member identity to
  check, so the two tiers currently have the same audience.
- Steward authority is a per-node `commons_memberships` table with WebAuthn passkey login, and
  reviewer identity "is a database-level identity, not an on-chain identity"
  ([pacto-bkc-convergence-v0.1](./pacto-bkc-convergence-v0.1.md#gap-5-dao-dao-governance-integration-is-missing),
  lines 250-256). That document rates this "honestly, the least" BKC has (line 247) and lists
  "Cross-DAO authorization for inter-bioregion attestation" as not addressed (line 270).
- The deployed retrieval router's PolicyScope runs with "currently no auth identity" and is to
  "derive from `commons_memberships` + edge governance tables when WebAuthn auth identity is
  threaded to the retrieval path"
  ([live-retrieval-architecture](../foundations/live-retrieval-architecture.md#layer-1-policyscope-deterministic-no-llm),
  lines 98-101). The architecture derives PolicyScope "from caller identity"
  ([federated-memory-architecture](../foundations/federated-memory-architecture.md#policyscope),
  line 55).

## What the trust-graph work offers

In the talk, "the community itself can be an entity in this network of nodes, and the community
can issue credentials, a verifiable membership credential of belonging to a community" [14:40].
Issuance should not rest on one person: "we need [multi-sigs] on the wallets that issue these
credentials and community stewardship of community credential issuance" [15:39]. The public
specifications fill in that shape.

- **Membership is two signed acts.** In the OpenVTC ecosystem ("OpenVTC" below means the
  ecosystem, not only its app), "Membership is a bi-directional pair: a grant
  from the community and an acknowledgement from the member"
  ([ecosystem overview](https://openvtc.github.io/wiki/overview), "Layer 4: Trust Credentials").
  This follows the DTG relationship pattern. A relationship is two credentials, one issued each
  way and each signed only by its issuer, and "it's not one credential that we're both signing"
  [13:24] ([ToIP VRC page](https://lf-toip.atlassian.net/wiki/spaces/HOME/pages/258113643),
  note 1). The Sideways spec gives members "the right to reject a VC"
  ([Verifiable Community spec](https://github.com/SidewaysEarth/VerifiableCommunity), "Notify
  member of their VC"). BKC already asks for the member's half in pools. Its Consent Boundary
  Pattern says "Pool membership and data sharing require explicit pledger consent at each scope"
  ([commitment-pooling §5.3](../foundations/commitment-pooling-foundations.md#53-pattern-language-alignment),
  line 187). Carrying that from pool membership to commons membership is this note's extension.
- **Roles are separate credentials.** In OpenVTC a community's roles (vetter, maintainer and
  custom roles) "are authority credentials", and an authority credential is "a statement to a
  verifier of what a holder may do" (same section). OpenVTC's membership credential means more
  than standing. It is proof of "a real, unique human within a community". On this note's
  reading, Sideways' default types are closer to BKC's case: "Membership (In good standing),
  Trusted Membership, and Provisionary membership" (spec, "Issuer: Defining credentials and
  issuance requirements").
- **Issuance and revocation share a quorum.** Sideways asks for administrator capabilities "that
  require X of N permissions and multiple equal admins" (spec, "Issuer: Defining credentials and
  issuance requirements"), and "The procedure for revocation is the same as for adding a new
  member, including the approvals process" (spec, "Revoke membership, upgrade or downgrade"). In OpenVTC, "consequential actions wait in an
  action list until the N-th approval" (overview, "Where Things Are Heading").
- **The member holds the credential, and it can travel.** Sideways has "No central database
  whatsoever" because "each person holds their own" (spec, "Defaults"). Project Weave describes
  the trust graph as letting "trust earned in one community context be portable to another
  without merging governance" ([technical depth](https://projectweave.tech/technical-depth.html)).
  Sideways gives a network form: "The ecovillage network provides membership or citizenship to
  anyone who belongs to any of its authorized member organizations"
  ([Verifiable Community](https://sideways.earth/verifiable-community/)).
- **Group memory is gated the same way.** OpenVTC data rooms are "a credential-governed,
  MLS-encrypted space that its members' agents can also recall from" (overview, "Layer 5: The
  User Experience"). Kaliya's "group brain" is "a shared repository of a group's collective
  knowledge", which for platform-bound groups "lives on someone else's servers, under someone
  else's terms of service"
  ([Free Our Groups](https://identitywoman.net/free-our-groups-from-platforms-to-protocols/)).
  BKC already scopes memory recall by a PolicyScope "derived from caller identity, system policy,
  and membrane governance"
  ([federated-memory-architecture](../foundations/federated-memory-architecture.md#policyscope),
  line 55). Reading data rooms and BKC's scoped memory as two homes for a group brain is this
  note's inference. Kaliya does not link the term to data rooms.

## Hypothesis

For whoever takes up steward authority or cross-node consent. Nothing here is decided or changed.

1. **Read the two slots as naming two credential types.** `community_only` would mean readable by
   holders of the commons' current membership credential, which separates it from `private`.
   `steward_authority` would name a role credential and its issuing quorum, not a row in one
   node's `commons_memberships` table. Keeping membership and role apart follows the
   OpenVTC split and keeps every member from becoming a steward.
2. **Point `revocation_process_ref` at revocation by the issuing quorum**, as in Sideways. The
   optional slot would then have a default that is not node-local.
3. **Feed a verified presentation into PolicyScope** at the point live-retrieval-architecture
   already reserves for an auth identity (line 101). `commons_memberships` could remain as one
   node's cache of verified credentials.
4. **Let membership cross nodes by an acceptance rule**, in the Sideways network form. A node
   recognizes members of named peer commons, so membership travels without one shared table and
   without merging node governance.

**Boundary.** Membership and roles gate who may read, approve and revoke. They do not grant the
right to promise. "The right to promise is not granted by a pool or a steward"
([commitment-pooling §7.1](../foundations/commitment-pooling-foundations.md#71-create--self-sovereign-promise-issuance),
line 221). A role credential could identify who counts as "a steward or peer" for the VERIFIED
transition (line 235), but trust in a commitment still "emerges from witnessed follow-through,
not pre-approval" (line 237). Member credentials are also a separate layer from node identity,
which BKC already lists separately from steward roles
([bioregional-swarm-telos](../bioregional-swarm-telos.md#the-three-planes), line 55). The talk's
other stewardship credential is a different thing. Kaliya presents as "Frank's work" [21:30]
credentials "about your care and stewardship of land", with the land itself, through an installed
mesh network, as issuer. Those attest to work done. `steward_authority` names who may approve and
revoke.

## Limits

- **The recipes are not stable.** Kaliya describes three code bases still being made to
  interoperate [18:22] and says "in about 2 years those protocols will freeze" [19:54]. The DTG
  Credentials Core Specification is at Working Draft 02 (September 2026), and the ecosystem's
  latest coordinated release, Eucalyptus, spanned eighteen repositories and "close to two
  thousand commits, two hundred of them breaking" (overview). OpenVTC calls the Keyring wallet
  "the stack's second independent implementation of the vetting protocol and a steady source of
  conformance findings". This note pins no format and no implementation.
- **The talk deferred revocation.** Asked how to untrust someone, the response was that
  "Revocation of your credential and removal from a trust registry" raised "much more
  complicated questions", and the talk moved on [14:21]-[14:31]. The specifications say who
  revokes (the issuer, ToIP VRC note 3, or the quorum, Sideways). None of the sources read here
  says how a revocation reaches nodes that cache membership.
- **A roster is sensitive.** Kaliya Young and David Hodgson's warning about public impact claims applies to a
  membership roster too, on this note's reading: "a public, verifiable record of 'this community
  is doing conservation work on this land' is also a map for retaliation"
  ([Who Is Tending the Digital Substrate](https://identitywoman.net/who-is-tending-the-digital-substrate-for-bioregional-movements/)).
  The OpenVTC overview notes that "the spec recommends ZKP presentation by default" ("The Big
  Picture"), and the Sideways defaults include "No immutable or public records". A
  `community_only` check should verify a presentation without publishing who holds the credential.
- **Issuance terms stay with each community.** The policy slots must stay compatible with
  community-led FPIC, OCAP, CARE and TK practice (lines 46-53). This note maps no community's
  governance onto credential issuance.
- **Untested in BKC.** No BKC node issues or verifies credentials. Items 1 and 3 would change
  the line-35 enforcement and the PolicyScope input. Neither is proposed here as a schema change.

## Open questions

1. Which credential format would a BKC node verify? OpenVTC's Verifiable Trust Agent holds W3C
   Data Integrity, BBS, SD-JWT and ISO mdoc credentials (overview, "Layer 2"), and its mediator
   speaks DIDComm v1 for Keyring and the wider Aries/Credo world ("Layer 3").
2. How does a login bind to the key that holds credentials? A WebAuthn passkey is scoped to the
   site that registered it, so a steward passkey shows control of an account on that site, not
   membership in a commons. OpenVTC's VTA Wallet browser plugin is one pattern: a passkey
   ceremony logs the user in "as the controller of your VTA DID", and "keys never leave the VTA"
   ("Layer 5").
3. How does that key relate to the identities BKC already records, `reviewer_uri` and the
   designed on-chain `attestor_address` (pacto-bkc-convergence-v0.1, lines 255 and 262-263)?
4. Who issues: the commons node, the contributing nodes, or a federation of commons? In BKC's
   federation guide a commons is a node of its own. Personal nodes contribute to it and "a
   commons admin approves or rejects" (line 525), and a federation connects "multiple commons
   nodes" (line 527) ([The Four Layers](../foundations/federation-overview.md#the-four-layers)).
   On this note's reading, that commons admin is the role a steward credential would name.
5. Can a node agent act under a commons credential? An OpenVTC delegation credential "moves the
   permission question without answering it" (overview, "Layer 4"), and ToIP names
   "authenticated delegation" to an AI agent as an open standard still to be defined (VRC page).
   Whether an agent such as Octo could hold a delegation from a commons is not settled by any
   source read here.

## Disposition

**Implementation hypothesis.** BKC's `community_only` and `steward_authority` slots name sets of
people but resolve only inside one node. Community-issued membership and role credentials of the
kind the DTG work and Sideways specify, issued and revoked by a community quorum and held by the
member, are a candidate referent for both. Nothing in BKC changes. The smallest test is one
commons issuing membership and one steward role credential to a few members, and one node gating
`community_only` reads on a verified presentation.

## Provenance

- Kaliya Young and Drummond Reed (co-presenters, per the public video description), Trust over IP explainer at the Protocols of Place workshop (Kinship Earth, White
  Salmon, WA), September 2026, [video](https://youtu.be/AelpLS2pY18) published 2026-10-04.
  Timestamps refer to the video. Speaker turns come from an auto-transcript, and the speaker at
  [13:24] is identified as Drummond Reed by inference.
- [OpenVTC Ecosystem Overview](https://openvtc.github.io/wiki/overview), page as of 2026-10-08.
- [Verifiable Relationship Credentials](https://lf-toip.atlassian.net/wiki/spaces/HOME/pages/258113643),
  ToIP DTG WG, page dated 2025-09-24.
- Sideways, [Verifiable Community spec](https://github.com/SidewaysEarth/VerifiableCommunity)
  v1.2 (2025-07-01) and [Verifiable Community](https://sideways.earth/verifiable-community/).
- Project Weave, [technical depth](https://projectweave.tech/technical-depth.html).
- Kaliya Young, [Free Our Groups](https://identitywoman.net/free-our-groups-from-platforms-to-protocols/)
  (2026-07-07); Kaliya Young and David Hodgson,
  [Who Is Tending the Digital Substrate for Bioregional Movements?](https://identitywoman.net/who-is-tending-the-digital-substrate-for-bioregional-movements/)
  (2026-05-25).
- These sources are not independent. Kaliya co-presented the talk, is listed on the use-case team for
  Sideways spec v1.2, and is on the Project Weave team ("what we're doing at Project Weave"
  [19:54]). Weave's technical page treats the First Person Project as the anchor of its stack,
  and OpenVTC implements the First Person Protocol from that project's white paper. Their
  agreement is one network's design, not independent corroboration.
- Read 2026-10-11. BKC line numbers refer to the files at commit 9848ccf.
