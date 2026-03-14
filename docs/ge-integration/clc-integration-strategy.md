# CLC Integration Strategy

**Date:** 2026-03-13
**Status:** Draft
**Depends on:** [compatibility-memo.md](./compatibility-memo.md), [commitment-pooling-foundations.md](../foundations/commitment-pooling-foundations.md)

---

## Strategic Position

Bioregional Knowledge Commons (BKC) provides **off-chain curation and routing intelligence**. Cosmo-Local Credit (CLC) provides **on-chain settlement and execution**. These are complementary layers, not competing implementations.

BKC's value is upstream: bioregion-aware context, consent-aware visibility, typed commitment metadata, federated knowledge graph, evidence-based provenance. CLC's value is downstream: token vaults, multi-hop swap execution, fee economics, liquidity coordination. The integration strategy is a bridge layer, not a merger.

---

## Decision Gate: Compatibility-First or Deployment-First?

Before Phase 1 begins, choose an approach:

**Compatibility-first** (recommended): Study CLC's token graph, quoter models, and registry patterns. Build the semantic-to-contract translation layer. Then selectively deploy where settlement warrants it.

**Deployment-first**: Deploy a test GiftableToken + SwapPool on Alfajores, learn by doing.

**Why compatibility-first:** BKC's value is upstream intelligence — knowing *which* commitments should route *where* and *why*. Deploying pools without understanding CLC's token graph topology produces isolated liquidity with no routing paths. The hard problem is the semantic-to-contract translation, not the contract deployment.

### Go/No-Go Criteria for Phase 2

All three must be met:

1. **Tokenizable commitment class identified** — at least one concrete, redeemable offer type (labor hours, goods, stewardship services) that can be meaningfully represented as a GiftableToken. Abstract knowledge curation is not tokenizable.

2. **Viable `Hop[]` path constructed** — at least one valid multi-hop route on an existing or Alfajores test pool graph that connects a BKC commitment token to a target token (e.g., cUSD). Proves the token graph is navigable.

3. **On-chain settlement adds value** — at least one clear reason settlement on Celo adds value over staying fully off-chain: cross-community redemption, LP liquidity access, verifiable receipt trail, or interop with existing Sarafu pools (26K+ users, 188 active pools).

---

## Phase 1 — Assetization + Path Construction (C1, post-hackathon, ~30 days)

### The Hard Problem

BKC's routing scorer outputs semantic pool suggestions: scores, bioregion fit, tag overlap, timeframe alignment, capacity fit. CLC's `SwapRouter` takes `Hop[]` of `(pool, tokenIn, tokenOut)` and only quotes along known token routes.

These operate at different abstraction levels. The scorer says "this commitment fits Victoria Landscape Hub (score: 68)." The SwapRouter says "give me a sequence of pool addresses and token pairs." Translation between these layers is the core engineering challenge.

### Translation Pipeline

#### 1. Voucher/Issuer Mapping

Which BKC commitments correspond to which GiftableTokens?

Not all will. Only commitments with concrete, redeemable offers qualify — labor hours, goods, stewardship services. Knowledge curation commitments, governance containers, and abstract pledges stay off-chain.

Mapping logic:
- `commitment.offer_type` + `commitment.unit` → candidate GiftableToken parameters (name, symbol, decimals)
- `commitment.issuer_uri` → GiftableToken owner address (requires identity bridge, see below)
- `commitment.estimated_value_usd` → initial quoter parameterization hint

GiftableToken issuance pattern (from `clc-protocol/src/GiftableToken.sol`):
- `mintTo(address to, uint256 amount)` — writer-authorized minting
- `writers` mapping — multiple authorized minters per token
- `expired` flag with `applyExpiry()` on transfer — maps to BKC commitment timeframe limits

#### 2. Pool/Token Graph Construction

Map BKC pools to existing or candidate SwapPools. Build a token adjacency graph from on-chain pool listings.

Data sources:
- **On-chain**: `eth-indexer` PostgreSQL tables for existing Sarafu pools on Celo mainnet
- **BKC**: `/pools/` API for BKC pool metadata (capacity, bioregion, routing tags)
- **Adjacency**: Pool P lists tokens [A, B, C] → edges A↔B, A↔C, B↔C through P

SwapPool interface (from `clc-protocol/src/SwapPool.sol`, deployed `0xCF879ADd8c34083b48c8a638D3C166eFcF35D454`):
- `tokenRegistry` — allowlist of accepted tokens (zero address = accept all)
- `tokenLimiter` — per-token credit caps via `ILimiter.limitOf(token, pool)`
- `quoter` — `IQuoter.valueFor(outToken, inToken, value)` for exchange rate

#### 3. Path Construction

BKC scorer → candidate pools → SwapPool token lookup → `Hop[]` assembly → SwapRouter quote.

```
BKC routing scorer
  → ranks pools by semantic fit (bioregion, tags, capacity)
  → for each candidate pool:
    → is it a SwapPool with relevant tokens listed?
    → if yes: construct Hop{pool, tokenIn, tokenOut}
    → chain Hops for multi-hop paths
  → feed Hop[] to SwapRouter.quoteExactInput()
  → return combined score: semantic_score + quote_feasibility
```

SwapRouter interface (from `clc-protocol/src/SwapRouter.sol`, deployed `0x204653A89FF5F2A935c88b0c750cAcdaA9e7368d`):
```solidity
struct Hop {
    address pool;
    address tokenIn;
    address tokenOut;
}

function quoteExactInput(Hop[] calldata path, uint256 amountIn)
    external returns (uint256 amountOut)
function quoteExactOutput(Hop[] calldata path, uint256 amountOut)
    external returns (uint256 amountIn)
```

The SwapRouter is stateless — it walks the Hop array, calling each pool's quoter. BKC's contribution is selecting *which* Hop sequences to quote, based on upstream knowledge the router doesn't have.

#### 4. Read-Only Celo Integration

Before any write operations, establish read access:
- Query SwapPool state via `viem` `publicClient` (`eth_call` to pool contracts)
- Read Sarafu Dune metrics ([dune.com/grassrootseconomics/sarafu-network](https://dune.com/grassrootseconomics/sarafu-network))
- Display CLC pool data alongside BKC pool data in commons-web
- No token issuance, no transactions — observation only

#### 5. Event Bridge

CLC on-chain events → BKC Evidence entities via `eth-tracker`.

Start with:
- `Swap` events (SwapPool) — record exchange activity as Evidence
- Expand to `Transfer` events (GiftableToken mint/burn) for issuance/redemption provenance
- Pool configuration events (listing changes, fee updates, `seal`) for governance audit trail

Identity bridge:
- BKC entity URI ↔ Ethereum address
- Established via signer attestation: entity signs a message proving address ownership
- Stored as entity metadata, queryable for cross-system resolution

---

## Phase 2 — Selective On-Chain Representation (C2, ~60 days)

**Not** "BKC pools deploy as CLC SwapPools." The abstractions aren't 1:1. Many BKC pools are governance containers or knowledge curation spaces with no settlement function. Forcing them on-chain loses their purpose.

Instead: **selected BKC commitments and pools can be represented on Celo as GiftableTokens + SwapPools where settlement adds value.**

### What Gets Tokenized

Communities with concrete, redeemable offers:
- Labor hours (restoration work, monitoring, mycoremediation)
- Goods (native plants, soil amendments, equipment loans)
- Stewardship services (watershed monitoring, habitat surveys)

A BKC pool that aggregates tokenizable commitments may deploy a corresponding SwapPool. But many BKC pools will remain off-chain:
- Knowledge curation pools (aggregating research, case studies)
- Governance containers (decision-making, charter development)
- Coordination pools (meeting coordination, planning)

### Agent-Assisted Tokenization

Natural language → structured commitment → agent determines tokenization appropriateness:
- Does the commitment have a concrete, redeemable offer? (not abstract)
- Is there a target community that would accept the token?
- Does on-chain settlement add value over off-chain tracking?
- If yes → generate GiftableToken deployment parameters
- If no → commitment stays in BKC knowledge graph only

### CLC Limiter Integration

Where relevant, BKC threshold bands inform Limiter configuration for on-chain pools:

| BKC Threshold-Based Flow Funding (TBFF) Band | Amount | On-Chain Limiter Config |
|---|---|---|
| Auto | < $500 | Limiter cap set permissively; auto-advance |
| Semi | $500 – $5K | Moderate cap; requires steward review |
| Manual | > $5K | Restrictive cap; requires multi-sig |

Limiter interface (from `clc-protocol/src/Limiter.sol`, deployed `0x392d269E5AB4d6024AccD3b2F7dE0b79E0f7602f`):
```solidity
function limitOf(address token, address holder) external view returns (uint256)
function setLimitFor(address token, address holder, uint256 value) external onlyWriter
```

BKC `capacity_usd` and `remaining_capacity_usd` metadata inform `setLimitFor()` values. Enforcement is on-chain — BKC provides the policy inputs, not the enforcement.

### Settlement Write-Back

CLC swap events → BKC Evidence → claim → proof pack → Regen anchor:
1. `eth-tracker` captures `Swap` event from tokenized pool
2. Bridge creates Evidence entity with settlement metadata (tx hash, amounts, participants)
3. Evidence links to existing BKC commitment via `proves_commitment` predicate
4. Claim created, attestations gathered, anchored on Regen Ledger
5. Proof pack archives the full provenance chain: commitment → token → swap → evidence → claim → anchor

### Two-Way Sync (Tokenized Pools Only)

For pools that exist both as BKC CommitmentPools and CLC SwapPools:
- BKC pool metadata (capacity, bioregion tags, steward governance) → informs token registry and limiter config
- CLC on-chain state (liquidity depth, swap volume, fee revenue) → displayed in BKC pool dashboard
- Sync is eventually consistent, not real-time — BKC is authoritative for metadata, CLC is authoritative for on-chain state

---

## Phase 3 — Upstream Intelligence Provider (C3, ~90 days)

BKC as the off-chain curation and routing intelligence layer for CLC-compatible networks.

### Agent-Mediated Routing Workflow

```
User: "I have 40 hours of mycoremediation to offer"

  → BKC agent: drafts structured commitment (offer_type, unit, bioregion, tags)
  → BKC scorer: identifies candidate pools (semantic scoring)
  → Path constructor: maps scored pools to CLC token graph
  → SwapRouter: quotes viable Hop[] paths
  → Agent: presents options with combined semantic + quote scores
  → User: selects route, executes
  → CLC: on-chain settlement
  → BKC: Evidence write-back, proof pack
```

BKC adds context CLC's token-pair routing doesn't have:
- **Bioregion proximity** — commitments route preferentially within their watershed/bioregion
- **Taxonomy overlap** — typed offers match pools by semantic tag similarity
- **Timeframe alignment** — seasonal work matches seasonally-appropriate pools
- **Capacity fit** — commitment size matches pool remaining capacity
- **Governance compatibility** — steward approval likelihood based on pool governance membrane

### Consent-Aware Layer

- `node_private` commitments route through BKC only — never surface on-chain
- Public commitments eligible for CLC settlement
- Consent boundary is the tokenization gate: only explicitly public, tokenization-approved commitments cross into CLC
- 34 filtered query sites in BKC enforce visibility scope; on-chain is inherently public

### CLC Confederation Compatibility (§5.2a)

The CLC white paper §5.2a describes confederation as "forks help everyone" — a mesh of overlapping curations where different communities maintain different pool networks that can interoperate.

BKC federation as a Commitment Pooling Protocol (CPP)-compatible network profile:
- KOI-net domain events carry commitment/pool state changes across federated nodes
- Each bioregional node maintains its own curation decisions (which commitments, which pools)
- Cross-bioregion routing uses federation edges, analogous to CLC's cross-pool routing
- BKC's governance membrane (edge approval, unknown handshake deferral) maps to CLC's confederation trust model

### sCLC (staked CLC) Participation

**Defer until Phase 3 evaluation.** sCLC is a time-bounded epoch access receipt — an access key for the capped fee-access budget, not a governance token or routing authority grant. BKC should only consider acquiring sCLC if:
- BKC communities need fee-gated swap access on CLC pools
- The access cost is justified by the routing benefits received
- BKC is actively participating in CLC pool liquidity (not just observing)

This is an access key, not a collaboration badge. Premature adoption adds cost without clear return.

---

## What to Use from Grassroots Economics (GE) / CLC (Don't Reimplement)

| Component | Source | Use |
|---|---|---|
| `SwapPool.sol` | `clc-protocol/src/SwapPool.sol` | Vault + swap engine (deployed `0xCF879ADd...` on Celo mainnet) |
| `SwapRouter.sol` | `clc-protocol/src/SwapRouter.sol` | Multi-hop quoter (deployed `0x204653A8...`) |
| `GiftableToken.sol` | `clc-protocol/src/GiftableToken.sol` | ERC-20 voucher issuance |
| `Limiter.sol` | `clc-protocol/src/Limiter.sol` | Per-token credit caps |
| `eth-tracker` + `eth-indexer` | `cosmo-local-credit/eth-tracker`, `cosmo-local-credit/eth-indexer` | Chain event indexing to PostgreSQL |
| `sarafu.network` | `grassroots-economics/sarafu.network` | Reference UI patterns (pool creation, swap flow) |

**Not adopted:** Full GE custodial/ramp/USSD stack (`eth-custodial`, `sarafu-vise`). That's a separate operational world for feature-phone access and fiat on-ramps — orthogonal to BKC's knowledge graph layer.

## What BKC Builds (Unique Upstream Value)

| Capability | Why CLC Doesn't Have It |
|---|---|
| Off-chain routing intelligence (bioregion, taxonomy, timeframe, capacity scoring) | CLC routes by token-pair adjacency; no semantic context |
| Consent-aware visibility (`node_private`, 34 filtered query sites) | On-chain is inherently public |
| Agent-assisted commitment drafting (natural language → structured → tokenization decision) | CLC assumes structured voucher input |
| Provenance chain (Evidence → claims → attestations → proof packs → Regen anchor) | CLC has tx receipts, not evidence chains |
| Federated knowledge graph (1,005+ entities across 4 KOI-net nodes) | CLC has token graph, not knowledge graph |
| Governance membrane with audit trail (edge approval, steward curation, verification) | CLC has contract owner + sCLC staking |

---

## CPP 4-Interface Mapping

BKC provides upstream inputs to CPP interfaces. It does not replace or duplicate the on-chain equivalents.

| CPP Interface | CLC On-Chain Implementation | BKC Upstream Input |
|---|---|---|
| **Curation** | Token registry — which vouchers a SwapPool accepts | Governance membrane decides which commitments are tokenization-worthy; routing scorer recommends pools. BKC curation is semantic (bioregion fit, tag overlap); CLC curation is contractual (token allowlist). |
| **Valuation** | `DecimalQuoter` / `RelativeQuoter` / `OracleQuoter` — exchange rate computation | `estimated_value_usd` and routing weights inform quoter parameterization, but BKC is not the quoter. On-chain price discovery is CLC's domain. |
| **Limitation** | `Limiter` — per-token, per-address caps enforced on deposit | TBFF threshold bands and `capacity_usd` inform Limiter configuration. Enforcement is on-chain — BKC provides policy inputs. |
| **Exchange** | `SwapPool` vault + `SwapRouter` multi-hop execution | No on-chain execution. BKC provides route suggestions (which pools, which paths); CLC executes swaps. |

---

## References

- [CLC White Paper](https://cosmolocal.credit) — CPP core primitive (Ch 1), routing as service (§5.2), confederation (§5.2a)
- [BKC ↔ GE ↔ CLC Compatibility Memo](./compatibility-memo.md)
- [Commitment Pooling Foundations](../foundations/commitment-pooling-foundations.md)
- [Sarafu Dune Dashboard](https://dune.com/grassrootseconomics/sarafu-network) — live network metrics
- CLC contracts: `clc-protocol/src/` — SwapPool, SwapRouter, GiftableToken, Limiter (all AGPL-3.0)
- GE indexing: `grassroots-economics/eth-tracker` + `eth-indexer`
