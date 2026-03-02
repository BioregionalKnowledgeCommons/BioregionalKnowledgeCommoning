# Mar 2-5 Execution Plan (BKC x Build Day Swarm)
*Created: 2026-03-02 (Monday)*

## Objective
Ship a coherent, live demo on **Thursday, March 5, 2026 at 2:00 PM MT** that proves:
1. Knowledge commons is live and federated (not slideware)
2. Agent coordination can write/query that knowledge layer
3. Capital-allocation narrative is grounded in auditable evidence

## What Changed in Telegram Context (Since Last Session)
- owocki proposed a recurring build cadence: **Friday 12:00-3:00 PM** as weekly Schelling point
- owocki emphasized a packaging request: make the roadmap/vision "grokkable" for X audience (strawmap/infographic style)
- owockibot spotlighted Todd/Nou outputs publicly (watershed + A2A demo)
- owocki floated a concrete movement-level scope: **Boulder summit in August-ish**, possible **$25k-50k** treasury allocation if governance aligns
- plurality/Google grant signal remains active; application deadline cited as **April 3, 2026**

## Current Ground Truth
- BKC Gate status remains the same from prior session:
  - Gate A: integration decision post to Telegram after AG response (deadline **Mar 3, noon MT**)
  - Gate B: summarizer ingest sample call + token handoff if confirmed (deadline **Mar 3, 6:00 PM MT**)
  - Gate C: 4-node health + pre-stage helper + dry run + steward passkey (deadline **Mar 4, 6:00 PM MT**)
- `nou-techne` repos are cloned locally under:
  - `/Users/darrenzal/projects/nou-techne/`

## Demo Shape (Mind-Blowing but Realistic)
Use a "show > tell" sequence with three proof layers:

1. **Reality Layer (Live infra)**
- BKC 4-node federation on globe
- commons governance membrane (staged -> approved -> ingested)

2. **Coordination Layer (Agent workflow)**
- Clawsmos/Workshop A2A narrative: visible phase-based coordination
- Summarizer -> BKC `/ingest` (if Gate B lands); otherwise replay with sample payload

3. **Impact Layer (Capital + ecological signals)**
- Colorado River data artifact from Nou repo as evidence input
- explain how evidence entities map to allocation decisions and public accountability

## Day-by-Day Plan

## Monday, March 2, 2026
- [ ] Post a short Telegram update with:
  - current BKC live status
  - explicit integration seam offer (`/ingest`, `/chat`)
  - proposal for roadmap visualization sprint before build day
- [ ] Prepare one-page "Bioregional Swarm Roadmap v0.3" artifact in strawmap-style visual language
- [ ] Validate external dependencies:
  - Co-op app links currently 404 -> avoid relying on those routes live
  - use stable demo endpoints and local mirrors

## Tuesday, March 3, 2026
### By 12:00 PM MT (Gate A)
- [ ] If AG responds: post integration decision in Telegram (yes/no + exact next technical step)
- [ ] If AG does not respond: post fallback decision to proceed with standalone BKC demo path + open integration slot

### By 6:00 PM MT (Gate B)
- [ ] If Summarizer confirmed:
  - run contract sample call from `Octo/docs/integration/summarizer-ingest-contract.md`
  - rotate/share ingest token out-of-band
  - capture success/failure logs for runbook
- [ ] If not confirmed:
  - freeze fallback: staged commons-intake demo + static sample payload

## Wednesday, March 4, 2026
### By 6:00 PM MT (Gate C)
- [ ] Execute full pre-flight from `mar5-build-day-runbook.md`
- [ ] Confirm steward passkey login on production `/commons`
- [ ] Run pre-stage helper so queue has at least one approval candidate
- [ ] Full dry run timing to 30-minute script with bailout points

## Thursday, March 5, 2026
- [ ] 30-minute segment execution
- [ ] Capture social artifacts during run:
  - 30-60 sec clip of governance membrane moment
  - screenshot of source-grounded chat response
  - single "what shipped today" post within 2 hours

## Required Artifacts Before Go-Time
- [ ] Telegram-ready roadmap summary (5-tweet or 5-message form)
- [ ] One infographic (strawmap-inspired, BKC-specific)
- [ ] Demo fallback checklist printed/pinned
- [ ] One canonical "integration contract link pack" message

## Suggested Telegram Message (Ready Draft)
Use this if posting today:

> Quick build-day sync from BKC: we have 4-node federation live (Salish Sea, Front Range, GV, CV), governance membrane live (staged -> steward approval -> ingest), and graph-grounded chat live.  
> If Clawsmos Summarizer is ready, we can wire `/ingest` immediately this week.  
> Also drafting a grokkable roadmap visual so the bioregional swarm arc is legible to wider audience before Thu Mar 5 (2pm MT).  
> Happy to pair with anyone who wants to connect action-plane outputs to evidence entities in the commons.

## Risks to Watch
- Co-op routes shared in thread currently return 404; avoid dependence during live demo
- `/ingest` writes directly (no staging); keep governance membrane demo on `/koi-net/share` path
- X audience framing is now a core expectation; no packaging = reduced perceived momentum

## Immediate Next Action
Post the Telegram update today (Mar 2) with a concrete integration ask and timeline, then run Gate A prep so tomorrow's noon checkpoint is a binary decision, not an open loop.
