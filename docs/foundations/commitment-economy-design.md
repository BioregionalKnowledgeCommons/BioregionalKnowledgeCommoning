# Commitment Economy Design

**Companion doc:** [commitment-economy-vision.md](./commitment-economy-vision.md) — philosophy, pattern language, transition path, and situated-transfer metadata for the mechanisms described here.

## Two Faces of a Complete Local Economy

The bioregional commitment economy combines two complementary layers that together provide both productive exchange and needs-based sufficiency.

### Commitment Pooling — Supply & Exchange Layer

People issue vouchers backed by their productive capacity: labor, goods, services, knowledge, stewardship. Pools curate and value these individual vouchers, making them collectively liquid. Cycle clearing and netting across commitments reduces dependence on extractive external currency — while federation across bioregions increases healthy interdependence.

This maps to Steiner's **Payment** ledger (exchange of current value) and **Loan** ledger (forward commitment of productive capacity).

### TBFF — Needs-Based Redistribution Layer

Each participant declares a needs threshold and a comfort level. Overflow above comfort routes to those below threshold. External funding (grants, stablecoins) enters through TBFF and flows to where it's needed most.

This maps to Steiner's **Gift** ledger (structural redistribution for the common good).

### Together: Sufficiency Guarantee

- The **pool** handles WHAT flows — goods, services, capacity
- **TBFF** handles WHO GETS HOW MUCH — needs-based redistribution
- **Cycle clearing** maximizes internal settlement, reducing metabolic dependency on extractive systems
- The flywheel: more diverse commitments → more internal netting → less need for extractive external currency → more resilient — while cross-bioregion federation strengthens regenerative interdependence

## Fractal Structure

The same pattern repeats at every scale:

| Level | Commitments | TBFF Redistribution | Gap |
|-------|-------------|--------------------|----|
| **Individual** | Personal skills/time vouchers | Threshold within a project | What the person can't self-provision |
| **Project** | Pooled commitments from members | Project threshold within a bioregion | What the project can't internally settle |
| **Bioregion** | Federated capacity across projects | Bioregion threshold across the network | What the bioregion imports |
| **Network** | Cross-bioregion capacity exchange | Meta-level redistribution | What requires global coordination |

At each level, the threshold represents the gap that the circular economy can't close — the minimum external input needed for sufficiency. Reducing this gap means shifting from extractive dependencies (donor cycles, chokepoint suppliers) to regenerative interdependence (reciprocal, visible, chosen exchange across federated bioregions).

## How the Pool Makes Vouchers Liquid

An individual voucher ("I'll give 10 hours of garden labor") has limited liquidity — who needs exactly that? The pool aggregates diverse commitments, enabling:

1. **Multi-hop exchange**: Garden labor → pool → carpentry service (without direct barter match)
2. **Valuation**: The pool's acceptance criteria and scoring signal what the community values
3. **Backstop**: Pool-level reserves (in stablecoin or other vouchers) cover redemption when timing mismatches occur
4. **Discovery**: Routing suggestions match new commitments to pools where they fill gaps

## On-Chain Architecture

### Commitment Voucher Token (GiftableToken)
Each pool issues a voucher token on Celo. When commitments reach VERIFIED state, the pool mints tokens proportional to assessed value. Follows the Grassroots Economics GiftableToken pattern: authorized minters, ERC-20 compatible, optional expiry (demurrage). Note: demurrage is a seasonal tool, not a standing default — pool nourishment comes primarily from swap fees and steward-set limits. See [commitment-economy-vision.md §3](./commitment-economy-vision.md#3-demurrage-a-seasonal-tool-not-a-standing-engine).

### TBFF Settlement (TBFFSettler)
A thin on-chain contract wraps TBFFMath (pure convergence library) with discrete ERC-20 transfers. Each settle() call reads balances, computes redistribution via iterative convergence, and executes transfers. No streaming required — keeps it simple for the hackathon, upgradeable to Superfluid later.

### Dual-Chain Attestation
Claims derived from settled commitments anchor on both Regen Ledger (ecological permanence) and Celo EAS (Ethereum-compatible attestation). Three-way content hash verification ensures integrity across chains.

## Relationship to GE/Sarafu/CLC Precedent

The Grassroots Economics Community Inclusion Currency (CIC) model pioneered voucher-based community economies in Kenya. BKC adapts this for bioregional knowledge commons:

- **GiftableToken**: Same contract, different context — commitment vouchers instead of currency vouchers
- **SwapPool**: Same infrastructure for inter-community liquidity, applied to inter-pool exchange
- **Sarafu Network**: 188 active pools provide read-only context for cross-network discovery
- **CLC**: Cosmo-Local Credit — commitment pooling protocol for routing real-world obligations across federated pools

The key innovation is coupling this with TBFF redistribution and ecological claim anchoring — linking productive exchange to needs-based sufficiency to verified impact. See [commitment-economy-vision.md §9](./commitment-economy-vision.md#9-convergence-with-clc) for full CLC interface mapping.

## Dependency Quality Signal

Flow data through TBFF reveals which commitments are most effective at shifting from extractive dependency to regenerative interdependence:

1. Track what flows OUT of the bioregion through extractive channels (imports that require external currency, chokepoint suppliers, donor cycle dependency)
2. Track which internal commitments REPLACE those extractive dependencies
3. Track which cross-bioregion exchanges STRENGTHEN healthy interdependence (reciprocal, visible, chosen)
4. Signal to the community: "we need more of X" (where X reduces extractive dependency) and "this federation link is working" (where cross-bioregion routing creates mutual benefit)
5. Pool scoring weights adjust to incentivize high-substitution commitments

This creates a feedback loop: flow data → community intelligence → commitment routing → healthier dependency profile → improved flow data. Progress means less donor cycle dependency, less chokepoint vulnerability, less learning-loop outsourcing — but more federated exchange, more reciprocal capacity sharing, more collective learning.

CLC's netting yield formalizes the circularity dimension: `(gross routed value − net external liquidity injected) / gross routed value`. Higher = more circular settlement. This is a proxy for reduced metabolic dependency — not for reduced interdependence. See [commitment-economy-vision.md §9.9](./commitment-economy-vision.md) for the full dependency-quality framework.

## Needs: Present but Not Yet Compositional

The commitment data model includes `declaration_type` (offer or need), `fiat_only`, `need_category`, and `monthly_amount_usd` — enabling extraction of both offers and needs from mapping workshop conversations. However, these fields are not yet wired through the full system: pool governance doesn't track aggregate needs gaps, the routing scorer doesn't boost commitments that fill unmet needs, and the evidence loop doesn't yet learn from need fulfillment. Making needs compositional across pooling, routing, activation, and evidence is the next design step. See [commitment-economy-vision.md §4](./commitment-economy-vision.md#4-making-needs-compositional).

## Protection and Repair

Commitment pooling requires safety mechanisms — limits, insurance, disputes, forkability, consent boundaries, and bounded autonomy for capital decisions. These are detailed in [commitment-pooling-foundations.md §5](./commitment-pooling-foundations.md#5-governance-guidance) (consent and rights, dispute resolution) and [commitment-economy-vision.md §8](./commitment-economy-vision.md#8-protection-and-repair) (CLC loss waterfall, graduated response, forkability as safety valve).
