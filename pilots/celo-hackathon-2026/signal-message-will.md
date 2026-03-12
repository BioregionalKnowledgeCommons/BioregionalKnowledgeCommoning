# Signal Message to Will Ruddick

**Context:** Will is building CLC DAO (Credit Loop Commons) on Celo — "credit routing for the long tail of real world commitments." White paper in progress. He writes about this on Substack (grassrootseconomics.substack.com).

---

Hey @Will Ruddick

I've been reading your recent Substack pieces: "Touching the Knowledge Commons" and "From Abstraction to Aliveness" in particular land close to something I've been working on in the realm of Bioregional Knowledge Commoning.

We've built a federated knowledge graph (4 bioregional nodes, ~1,000 entities) with a commitment pooling layer that maps closely to what you're describing with CLC DAO:

- Commitments with typed offers, wants, and limits — richer than a bare CAV, carrying constraints and routing metadata
- CommitmentPools with steward governance and activation thresholds — analogous to your swap pools but with human curation gates
- Evidence linking + proof packs — the "shared memory of kept commitments" you wrote about, anchored on-chain
- Routing scorer — deterministic matching of commitments to pools based on bioregion, taxonomy overlap, capacity fit

A design choice we're particularly aligned on: Our system separates commitment issuance from pool curation from verification as three orthogonal operations. Anyone can make a promise — self-sovereign issuance, just as in your three-layer model. Pool stewards curate which commitments belong. Verification is an independent trust signal earned through witnessed follow-through. A commitment can be curated into a pool before it's verified, or verified without being in any pool. And forkability is the safety valve — if a pool's curation diverges from community values, the community takes their history and rebuilds.

We've mapped the concept alignment between BKC, GE vouchers, and CLC in detail — CREATE maps to voucher issuance, PLEDGE to pool seeding, VERIFY to trust attestation. The full mapping is here: https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning/blob/main/docs/ge-integration/compatibility-memo.md

We're thinking of entering both the Celo Synthesis and Agent V2 hackathons this week, building on this work. The angle: AI agents help communities express commitments in natural language, then route them into stewarded pools. BKC is the knowledge and governance layer; Celo is the settlement and provenance layer. Our routing scorer is BKC-native but designed to be CLC-compatible — we'd love to make sure the integration seams are right.

Two questions:
1. Is the CLC white paper at a stage where you'd share a draft? Understanding the multi-hop routing and netting mechanics would help us design toward real compatibility rather than just conceptual alignment.
2. Would you be open to seeing a demo after the hackathon? The routing scorer + proof pack pattern might be a useful reference implementation — concrete commitments from coherent agents, as you put it.

Our commitment pooling foundations: https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning/blob/main/docs/foundations/commitment-pooling-foundations.md

Open to jam on this with anyone interested.
