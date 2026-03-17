# BKC ↔ Grassroots Economics ↔ CLC DAO Compatibility Memo

**Date:** 2026-03-17
**Purpose:** Map BKC commitment pooling concepts to GE/Sarafu production patterns and CLC DAO design, with code references.

---

## Concept Mapping

| BKC | GE / Sarafu | CLC DAO (design) | Notes |
|-----|-------------|-------------------|-------|
| **Commitment** (offers/wants/limits in metadata) | **CAV** (Community Asset Voucher) — ERC-20 token representing a community's productive capacity | **Redeemable voucher / invoice / credit** — concrete promises from coherent agents | BKC richer: typed offers/wants/limits, agent-assisted drafting, no token required |
| **CommitmentPool** + steward governance | **SwapPool** (`erc20-pool/solidity/SwapPool.sol`) — multi-token liquidity pool with price-index exchange | **Clearing pool** + value index — multi-hop routing with netting | BKC adds steward governance membrane; GE has on-chain pool admin/owner |
| **CommitmentAction** + Evidence | **CAV redemption/swap** — `withdraw()` event on SwapPool | **Settlement against inventory** — obligation discharge | BKC adds proof chain (Evidence entity → claims → anchor) |
| **TBFF threshold bands** | **TokenLimiter** (`erc20-limiter/solidity/Limiter.sol`) — per-holder, per-token caps | **Pool safety limits** — credit exposure caps | Similar mechanics: BKC threshold = value-based auto/semi/manual; GE limiter = per-address cap |
| **`governs_pool` predicate** | Pool admin/owner (contract `setFee`, `seal`) | **sCLC fee-access receipt** — time-bounded epoch access key for capped fee-access budget | Different layers: BKC = knowledge graph predicate; GE = contract owner; CLC = fee-gated access |
| **KOI-net federation** | **EVM events** (`Swap`, `Deposit`, `Collect`) + eth-indexer | **Multi-hop routing** — credit paths across pool network | Complementary: BKC federated knowledge; GE federated chain events; CLC routes across both |
| **Visibility scope / consent** | N/A (all on-chain, public) | N/A | BKC advantage: `node_private` commitments, 34 filtered query sites |
| **Routing scorer** | Manual matching (user selects swap pair) | **Value index + netting** — automated multi-hop clearing | BKC v0 is deterministic weighted scorer; CLC adds graph-based routing |

---

## GE Technical Details (from code)

### SwapPool Contract (`erc20-pool/solidity/SwapPool.sol`)

Core interface:
- `deposit(token, value)` — add liquidity
- `withdraw(outToken, inToken, value)` — execute swap (emits `Swap` event)
- `getQuote(outToken, inToken, value)` — price lookup via external quoter
- `setFee(uint256)` — fee in PPM (parts per million)
- `seal(uint256 state)` — irreversible state locking (fee, feeAddress, quoter)

**Mapping to BKC:** Pool creation = `POST /pools/create`. Deposit ≈ pledge (`POST /pools/{rid}/pledge`). Withdraw ≈ redemption (EVIDENCE_LINKED → REDEEMED state transition). Seal ≈ pool finalization (no BKC equivalent yet — pools stay mutable).

### Limiter Contract (`erc20-limiter/solidity/Limiter.sol`)

- `limitOf(token, holder) → uint256` — per-holder, per-token limit
- `setLimit(token, value)` — holder sets own limit
- `setLimitFor(token, holder, value)` — owner sets limit for contracts

Frontend calculates available capacity: `swapLimit = max(0, limitOf - poolBalance)` (`sarafu.network/src/components/pools/utils.ts:31-96`).

**Mapping to BKC:** `limitOf` → pool `remaining_capacity_usd` in metadata. Per-bioregion commitment caps achievable via pool metadata `capacity_usd`. The routing scorer uses `remaining_capacity_usd` to compute capacity fit score.

### Price Index / Quoter

- `priceIndex(tokenAddress) → uint256` (default `10000n` if no quoter set)
- Exchange: `fromAmount × (priceIndex_in / priceIndex_out)`
- `sarafu.network/src/components/pools/contract-functions.ts:52`

**Mapping to BKC:** No equivalent yet. BKC commitments carry `estimated_value_usd` in metadata — flat valuation, no relative pricing. CLC's value index would add dynamic pricing. Post-hackathon consideration.

### Demurrage (`erc20-demurrage-token`)

Time-decay on token balances (encourages circulation). Frontend adds 0.5% buffer to swap amounts to account for decay during transaction confirmation (`sarafu.network/src/components/pools/forms/swap-form.tsx:556-654`).

**Mapping to BKC:** `PoolCreateRequest.demurrage_rate_monthly` field exists (default 0, disabled). The foundations doc describes optional 2% monthly decay on unredeemed capacity. Conceptually aligned — both prevent hoarding.

### Celo Infrastructure

- **Network:** Celo mainnet (production), chain ID 42220
- **RPC:** `https://r4-celo.grassecon.org` (custom GE node) + public fallback
- **Tokens:** cUSD (`0x765DE816845861e75A25fCA122bb6898B8B1282a`), CELO native
- **BKC tokens deployed:**
  - **VCV (Victoria Commitment Voucher):** GiftableToken at [`0x4CDb98Ff88af070b1794752932DbAD9Edf7a1573`](https://celoscan.io/address/0x4CDb98Ff88af070b1794752932DbAD9Edf7a1573) — 6 decimals, agent wallet authorized as minter. 28,600 VCV minted across 23 commitments.
  - **TBFFSettler:** [`0x10De66A7f4e20d696Fb0d815c99068D4fA1f9030`](https://celoscan.io/address/0x10De66A7f4e20d696Fb0d815c99068D4fA1f9030) — 5 nodes, TBFFMath convergence, discrete ERC-20 transfers.
- **BKC agent wallet:** `0x6f844901...` — holds 95.7 CELO + 28,600 VCV
- **Wallet:** Valora + Web3Modal (Reown)
- **Indexing:** `eth-tracker` + `eth-indexer` → PostgreSQL FDW (Foreign Data Wrapper)

**Hackathon result (2026-03-17):** Deployed GiftableToken (VCV) and TBFFSettler on Celo mainnet (not testnet). End-to-end pipeline working: audio transcript → AI commitment extraction → commitment creation → VCV minting on Celo. SwapPool deployment is next (Day 8).

### Sarafu dApp Patterns

- **Pool creation UI** streams deployment status via async generator: contract deploy → confirmation → DB save → success (`sarafu.network/src/components/pools/forms/create-pool-form.tsx:81-102`)
- **Swap flow**: reset approval → approve amount → execute swap (3-step) (`swap-form.tsx`)
- **Pool listing**: aggregates from chain_data + pool_router FDW tables, sortable by swap count, name, voucher count
- **Federated DB**: PostgreSQL with FDW for chain data synthesis — similar to BKC's entity federation

---

## CLC (Cosmo-Local Credit)

**Status:** White paper published at [cosmolocal.credit](https://cosmolocal.credit) (v0.6, Ruddick & Sohail). Contracts deployed on Celo mainnet (v0.5.0): SwapPool (`0xCF879ADd...`), SwapRouter (`0x204653A8...`), GiftableToken (`0x1F74298f...`), Limiter (`0x392d269E...`). 188 active pools, 26K+ users on Sarafu Network.

### Key Concepts

| Concept | Description | BKC analog |
|---------|-------------|------------|
| **Multi-hop routing** | `SwapRouter.quoteExactInput(Hop[])` walks pool graph for multi-hop quotes | Routing scorer v0 is single-hop; C1 maps scorer output to `Hop[]` paths |
| **Value index** | `IQuoter` implementations (DecimalQuoter, RelativeQuoter, OracleQuoter) | `estimated_value_usd` is static; quoter integration is C1 |
| **Netting flows** | Bilateral/multilateral debt clearing via cycle enumeration | No equivalent — BKC settles via TBFF, not netting |
| **sCLC access receipt** | Time-bounded epoch access key for capped fee-access budget | `governs_pool` predicate + steward role |
| **SwapPool** | Multi-token vault with token registry, limiter, quoter, fee policy | CommitmentPool with threshold activation |
| **Credit routing for the long tail** | Making small community commitments routable across regions | Exactly the routing scorer's purpose |

### Integration Path

1. **Hackathon (done):** BKC-native routing scorer + on-chain deployment. VCV GiftableToken and TBFFSettler deployed on Celo mainnet. End-to-end: audio → commitment extraction → VCV minting. 28,600 VCV minted across 23 commitments. Dual-chain proofs (Regen Ledger + Celo EAS).
2. **C1 (post-hackathon):** Multi-hop path construction. Build token adjacency graph from on-chain pool listings (including BKC's SwapPool, deploying Day 8). Construct `Hop[]` paths from scorer-ranked pools → SwapRouter quoting. Read Sarafu pools (188 active, read-only). See [clc-integration-strategy.md](./clc-integration-strategy.md) for full phased plan.
3. **C2 (future):** Cross-network routing. Settlement write-back: CLC swap events → BKC Evidence → proof pack → Regen anchor. Multi-hop routing across BKC + Sarafu pools via SwapRouter.

### Will Ruddick's Narrative Arc

From the Substack essays:
- **"Footnotes on Intelligence"** — sensing → meaning-making → caring → committing → coordinating → learning (the demo loop we're building)
- **"From Abstraction to Aliveness"** — concrete promises from coherent agents, not abstract group currency (why BKC commitments carry typed offers/wants/limits)
- **"Touching the Knowledge Commons"** — shared memory of kept commitments (emotional center — proof packs as witnessed follow-through)
- **"Honor, Integrity, and the Cost of Keeping Our Word"** — trust from witnessed follow-through, not token mechanics (steward governance gates)
- **"The Protocol Beneath the Tools"** — AI and Celo are layers, not the foundation. Stewardship is. (BKC canonical, Celo settlement layer)

---

## Compatibility Assessment

### High Compatibility
- **Pool abstraction**: SwapPool and CommitmentPool serve same purpose (aggregate capacity, enable routing). Different implementations (EVM contract vs. knowledge graph entity with metadata).
- **Limiter / threshold**: Both enforce capacity constraints. BKC value-based bands; GE per-address caps.
- **Federated data**: Both use PostgreSQL federation. BKC via KOI-net events; GE via FDW + chain indexing.
- **Demurrage**: Both support time-decay. BKC optional per-pool; GE per-token contract.

### Medium Compatibility
- **Price/value**: GE has dynamic price indices via quoter contracts. BKC uses static `estimated_value_usd`. Gap closable via value index integration (C1).
- **Swap/redemption flow**: GE 3-step (approve → execute → confirm). BKC multi-state (PROPOSED → VERIFIED → ACTIVE → EVIDENCE_LINKED → REDEEMED). Different granularity, same arc.

### Low Compatibility (design differences, not conflicts)
- **Governance**: GE = contract owner + seal pattern. BKC = steward predicate + commons membrane. CLC = fee-gated access via sCLC receipt. Three different layers that could compose.
- **Identity**: GE = Ethereum address. BKC = entity URI in knowledge graph. CLC = sCLC holder address. Bridge needed for cross-system identity.
- **Privacy**: GE fully on-chain (public). BKC has visibility scope. CLC TBD. BKC's consent model is an advantage for sensitive community commitments.

### Design Differences (complementary, not conflicting)
- **Token issuance**: GE issues CAV vouchers. BKC now also issues GiftableTokens on Celo (VCV for commitment vouchers) — but tokenization is selective, not universal. Knowledge curation commitments stay off-chain; concrete redeemable offers get minted. BKC's routing scorer determines tokenization appropriateness.
- **On-chain settlement**: GE settles on Celo via SwapPool swaps. BKC settles via TBFF + proof packs anchored to both Regen Ledger and Celo EAS. TBFFSettler on Celo provides on-chain convergence math. The two settlement approaches are complementary — BKC adds provenance chain (Evidence → claims → attestations → proof packs) on top of on-chain execution.

---

## Three-Operation Governance Mapping

BKC decomposes commitment governance into three orthogonal operations. Each maps to GE/CLC patterns:

### CREATE → Voucher Issuance (Self-Sovereign)

| BKC | GE / Sarafu | CLC DAO |
|-----|-------------|---------|
| `POST /commitments/create` — anyone can create a commitment in PROPOSED state | CAV issuance — community creates ERC-20 voucher representing productive capacity | Credit issuance — coherent agent issues redeemable promise |

**Shared principle:** Promise issuance is self-sovereign. No gatekeeper reviews creation. In GE, a community mints its own voucher. In BKC, a pledger creates their own commitment. The right to promise is inherent, not granted.

### PLEDGE → Pool Seeding / Acceptance (Peer-Curated)

| BKC | GE / Sarafu | CLC DAO |
|-----|-------------|---------|
| `POST /pools/{rid}/pledge` — steward curates commitment into pool | `deposit(token, value)` on SwapPool — liquidity provider adds token to pool | Pool acceptance — clearing pool includes credit in routing graph |

**Shared principle:** Pool inclusion is peer-curated. In GE, a pool admin controls which tokens are deposited. In BKC, a steward controls which commitments are pledged. This maps to SPROUT License §3.5 peer-curation: inclusion is earned through relevance judgment, not central approval. Declining is implicit (not pledged / not deposited).

### VERIFY → Trust Attestation (Earned Through Follow-Through)

| BKC | GE / Sarafu | CLC DAO |
|-----|-------------|---------|
| `PATCH /commitments/{rid}/state` (PROPOSED → VERIFIED) — peer attests pledger can deliver | Voucher redemption history — trust built by repeated successful swaps | Redemption history + fee-access receipt (sCLC) — trust built through participation |

**Shared principle:** Trust emerges from witnessed follow-through, not pre-approval. In GE, a voucher's trustworthiness comes from redemption history, not from an approval step at issuance. In BKC, verification is an explicit attestation that the pledger can deliver — independent of pool curation.

### Orthogonality

The three operations are independent in BKC:
- A commitment can be **pledged** to a pool while still PROPOSED (curated but unverified)
- A commitment can be **verified** without being in any pool (trusted but uncurated)
- **Forkability** is the safety valve: if a pool's curation diverges from community values, stewards fork and re-curate. Commitments exist independently of pools, so they survive governance failures. This is the antidote to possessive stewardship.

In GE, this orthogonality is partially present (a voucher exists independently of any pool it's deposited in) but verification is implicit (redemption history rather than explicit attestation). CLC adds fee-gated routing access via sCLC receipts. BKC makes all three operations first-class with separate audit trails.

**Current runtime:** Single-pool MVP. Multi-pool pledging and cross-pool routing are post-hackathon (C1/C2).

---

## Recommended Actions

1. **Hackathon (done):** BKC routing scorer + on-chain deployment. VCV GiftableToken ([`0x4CDb98Ff...`](https://celoscan.io/address/0x4CDb98Ff88af070b1794752932DbAD9Edf7a1573)) and TBFFSettler ([`0x10De66A7...`](https://celoscan.io/address/0x10De66A7f4e20d696Fb0d815c99068D4fA1f9030)) deployed on Celo mainnet. End-to-end commitment extraction → minting pipeline on production. 28,600 VCV minted across 23 commitments.
2. **Day 8 (next):** Deploy BKC SwapPool (from GE `erc20-pool`) with VCV + cUSD, DecimalQuoter (1:1 rate). Read Sarafu pools (188 active, read-only). Display on `/commons/pools`.
3. **Signal to Will:** Share integration strategy doc. Offer BKC as upstream curation layer for CLC confederation (§5.2a). Now with on-chain deployment evidence.
4. **Post-hackathon C1:** Multi-hop path construction — `Hop[]` assembly across BKC + Sarafu pools via SwapRouter. Token graph construction from on-chain pool listings. See [clc-integration-strategy.md](./clc-integration-strategy.md).
5. **Post-hackathon C2:** Cross-network routing + settlement write-back via event bridge.
