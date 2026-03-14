# Hackathon Hub — Celo V2 + Synthesis

Two hackathons, same codebase, tailored narratives. MVP feature-complete on live Octo.

## Deadlines

| Hackathon | Build window | Submissions close | Winners |
|-----------|-------------|-------------------|---------|
| Celo V2 "Build Agents for the Real World" | Mar 2–22 | **Mar 22, 9 AM GMT** | Mar 24, 3 PM GMT |
| [Synthesis](https://synthesis.md/) | Mar 13–22 | **Mar 22, 11:59 PM PST** | Mar 25 |

## Registration Status (updated 2026-03-14)

### Celo V2 — Registered

| Step | Status | Details |
|------|--------|---------|
| Karma project | ✅ Done | [Bioregional Commitment Routing](https://www.karmahq.xyz/project/bioregional-commitment-routing) |
| 8004scan agent | ✅ Done | [agentId 1855](https://www.8004scan.io/agents/celo/1855) on Celo mainnet |
| agent.json on GitHub | ✅ Done | [ERC-8004 metadata](https://raw.githubusercontent.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning/main/pilots/celo-hackathon-2026/agent.json) |
| Telegram group | 🔲 Optional | [Join](https://t.me/realworldagentshackathon) for support/updates |

### Synthesis — Registered

| Step | Status | Details |
|------|--------|---------|
| POST /register | ✅ Done | participantId `a3ae357b`, teamId `d80b5adb`, [registrationTxn on Base](https://basescan.org/tx/0xacadafc618ba1569c30908320ff2deedf23f0898d55e09b03e831d12a2b52e58) |

## Submission Checklists (for submission day, ~Mar 22)

### Celo V2 (via [Karma](https://www.karmahq.xyz/community/celo/programs/1059/apply))

1. [x] Register project on Karma — [Bioregional Commitment Routing](https://www.karmahq.xyz/project/bioregional-commitment-routing)
2. [x] Register agent on [8004scan](https://www.8004scan.io/) — [agentId 1855](https://www.8004scan.io/agents/celo/1855)
3. [ ] Register on [agentscan.info](https://agentscan.info/) — needed for tweet (distinct from 8004scan)
4. [ ] Verify agent with [Self AI](https://app.ai.self.xyz/) — required for judging (screenshot if unavailable in region)
5. [ ] Compose + post tweet: Karma link + agentscan agentId + 8004scan link + tag @Celo @CeloDevs @CeloPG
6. [ ] Submit via [Karma form](https://app.karmahq.xyz/celo/programs/1059/apply): email + Karma project + tweet URL
7. [ ] Optional: Register on [Molthunt](https://www.molthunt.com/) (supplementary)
8. [ ] Upload demo video to Karma project page

### Synthesis (via [Devfolio](https://synthesis.devfolio.co/))

- [x] Complete registration — participantId `a3ae357b`
- [ ] Check [synthesis-hackathon GitHub](https://github.com/sodofi/synthesis-hackathon) README for current submission format
- [ ] Submit project via Devfolio

## Live Demo URLs

- Commitments dashboard: https://45.132.245.30.sslip.io/commons/commitments
- Create commitment: https://45.132.245.30.sslip.io/commons/commit
- Flow funding viz: https://45.132.245.30.sslip.io/commons/flow-funding
- Salish Sea Knowledge Garden: https://45.132.245.30.sslip.io

## Repos

- **Web**: [BioregionalKnowledgeCommons/bioregional-commons-web](https://github.com/BioregionalKnowledgeCommons/bioregional-commons-web)
- **Governance + pilot docs**: [BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning](https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning)
- **KOI backend (canonical)**: `~/projects/regenai/koi-processor` (`regen-prod` branch)
- **Synthesis hackathon reference**: [sodofi/synthesis-hackathon](https://github.com/sodofi/synthesis-hackathon)

## Artifacts Index

| File | Description |
|------|-------------|
| [vision.md](vision.md) | North star — thesis, arc, CLC convergence thread |
| [brief.md](brief.md) | 1-page submission brief |
| [conversation-log.md](conversation-log.md) | Human-agent collaboration log (for Synthesis `conversationLog` field) |
| [demo-storyboard.md](demo-storyboard.md) | Full architecture + routing scorer spec + verification checklist |
| [demo-script-friday.md](demo-script-friday.md) | Presenter's click-by-click script for Friday demo |
| `demo-recording-2026-03-13.mov` | Fallback recording (gitignored, local only) |
| [telegram-coordination-post.md](telegram-coordination-post.md) | Async share for builders group |

## Tracks + Judging

### Celo V2

| Track | Prize | Criteria |
|-------|-------|----------|
| Best Agent | 3K / 2K / 1K | Reputation score + integration quality + manual review |
| Best Agent Infra | 2K | Technical innovation, DX, security, real-world applicability |
| Highest 8004scan rank | 500 | Combinable with other tracks |

### Synthesis

| Track | Prize | Notes |
|-------|-------|-------|
| Open track | 10K pool | Themes: agents that pay / trust / cooperate / keep secrets |
| Partner tracks | Smaller prizes | For partner tool usage |

Judged by AI agents + human judges.

## Team + Roles

| Person | Focus |
|--------|-------|
| Darren | Routing logic, API, MCP tools, Celo adapter, submissions |
| Benjamin | Web UX polish, routing viz, submission narrative, demo recording |
| Shawn | TBD (Friday session) |

## Key Resources

- [Karma submission portal](https://www.karmahq.xyz/community/celo?programId=1059)
- [Celo agent docs](https://docs.celo.org/build-on-celo/build-with-ai/overview)
- [ERC-8004](https://docs.celo.org/build-on-celo/build-with-ai/agent-skills) — agent wallet standard
- [x402 / Thirdweb](https://portal.thirdweb.com/x402) — payment protocol
- [agentscan](https://agentscan.info/) — on-chain agent scanner
- [Self AI](https://app.ai.self.xyz/) — identity verification
- [Synthesis GitHub](https://github.com/sodofi/synthesis-hackathon)
- [Synthesis chat](https://nsb.dev/synthesis-chat)
- [Celo V2 Telegram](https://t.me/realworldagentshackathon)
- [CLC DAO forum post](https://forum.celo.org/t/introducing-clc-dao-credit-routing-for-the-long-tail-of-real-world-commitments-on-celo/12910)
- [Commitment pooling foundations](../../docs/foundations/commitment-pooling-foundations.md)
- [GE compatibility memo](../../docs/ge-integration/compatibility-memo.md)
