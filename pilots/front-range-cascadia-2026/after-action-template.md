# MVIS After-Action: [Landscape Group] — [Date]

## Session Summary

- **Landscape group:**
- **Coordinator:**
- **Operator:**
- **Intents ingested:** (count)
- **Intents promoted to active:** (count)
- **Match proposals generated:** (count)
- **Proposals introduced:** (count)
- **Proposals accepted / declined / expired:**

## Intent Keys

Record all intent_keys for debugging and replay if engineering reopens.

| intent_key | type | asset_key | publisher | final status |
|------------|------|-----------|-----------|--------------|
| | | | | |

## Proposal RIDs

| proposal_rid | offer_key | want_key | outcome |
|--------------|-----------|----------|---------|
| | | | |

## Vocabulary

- **Asset keys used:** (list the exact keys from controlled vocabulary)
- **New vocabulary added mid-session:** (exception — capture why)
- **Vocabulary mismatches or confusion:** (cases where scribe/coordinator used different terms than the controlled list)

## Coordinator Experience

- **Digest clarity (1–5):**
- **Friction points:** (steps that were confusing or slow)
- **Suggested digest wording changes:**
- **Steps that needed engineering help:** (anything not coverable by the runbook alone)

## Federation

- **NUC cache check passed:** yes / no
- **Anomalies:**

## Manual Interventions

- **Any direct DB edits required:** yes / no (detail if yes)
- **Any manual data fixes:**
- **Any intent status corrections needed:**

## Go/No-Go Checklist

- [ ] Session completed without manual DB surgery
- [ ] Coordinator operated from runbook alone
- [ ] Result was clear proposals or clear no-match — not ambiguous silence
- [ ] No federation handler errors during the session
- [ ] Vocabulary additions were exception-only (< 2 new terms)

**Verdict:** `PROCEED` to second cohort / `PATCH` needed (describe below) / `RETHINK` needed (describe below)

### If PATCH needed

Describe the narrowest fix that unblocks the next cohort. Reference the specific `mvis-followup-*` issue if applicable.

### If RETHINK needed

Describe the workflow or architectural assumption that didn't hold.
