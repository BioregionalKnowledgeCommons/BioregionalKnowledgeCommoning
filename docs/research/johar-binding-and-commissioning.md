---
doc_id: bkc.connection.johar-binding-and-commissioning
doc_kind: research
status: draft
disposition: clarify existing term
depends_on:
  - bkc.commitment-economy-vision
  - bkc.commitment-economy-design
relates_to:
  - bkc.commitment-pooling
concepts:
  - intent-publication
  - demand-signal
  - fiat-only-need
  - payment-commitment
  - conditional-intent
external_sources:
  - rid: substack-corpus:indyjohar:the-investment-cycle-is-turning-inside
    title: "The investment cycle is turning inside out."
    url: https://indyjohar.substack.com/p/the-investment-cycle-is-turning-inside
    published: "2026-09-09"
  - rid: substack-corpus:indyjohar:the-system-as-a-dynamic-of-binding
    title: "The System as a Dynamic of Binding"
    url: https://indyjohar.substack.com/p/the-system-as-a-dynamic-of-binding
    published: "2026-08-19"
---

# Johar on commissioning: separating benefit estimates from payment commitments in BKC intents

## Why this note exists

This note reads two Indy Johar posts against BKC:
["The investment cycle is turning inside out."](https://indyjohar.substack.com/p/the-investment-cycle-is-turning-inside)
(2026-09-09) and
["The System as a Dynamic of Binding"](https://indyjohar.substack.com/p/the-system-as-a-dynamic-of-binding)
(2026-08-19). One point from the first bears on a design question BKC already has open. The
second adds one observation and no proposal.

## Avoided loss and payment commitment

Johar's worked example is a cooler city. Residents, health services, employers, schools and
public authorities have connected needs, and an intervention "may create substantial value across all of
them while offering an insufficient return to any one budget." He then states a limit: "An
avoided loss becomes a revenue source only where someone can make a credible payment
commitment." And: "Pooling budgets can change their scale, timing and purchasing capacity;
additional expenditure still has to be funded."

In BKC, the intent proposal's
[Demand Signal Aggregator (§4.4)](../ge-integration/intent-publication.md#44-demand-signal-aggregator)
aggregates unfulfilled intents into market-making signals, and "LPs see where liquidity is
needed and can direct capital to high-demand gaps" (line 124). An aggregated WANT records a
need. It does not record that anyone has committed to pay for it.

BKC already marks the kind of need where this matters. The commitment data model carries
`fiat_only`
([commitment-economy-design, "Needs: Present but Not Yet Compositional"](../foundations/commitment-economy-design.md#needs-present-but-not-yet-compositional),
line 99), and the vision asks whether stewards can see "which needs are fiat-only (requiring
real dollars) versus substitutable"
([commitment-economy-vision §4](../foundations/commitment-economy-vision.md#4-making-needs-compositional),
line 138). The same section says declared needs "become typed WANT intents" (line 148). But
`fiat_only` does not appear in
[intent-publication.md](../ge-integration/intent-publication.md) or the
[MVIS pilot spec](../../pilots/front-range-cascadia-2026/mvis-pilot-spec.md) (text search of
both files), and no field in the
[intent format sketch (§3)](../ge-integration/intent-publication.md#3-intent-format-sketch)
records a payment commitment. `token_in` ("asset offered", optional for WANT type) can state
what the issuer would give, but a WANT intent is not a binding commitment (§9 Q3 asks when it
becomes one), and no field names a payer other than the issuer.

The intent proposal already asks the question this bears on.
[§9 Q3](../ge-integration/intent-publication.md#9-open-questions) (line 256) reads: "When does a
WANT intent become a binding commitment? What are the state transitions?" In this note's reading,
Johar's sentence, which concerns when an avoided loss becomes revenue, suggests one criterion for
answering it where a need is fiat-only.

## Proposal

For whoever takes up §9 Q3. Nothing here is decided or changed.

1. **Keep two things apart in any WANT intent that carries a money figure:** an
   estimate of the benefit or avoided loss behind the need, and a payment commitment by a named
   party. Either can be absent. Only the second can show that Johar's condition is met, and only if the commitment is credible. Requiring a commitment already made is stricter than his "can make". Neither is the
   `monthly_amount_usd` that the commitment data model already records for needs (listed with
   `fiat_only` on line 99 of [commitment-economy-design](../foundations/commitment-economy-design.md#needs-present-but-not-yet-compositional)), which gives the size of the need. Whether
   this becomes a state in the Q3 transition or two fields in the §3 sketch is for the
   proposal's owners.
2. **Report fiat-only WANTs with no payment commitment as their own count** in the Demand
   Signal Aggregator, once `fiat_only` is carried into intents, so stewards and LPs do not read
   them as demand someone has agreed to pay for.
3. **Apply the same distinction to Conditional Intents.** The
   [§2.4 example](../ge-integration/intent-publication.md#24-conditional-intent) is on the
   provider side: "I would commit to providing B if at least 3 others in my landscape group also
   commit" (line 50). Line 52 adds a collective-action case, "a community water project that
   only makes sense at a minimum scale". Johar's coalition is on the payer side: it could
   "allocate contributions and establish authority to commission a response." A pledge to pay if
   others also pay is a conditional payment commitment. A statement of shared benefit is not.
   CONDITIONAL intents are
   [deferred in the MVIS pilot](../../pilots/front-range-cascadia-2026/mvis-pilot-spec.md#deferred-to-post-pilot)
   (line 30), so this is input for §9 Q6 on threshold-activation UX (line 259), not a pilot change.

**Limits.** Johar's example lists residents alongside budget-holding institutions (health
services, employers, schools, public authorities), though he notes that "People with the smallest budgets may have the
greatest exposure to failure." BKC's intents are issued by
users or pools (the §3 `issuer` field), and few of them may be able to pay. The main effect may
be to show how many fiat-only needs have no payer. That is untested, and this note does not
propose who pays. Johar also warns against making a payer a precondition: "A requirement to
identify the final buyer before exploration begins would reproduce the constraint we are trying to
overcome." None of the proposals above makes a payer a condition for publishing a WANT.

## The binding article: one observation

Johar writes: "Evidence must distinguish observed, inferred and hypothesised relationships." In
BKC's
[mapping intake contract](../foundations/bioregional-mapping-intake-contract-v0.1.md#relationship-shape),
the Relationship Shape example includes a numeric `confidence` (line 129). The contract has no
field table for relationships, its entity table marks `confidence` optional ("Extraction or
author confidence", line 115), and the relationships in Examples A and B carry none. No
structured field in the contract distinguishes observed, inferred and hypothesised relations.
This note proposes none.

## Disposition

**Clarify existing term.** The term is the WANT-to-binding-commitment transition in
[intent-publication.md §9 Q3](../ge-integration/intent-publication.md#9-open-questions).
In this note's reading, Johar's credible-payment sentence suggests a criterion for it, and the
existing `fiat_only` field marks where the criterion applies. The binding article changes nothing
in BKC. Here "binding commitment" is §9 Q3's sense, an obligation. Johar's "binding" means
consequential interdependence and is not adopted in BKC.

## Provenance

- Indy Johar, ["The investment cycle is turning inside out."](https://indyjohar.substack.com/p/the-investment-cycle-is-turning-inside), 2026-09-09.
- Indy Johar, ["The System as a Dynamic of Binding"](https://indyjohar.substack.com/p/the-system-as-a-dynamic-of-binding), 2026-08-19.
- Read 2026-09-24. Line numbers refer to the files as committed on that date.
