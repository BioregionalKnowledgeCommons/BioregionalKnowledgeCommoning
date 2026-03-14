# Demo Script — Friday Mar 13, Noon MT (11am PDT)

**Audience:** Benjamin + Shawn
**Duration:** ~3 minutes live, then discussion
**Live URL:** `https://45.132.245.30.sslip.io/commons/commitments`

---

## Pre-Demo Checklist

- [ ] Verify Octo is up: `curl -s https://45.132.245.30.sslip.io/health | jq .status`
- [ ] Sign out of any existing passkey session (browser → clear site data or use incognito)
- [ ] Reset commitments to PROPOSED state:
  ```bash
  ssh root@45.132.245.30 "docker exec regen-koi-postgres psql -U postgres -d octo_koi -c \"UPDATE commitments SET state = 'PROPOSED', pool_id = NULL WHERE state != 'PROPOSED'\""
  ```
- [ ] Open `https://45.132.245.30.sslip.io/commons/commitments` — confirm all 3 show PROPOSED badges
- [ ] Have terminal ready with Claude Code + personal-koi-mcp (for Scene 4 if showing)
- [ ] Fallback recording queued locally (see Recording Notes below)

---

## Scene 1: The Problem (30s)

**Open:** `https://45.132.245.30.sslip.io/commons/commitments`

**On screen:** Three commitment cards, all PROPOSED state.

**Say:**

> "These are real commitments from organizations in the Salish Sea. A nursery offering 200 hours of native plant restoration. A land trust lending soil monitoring equipment. A myco collective pledging 40 hours of mycoremediation.
>
> They exist today in spreadsheets and handshakes. The question: which pools should accept them, and how do we build trust around that decision?"

---

## Scene 2: Route (45s)

**Click:** "Check Routes" button on the **Mycopunks** commitment (mycoremediation pilot — best visual with fungi tag, clear score separation).

**On screen:** Routing suggestions panel opens showing two pools with scores.

**Point to score breakdown:**
- Victoria Landscape Hub: **68** (recommended)
  - same_bioregion: +30
  - offer_need_overlap: +18
  - timeframe_overlap: +10
  - capacity_fit: +10
  - governance_compat: 0
- Cascadia Bioregion Stewardship: **32** (not recommended)
  - umbrella bioregion: +15 (parent match, not exact)
  - lower tag overlap, partial capacity

**Say:**

> "The routing scorer evaluates six factors — bioregion match, tag overlap, timeframe, capacity, and governance. It's deterministic and transparent. No black box.
>
> Victoria scores 68 because it's in the same bioregion with matching need tags. Cascadia is a parent bioregion — broader match, lower score. The scorer suggests; stewards decide."

---

## Scene 3: Pledge + Verify (45s)

**Step 1 — Sign in:**

**Click:** Sign in button (top right or inline prompt)

**Action:** One-tap passkey authentication (Touch ID / security key)

**Say:** "Passkey sign-in. No passwords, no username by default."

**Step 2 — Pledge:**

**Click:** "Pledge to This Pool" on the Victoria Landscape Hub suggestion.

**On screen:** Commitment card updates — now shows "Pledged to: Victoria Landscape Hub Restoration Pool"

**Say:**

> "Pledging is pool curation — the steward is saying 'this commitment belongs in our pool.' It's independent of verification. You can curate first, verify later."

**Step 3 — Verify:**

**Click:** "Verify" button on the same Mycopunks commitment.

**On screen:** State badge changes from PROPOSED to VERIFIED.

**Say:**

> "Verification is a trust signal — 'we believe this pledger can deliver.' It's independent of pledging. You can verify without pledging, pledge without verifying. Three operations, composable. Not a single approval gate."

---

## Scene 4: Agent Draft (30s — optional, show if time allows)

**Switch to:** Terminal with Claude Code

**Run:**

```
Use draft_commitment_from_text to draft: "The Watershed Collective offers 100 hours of riparian buffer planting along the Goldstream River watershed, valued at $5,000, May through August 2026. They need native seedling supply and GPS mapping support. Maximum 2 sites at once."
```

**On screen:** Structured commitment JSON with typed offers, wants, limits, routing tags.

**Then run:**

```
Now use suggest_pool_routes with that draft
```

**On screen:** Routing suggestions with score breakdowns.

**Say:**

> "The agent takes natural language and makes the ancient coordination pattern legible — typed offers, wants, limits. The scorer does the rest. Human decides."

**Known gap note:** The MCP draft tool outputs bioregion names, not URIs. With exact URIs the score would be higher (68 vs ~18). URI normalization is a post-hackathon improvement.

---

## Scene 5: The Stack (15s)

**Say:**

> "Under the hood: BKC knowledge graph with 1,005 entities across 4 federated nodes. On-chain anchors via Regen Ledger. Consent-aware visibility scoping. Celo is the settlement layer — the stewardship infrastructure is the product."

---

## Post-Demo: Discussion Points

1. **Role assignments:**
   - Benjamin: web UX polish, routing visualization (FlowCanvas adaptation), submission narrative, demo recording
   - Shawn: TBD — discuss interest areas
2. **Hackathon deadlines:**
   - Celo V2: Mar 18 (9 AM GMT)
   - Synthesis: Mar 22 (11:59 PM PST)
3. **What exists:** `brief.md` (submission brief), `demo-storyboard.md` (full architecture), `/commons/flow-funding` (TBFF viz)
4. **Repos:** `BioregionalKnowledgeCommons/bioregional-commons-web`, `BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning`

---

## Post-Demo: Reset for Next Run

```bash
ssh root@45.132.245.30 "docker exec regen-koi-postgres psql -U postgres -d octo_koi -c \"UPDATE commitments SET state = 'PROPOSED', pool_id = NULL WHERE state != 'PROPOSED'\""
```

Verify: refresh `/commons/commitments` — all 3 should show PROPOSED.

---

## Fallback Recording Notes

If network issues prevent live demo Friday:

- **Tool:** QuickTime Player → File → New Screen Recording (or OBS)
- **Resolution:** 1920x1080
- **Flow:** Open commitments page → Check Routes on Mycopunks → Sign in with passkey → Pledge to Victoria → Verify → show state change
- **Duration:** Keep under 90 seconds
- **Save as:** `~/Desktop/bkc-commitment-routing-demo-2026-03-13.mov`
- **Record before noon Friday** as insurance
