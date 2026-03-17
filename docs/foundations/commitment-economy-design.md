# Commitment Economy Design

## Two Faces of a Complete Local Economy

The bioregional commitment economy combines two complementary layers that together provide both productive exchange and needs-based sufficiency.

### Commitment Pooling — Supply & Exchange Layer

People issue vouchers backed by their productive capacity: labor, goods, services, knowledge, stewardship. Pools curate and value these individual vouchers, making them collectively liquid. Cycle clearing and netting across commitments reduces dependence on external currency.

This maps to Steiner's **Payment** ledger (exchange of current value) and **Loan** ledger (forward commitment of productive capacity).

### TBFF — Needs-Based Redistribution Layer

Each participant declares a needs threshold and a comfort level. Overflow above comfort routes to those below threshold. External funding (grants, stablecoins) enters through TBFF and flows to where it's needed most.

This maps to Steiner's **Gift** ledger (structural redistribution for the common good).

### Together: Sufficiency Guarantee

- The **pool** handles WHAT flows — goods, services, capacity
- **TBFF** handles WHO GETS HOW MUCH — needs-based redistribution
- **Cycle clearing** maximizes internal settlement, minimizing external dependency
- The flywheel: more diverse commitments → more internal netting → less external currency needed → more self-sustaining

## Fractal Structure

The same pattern repeats at every scale:

| Level | Commitments | TBFF Redistribution | Gap |
|-------|-------------|--------------------|----|
| **Individual** | Personal skills/time vouchers | Threshold within a project | What the person can't self-provision |
| **Project** | Pooled commitments from members | Project threshold within a bioregion | What the project can't internally settle |
| **Bioregion** | Federated capacity across projects | Bioregion threshold across the network | What the bioregion imports |
| **Network** | Cross-bioregion capacity exchange | Meta-level redistribution | What requires global coordination |

At each level, the threshold represents the gap that the circular economy can't close — the minimum external input needed for sufficiency. Import substitution (tracked via flow data) shrinks that gap over time.

## How the Pool Makes Vouchers Liquid

An individual voucher ("I'll give 10 hours of garden labor") has limited liquidity — who needs exactly that? The pool aggregates diverse commitments, enabling:

1. **Multi-hop exchange**: Garden labor → pool → carpentry service (without direct barter match)
2. **Valuation**: The pool's acceptance criteria and scoring signal what the community values
3. **Backstop**: Pool-level reserves (in stablecoin or other vouchers) cover redemption when timing mismatches occur
4. **Discovery**: Routing suggestions match new commitments to pools where they fill gaps

## On-Chain Architecture

### Commitment Voucher Token (GiftableToken)
Each pool issues a voucher token on Celo. When commitments reach VERIFIED state, the pool mints tokens proportional to assessed value. Follows the Grassroots Economics GiftableToken pattern: authorized minters, ERC-20 compatible, optional expiry (demurrage).

### TBFF Settlement (TBFFSettler)
A thin on-chain contract wraps TBFFMath (pure convergence library) with discrete ERC-20 transfers. Each settle() call reads balances, computes redistribution via iterative convergence, and executes transfers. No streaming required — keeps it simple for the hackathon, upgradeable to Superfluid later.

### Dual-Chain Attestation
Claims derived from settled commitments anchor on both Regen Ledger (ecological permanence) and Celo EAS (Ethereum-compatible attestation). Three-way content hash verification ensures integrity across chains.

## Relationship to GE/Sarafu/CLC Precedent

The Grassroots Economics Community Inclusion Currency (CIC) model pioneered voucher-based community economies in Kenya. BKC adapts this for bioregional knowledge commons:

- **GiftableToken**: Same contract, different context — commitment vouchers instead of currency vouchers
- **SwapPool**: Same infrastructure for inter-community liquidity, applied to inter-pool exchange
- **Sarafu Network**: 188 active pools provide read-only context for cross-network discovery
- **CLC**: Community Land Contribution pools as a proven model for resource aggregation

The key innovation is coupling this with TBFF redistribution and ecological claim anchoring — linking productive exchange to needs-based sufficiency to verified impact.

## Import Substitution Signal

Flow data through TBFF reveals which commitments are most effective at reducing external dependency:

1. Track what flows OUT of the bioregion (imports that require external currency)
2. Track which internal commitments REPLACE those imports
3. Signal to the community: "we need more of X" (where X substitutes for imports)
4. Pool scoring weights adjust to incentivize high-substitution commitments

This creates a feedback loop: flow data → community intelligence → commitment routing → reduced dependency → improved flow data.
