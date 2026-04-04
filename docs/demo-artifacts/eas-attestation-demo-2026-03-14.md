# EAS Attestation Demo — 2026-03-14

Dual-chain proof: BKC commitment verification anchored on both Regen Ledger (Cosmos) and Celo (EVM) via Ethereum Attestation Service.

## Schema

| Field | Value |
|-------|-------|
| **Schema UID** | `0xdcf86a36ec6ec644e7727f9e1c7290b38f7f8503b051b893774cdd52573ee1e0` |
| **Schema** | `string commitmentRid, bytes32 contentHash, string proofPackUri, string regenTxHash, string bioregion, uint64 verifiedAt` |
| **Revocable** | Yes |
| **Registered by** | `0x6f844901459815A68Fa4e664f7C9fA632CA79FEa` |
| **View** | [celo.easscan.org/schema/view/0xdcf86a...](https://celo.easscan.org/schema/view/0xdcf86a36ec6ec644e7727f9e1c7290b38f7f8503b051b893774cdd52573ee1e0) |

## Attestation (canonical)

| Field | Value |
|-------|-------|
| **Attestation UID** | `0x4f761a97b5bd5c4070997912c15cbcc24fbdbf8d33dcb0c97d5138e55f704e14` |
| **Claim RID** | `orn:koi-net.claim:a42c60ce7e7f1848` |
| **Bioregion** | Greater Victoria |
| **proofPackUri** | `http://45.132.245.30:8351/claims/orn%3Akoi-net.claim%3Aa42c60ce7e7f1848/proof-pack` |
| **View** | [celo.easscan.org/attestation/view/0x4f761a...](https://celo.easscan.org/attestation/view/0x4f761a97b5bd5c4070997912c15cbcc24fbdbf8d33dcb0c97d5138e55f704e14) |

Supersedes earlier attestation `0x7eb29f...` which had a localhost proofPackUri (SSH tunnel artifact). Both share the same content hash — the canonical attestation above has the correct public URL.

## Cross-Chain Hash Verification

The same content hash appears in three places — proving the commitment data is identical across chains:

| Location | Hash |
|----------|------|
| **BKC proof pack** (`anchor.content_hash`) | `5d3788829ca78c092f144fa97208d31030f2c73f5ff5220eac4ec763a74b562d` |
| **Regen Ledger** (anchored via `MsgAnchor`) | `5d3788829ca78c092f144fa97208d31030f2c73f5ff5220eac4ec763a74b562d` |
| **Celo EAS** (`contentHash` bytes32) | `0x5d3788829ca78c092f144fa97208d31030f2c73f5ff5220eac4ec763a74b562d` |

All three match (BLAKE2b-256 of canonical claim JSON). Verified on-chain by decoding the EAS attestation data.

## Regen Ledger Anchor

| Field | Value |
|-------|-------|
| **TX hash** | `B1710CF16E33A155F72E082C45733C1F0A40E126C6573E4950194DC6C7301D45` |
| **Ledger IRI** | `regen:113eoH7AZHoRRw9mgQ7ZdqvG8U1uu5vfwaJSMYXUaEKdDbYJe8L8.json` |
| **Chain** | `regen-upgrade` (testnet) |
| **Timestamp** | 2026-03-12T02:12:01+00:00 |

## Proof Pack

The full proof pack JSON (claim, evidence, state history, attestations, anchor) is available via KOI API:

```
GET http://45.132.245.30:8351/claims/orn:koi-net.claim:a42c60ce7e7f1848/proof-pack
```

Note: The KOI API is accessible via the federation gateway on the server. For public access, a BFF claims proxy route is pending.

**Note:** The canonical attestation above uses the correct public URL. An earlier attestation (`0x7eb29f...`) had `localhost` in the proofPackUri due to SSH tunnel usage — it remains on-chain but is superseded. The script now supports `KOI_PUBLIC_URL` to separate fetch URL from on-chain URI.

## What This Proves

1. A bioregional commitment (TBFF settlement in Greater Victoria) was verified through BKC's multi-attestation process
2. The verification was anchored on Regen Ledger with content-addressable integrity (BLAKE2b-256 hash)
3. The same verification was attested on Celo via EAS, linking to the Regen anchor and full proof pack
4. Anyone on Celo can look up attestation `0x4f761a...` and verify the commitment independently
5. The content hash is identical across both chains — no divergence, no re-hashing

## Tooling

Script: `Octo/scripts/eas/attest.ts`

```bash
# Register schema (one-time)
npx tsx attest.ts --register-schema

# Create attestation for any ledger_anchored claim
npx tsx attest.ts orn:koi-net.claim:<rid>

# Check wallet balance
npx tsx attest.ts --check-balance
```

Requires: `.env` with `PRIVATE_KEY`, `EAS_SCHEMA_UID`. See `.env.example`.
