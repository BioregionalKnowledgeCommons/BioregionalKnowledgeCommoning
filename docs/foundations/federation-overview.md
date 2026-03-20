# KOI Federation: A Guide to Federated Knowledge Commons

> **What this document covers:** How organizations with existing knowledge gardens can connect them into a federated network using the KOI protocol — without restructuring their data, surrendering sovereignty, or centralizing control.

---

## Table of Contents

1. [What is KOI?](#what-is-koi)
2. [Core Concepts](#core-concepts)
3. [KOI and the Hypertext Tradition](#koi-and-the-hypertext-tradition)
4. [How Federation Works](#how-federation-works)
5. [What You Need to Run KOI](#what-you-need-to-run-koi)
6. [Data Channels](#data-channels)
7. [Interfaces & Applications](#interfaces--applications)
8. [Authentication & Access Control](#authentication--access-control)
9. [MCP: Agent-Readable Knowledge](#mcp-agent-readable-knowledge)
10. [Personal Nodes](#personal-nodes)
11. [From Personal to Federated](#from-personal-to-federated)
12. [Current Network Status](#current-network-status)
13. [Getting Started](#getting-started)
14. [FAQ](#faq)
15. [Related Repositories](#related-repositories)

---

## What is KOI?

**KOI** (Knowledge Organization Infrastructure) is an open-source protocol for creating federated networks of knowledge. Think of it as HTTP for knowledge sharing — but instead of making demands (GET, POST, DELETE), KOI sends *signals* that each node can independently decide how to act on.

KOI was designed by [Block Science](https://block.science/) and is being actively developed for bioregional knowledge commoning, ecological data management, civic infrastructure, trans-local networks, and organizational knowledge sharing.

**Key properties:**
- **Open source** — Anyone can run a node. Anyone can build a sensor.
- **Sovereign** — Each node controls its own data and decides what to share.
- **Non-extractive** — Signals, not commands. No node can tell another what to do.
- **Format-agnostic** — Connects markdown files, Notion databases, wikis, websites, GitHub repos — whatever you already use.
- **No restructuring required** — Sensor nodes read your existing data in its current format.

---

## Core Concepts

> **Protocol vs. implementation:** The KOI protocol (designed by Block Science) defines the communication primitives — RIDs, FUN events, edges, signed envelopes, and the handler pipeline. Everything else in this section describes our implementation choices built on top of those primitives. The protocol is intentionally minimal and content-agnostic, which is what makes it adaptable to different use cases.

### Nodes

A **node** is any computer running the KOI protocol. At the protocol level, nodes are either **full** (runs an HTTP server, receives webhooks) or **partial** (lightweight client, polls peers). Each node has its own **identity** (ECDSA keypair for cryptographic signing).

In our implementation, a node also has:
- Its own **database** (PostgreSQL with pgvector for semantic search)
- Its own **vault** (a directory of markdown files, Obsidian-compatible)
- Its own **sensors** (connectors that read from data sources)

We use nodes in several roles — these are deployment patterns, not protocol-defined types:
- **Organizational nodes** — representing a project, community, network, or institution
- **Bioregional nodes** — representing a geographic/ecological region
- **Thematic nodes** — representing a community of practice or domain (e.g., civic governance, regenerative finance)
- **Personal nodes** — representing an individual's knowledge environment
- **Coordinator nodes** — aggregating across multiple leaf nodes

### Reference Identifiers (RIDs)

Every piece of knowledge gets a **Reference Identifier** — a unique, stable name. Like an ISBN for ideas. RIDs let you *refer to* something without *possessing* it. This is what makes federation possible: two nodes can talk about the same entity without either one owning the canonical copy.

Format: `orn:koi-net.node:{name}+{hash_suffix}`

### Entities

The KOI protocol is content-agnostic — it transports knowledge objects identified by RIDs without prescribing what those objects represent. Our implementation organizes knowledge into **typed entities** with structured metadata:

| Entity Type | Examples |
|-------------|----------|
| Person | Researchers, community members, experts |
| Organization | NGOs, companies, First Nations, universities |
| Project | Initiatives, programs, research efforts |
| Location | Cities, watersheds, territories |
| Concept | Technical terms, frameworks, methodologies |
| Practice | Community activities (e.g., "herring monitoring") |
| Pattern | Cross-network generalizations from practices |
| Claim | Impact assertions with evidence chains |
| Evidence | Data, observations, supporting materials |

These types are implementation choices — a different KOI deployment could define entirely different entity types suited to its domain. Each entity has a **vault note** (markdown with YAML frontmatter) and a **backend record** (PostgreSQL with embeddings for semantic search).

### Entity Resolution

When data flows between nodes, entities need to be matched. Our implementation uses **multi-tier entity resolution**:

1. **Exact match** — Normalized name lookup (instant)
2. **Alias match** — Checks registered alternate names
3. **Contextual match** — Uses relationship context (e.g., "Sean" → "Shawn Anderson" when mentioned alongside a known organization)
4. **Fuzzy match** — Jaro-Winkler string similarity with type-specific thresholds
5. **Semantic match** — OpenAI embeddings + pgvector cosine similarity
6. **New entity** — Create if no match found

Entity resolution is not part of the KOI protocol itself — the protocol handles identity at the RID level (each knowledge object has a globally unique identifier). Resolution is an application-layer concern: how you reconcile entities across heterogeneous sources. Different deployments could use simpler or more sophisticated matching strategies.

---

## KOI and the Hypertext Tradition

> **Note:** This section is our interpretive framing, drawing connections between KOI's protocol primitives and the broader hypertext tradition. Block Science has not formally positioned KOI relative to Xanadu.

KOI's architecture shares deep structural roots with Ted Nelson's Xanadu project (1960s onward) — the original vision for a global hypertext system built on persistent addresses, bidirectional links, and content referenced across documents without duplication. Understanding this lineage clarifies both what KOI does and what it deliberately leaves to other layers.

### What KOI shares with Xanadu

Nelson's Xanadu introduced several ideas that remain radical:

- **Persistent identifiers** — Every knowledge object has a stable, unique address that never expires
- **Reference graphs** — Knowledge exists as a web of relationships, not isolated documents
- **Bidirectional awareness** — If Document A references Document B, B knows about it
- **Content-addressed knowledge** — You can point to something without possessing or copying it

KOI implements all four of these properties. RIDs are persistent identifiers. The entity graph is a reference graph. Backlinks (`mentionedIn`) provide bidirectional awareness. And the entire architecture is built on the principle that knowledge objects stay in their original systems — KOI references them, it doesn't duplicate them.

### Where KOI stops (by design)

Nelson's full Xanadu stack can be understood as four layers:

| Layer | Function | Xanadu | KOI |
|-------|----------|--------|-----|
| **1** | Persistent identifiers | Tumbler addresses | RIDs |
| **2** | Reference graph | Link database | Entity graph + FUN events |
| **3** | Transclusion rendering | Inline content inclusion | — |
| **4** | Document views | Composed documents from fragments | — |

KOI implements Layers 1 and 2 but intentionally omits Layers 3 and 4. This is a design choice, not a gap. KOI optimizes for **coordination across heterogeneous knowledge stores** — Obsidian vaults, Notion databases, GitHub repos, Discourse forums, chat platforms — rather than document composition. Trying to render transcluded views across all these systems would require full content storage, fragment addressing, permission mirroring, and version permanence. That would turn KOI into a complete hypertext platform, which was never the goal.

The result: KOI works as a **distributed card catalogue for knowledge objects**. It knows what exists, who attested to it, and how things relate. The rendering layer is separate and pluggable — Obsidian, Quartz, web dashboards, chat interfaces, or AI agents can each present the knowledge in their own way.

### Three knowledge object classes

Our implementation organizes knowledge into three complementary classes that create a natural curation flow. The KOI protocol itself is agnostic about how knowledge is categorized — these classes are a design pattern we've found effective for maintaining a navigable commons:

1. **Source Artifacts** — Comprehensive snapshots of external content (meeting transcripts, web pages, research papers). These form the evidence infrastructure. They are machine-managed, searchable, but not browsed directly.

2. **Curated Knowledge Notes** — Human or agent-authored synthesis (project descriptions, practice write-ups, entity profiles). This is the garden layer — selective, high-signal, maintained by gardeners.

3. **Derived Claims and Edges** — Structured propositions extracted from sources ("Organization X restored 50 hectares in Region Y"). These form the graph layer — queryable, verifiable, and traceable back to their evidence.

### The membrane principle

> Source artifacts are comprehensive. The garden is selective. Transclusion is the membrane between them.

This separation is what keeps a knowledge commons navigable at scale. Without it, gardens accumulate "shadow" complexity — comprehensive source material that overwhelms the curated knowledge. The membrane works in both directions:

- **Inward:** Source artifacts are ingested wholesale, but only promoted claims and synthesized notes enter the garden
- **Outward:** Any statement in the garden can trace back through its evidence chain to the original source

Transclusion in this context is not mainly a publishing feature — it is a **curation and review primitive**. The act of transcluding a claim from source into garden is the act of a gardener saying "this is worth knowing."

### Provenance as the trust surface

The real product of KOI federation is not elegant pages — it's responses that are useful *and show where they came from*. Every claim in the system can trace a provenance chain:

```
Curated knowledge note
  → extracted relationship (claim/edge)
    → source artifact (transcript, document, dataset)
      → original URL / file / conversation
```

This is what makes federated knowledge different from a search engine or a wiki. When an agent answers "what watershed restoration practices exist across the network?", the answer includes not just the practices, but *who observed them, where the observation was recorded, and how it was curated*. The trust surface is the provenance chain itself.

---

## How Federation Works

### FUN Events (Forget, Update, New)

When something changes in a KOI node, it signals its peers using **FUN events**:

- **F** (Forget): "I've removed something I previously shared."
- **U** (Update): "Something I've shared has changed."
- **N** (New): "I've learned something new."

These are **signals, not commands**. Each receiving node decides independently what to do. A node might:
- Integrate the update into its own database
- Ignore it entirely
- Queue it for human review
- Trigger a notification

FUN events are sent as **signed cryptographic envelopes** (ECDSA P-256), so you always know who sent a signal and can verify it's authentic.

### Edges: Consent-Based Connections

Nodes connect via **edges** — explicit, mutual agreements about what data to share:

1. **Node A proposes an edge** to Node B: "I want to share Practice entities with you."
2. **Node B approves or denies** the edge.
3. If mutually approved, data sharing begins — **strictly scoped** to the agreed entity types.

Edges define:
- **Direction** — Who provides data, who consumes it
- **RID type filter** — Which types of knowledge objects to exchange (e.g., in our deployment, only Practices and Patterns)
- **Polling interval** — How often to check for updates (typically 60 seconds)

### Poll + Confirm Loop

Federation uses a **polling model**, not push notifications:

```
Every 60 seconds:
  Node B → POST /koi-net/events/poll → Node A
  Node A responds with: "Here are 3 new events since your last poll"
  Node B processes events according to its own rules
  Node B → POST /koi-net/events/confirm → Node A
  Node A marks those events as delivered
```

This design means:
- No always-on websocket connections needed
- Nodes can go offline and catch up later
- Each node controls its own polling cadence
- Network partitions heal automatically

### Network Topology

The KOI protocol is topology-agnostic — it supports anything from flat peer-to-peer to hub-and-spoke. Our current deployment uses a **holonic structure** — leaf nodes connect to coordinators, which can connect to meta-coordinators:

```
[Greater Victoria]   [Cowichan Valley]        ← leaf nodes
        ↘                 ↙
   [Salish Sea Coordinator]                   ← coordinator
        ↕                ↓
   [Front Range]   [Cascadia Coordinator]     ← peer / future meta-coordinator
```

But this is a design choice, not a protocol requirement. You could also run a flat peer-to-peer network, a hub-and-spoke model, or lateral federation between peer organizations — whatever fits your governance structure.

---

## What You Need to Run KOI

Whether you're starting a new network for your organization or connecting to an existing one, the requirements are the same.

### You Don't Need To:

- **Restructure your knowledge garden** — KOI reads your data as-is
- **Adopt a specific tool** — Works with markdown, Notion, wikis, websites, whatever
- **Give up sovereignty** — You control what you share and what you accept
- **Run complex infrastructure** — A basic VPS (2 vCPU, 4GB RAM) is sufficient

### You Do Need:

1. **A data source** — Your existing knowledge garden (public or private)
2. **A KOI node** — A server running the KOI processor (can be shared hosting)
3. **A sensor** — A connector that reads your data source and feeds it to KOI
4. **An edge agreement** — Mutual consent with at least one other node (if federating)

### Sensor Nodes

Block Science describes "sensor nodes" as nodes that take inputs from outside organizational boundaries. In our implementation, sensors are lightweight connectors that read data from a source and feed it into your KOI node. We have sensors for:

- **Markdown vaults** (Obsidian, plain files)
- **GitHub repositories** (code, docs, issues)
- **Websites** (any public URL)
- **Notion databases**
- **Discourse forums**
- **Email** (Gmail via OAuth)
- **Chat platforms** (Telegram, Signal, Slack)

Sensors are easy to build — you can point Claude Code at the KOI protocol spec and your data source, and it will generate a sensor for you. They're typically 100-300 lines of Python.

### Minimum Setup Time

| Path | Time | What You Get |
|------|------|--------------|
| **Quick start** (scripted) | ~30 min | Running node, ready to federate |
| **Manual setup** | ~2 hours | Full control over configuration |
| **Personal node** (laptop) | ~15 min | MCP-connected personal knowledge environment |

---

## Data Channels

Our implementation supports two complementary channels for data exchange, both built on the KOI protocol's event and state communication primitives:

### Channel 1: Schema-Based Data

Request and receive **structured data** that matches a specific schema.

Example: "Send me anything that fits the Meeting Notes schema — it needs a date, participants, and notes."

- Data flows as typed entities with YAML frontmatter
- Each edge defines which schemas/entity types are exchanged
- Receiving node validates incoming data against expected structure
- Great for: cross-organizational knowledge exchange, commons aggregation

### Channel 2: Shared Directories

**File-level sync** between nodes — like a shared folder that stays in sync.

Example: Node A has a `shared/` directory. Anything dropped in there propagates to connected nodes within 60 seconds.

- Updates propagate automatically after edge approval
- Changes are detected and signaled via FUN events
- Great for: collaborative documents, shared resources, bilateral partnerships

### Choosing a Channel

| | Schema-Based | Shared Directory |
|---|---|---|
| **Control** | Fine-grained (per entity type) | Coarse (whole directory) |
| **Structure** | Entities with metadata | Any files |
| **Use case** | Knowledge commons, aggregation | Bilateral collaboration |
| **Overhead** | Entity resolution + typing | Minimal |

---

## Interfaces & Applications

### 1. Periodic Digests

Automated summaries of network activity:
- "Give me all updates from the past 7 days"
- Daily, weekly, or monthly cadence
- Delivered via email, Telegram, or rendered in-app

### 2. Network Visualization

A dashboard showing the KOI network as a graph:
- All nodes, their connections, and edge types
- Entity counts per node
- Event flow and health status
- Educational and inspirational — shows the living network

### 3. Telegram Alerts

Real-time notifications for:
- Sensor health (offline/unhealthy sensors)
- New federation events
- Entity resolution conflicts
- System errors

### 4. Agent-Readable Search (MCP)

The most powerful interface — see the [MCP section](#mcp-agent-readable-knowledge) below.

---

## Authentication & Access Control

### Public Data

For public knowledge gardens, no authentication is needed. Anyone can:
- Set up a sensor that reads public data
- Query the MCP for public entities
- Build applications on top of public knowledge

The value add of connecting public data through KOI: it becomes **legible to AI agents**. A KOI sensor gives your data a searchable handle that any AI tool can use.

### Authenticated Access

For private or commons-level data, KOI supports:

- **Email verification** — Prove you have an @organization.org email
- **API keys** — Unique keys per user for tracking and audit
- **OAuth flows** — RFC 8628 Device Authorization Grant for CLI tools
- **Role-based access** — Different data visibility per authentication level

### Access Tiers

| Tier | Access Level | Example |
|------|-------------|---------|
| **Public** | Anyone | Published research, project descriptions |
| **Commons** | Authenticated members | Shared methodologies, cross-org data |
| **Private** | Organization only | Internal notes, draft proposals |
| **Secret** | Individual only | Personal reflections, credentials |

These tiers are configurable per node and per edge. You can share Practice entities publicly while keeping internal Meeting notes private.

---

## MCP: Agent-Readable Knowledge

**MCP** (Model Context Protocol) is the interface that makes KOI knowledge accessible to AI agents — Claude, GPT, or any MCP-compatible tool.

### What MCP Enables

When you connect your knowledge garden through KOI and expose it via MCP, any authorized agent can:

- **Search** your knowledge semantically ("find all practices related to salmon habitat restoration")
- **Resolve entities** ("who is involved in this project?")
- **Traverse relationships** ("what organizations work on carbon credits in Cascadia?")
- **Get digests** ("summarize network activity from the past week")
- **Share documents** ("send this practice note to the commons")

### MCP Tool Categories

| Category | Tools | Purpose |
|----------|-------|---------|
| **Knowledge Search** | `search`, `search_github_docs` | Semantic search over indexed content |
| **Entity Resolution** | `resolve_entity`, `get_entity_neighborhood` | Find and connect entities |
| **Vault Operations** | `vault_read_note`, `vault_write_note`, `vault_search_notes` | Read and manage knowledge |
| **Federation** | `share_document`, `shared_with_me`, `federation_status` | Cross-node knowledge sharing |
| **URL Curation** | `preview_url`, `process_url`, `ingest_url` | Web content → knowledge graph |
| **Claims** | `create_claim`, `verify_claim`, `anchor_claim` | Impact claims with evidence |
| **Tasks** | `task_dashboard`, `task_list`, `task_add` | Task management |

### How It Works in Practice

```
You: "What practices related to watershed restoration exist across the network?"

Agent (via MCP):
  1. search("watershed restoration practices") → semantic search
  2. resolve_entity("Bowker Creek Initiative") → finds related org
  3. get_entity_neighborhood(bowker_creek_uri) → connected practices, people, evidence
  4. Returns: 3 practices from Greater Victoria, 1 from Cowichan Valley, 2 from Front Range
```

This is the key value proposition: **your knowledge garden becomes queryable by agents**, not just by humans browsing files.

---

## Personal Nodes

In addition to organizational nodes, individuals can run **personal KOI nodes** on their own machines. A personal node:

- Connects your **Obsidian vault** (or any markdown knowledge base)
- Indexes your **email** for semantic search
- Tracks your **working sessions** for context continuity
- Runs **entity resolution** across all your personal data
- Can **share selectively** with organizational nodes or peers

### Personal → Organizational Flow

```
[Your Personal Node]
  ├── Obsidian vault (private)
  ├── Email index (private)
  ├── Session history (private)
  │
  ├── share_document(mode='context_pack', recipient='commons')
  │     ↓
  │   Document staged on commons node
  │   Commons admin approves/rejects
  │     ↓
  └── Document integrated into organizational knowledge graph
```

### Share Modes

When sharing from a personal node, you control the scope:

| Mode | What's Shared |
|------|--------------|
| **root_only** | Just the selected document |
| **root_plus_required** | Document + required embeds (images, transclusions) |
| **context_pack** | Document + required + optional references (configurable depth) |

### Workflow Integration

Personal nodes integrate with your existing tools through Claude Code skills:

1. **Meeting notes** → Transcript extraction → Entity linking → Task creation → Knowledge graph
2. **Process notes** → Entity extraction → Backend deduplication → Wikilink insertion → Backlink propagation
3. **Cross-document discovery** → Find related documents across your vault based on shared entity references

This means your personal knowledge management workflow naturally feeds the federated commons — you document a practice in your vault, your agent contributes it to the commons, similar practices surface across the network, and patterns emerge.

---

## From Personal to Federated

KOI scales from one person's laptop to a global federated network. The architecture has four layers, each building on the last — but **each layer is optional and independent**. You can run just a personal node forever. You can share peer-to-peer without a commons. You can join a commons without federating. The protocol doesn't force progression — it enables it.

### The Four Layers

**1. Personal** — Your vault + local KOI backend. Meeting notes, entity resolution, semantic search. This works standalone — no network needed. You get value from day one.

**2. Peer-to-peer** — Connect with a collaborator. Shared directories sync over WireGuard with end-to-end encryption (X25519 + ChaCha20-Poly1305). Edge agreements scope what's exchanged. Sync happens within ~60 seconds.

**3. Commons** — A shared organizational knowledge base. Personal nodes contribute knowledge (staged for review), and a commons admin approves or rejects. This is the governance membrane: not everything that's shared gets integrated.

**4. Federation** — Multiple commons nodes connect. This can be **holonic** (leaf → coordinator → meta-coordinator, as in bioregional networks) or **lateral** (peer organizations sharing across domains — a civic governance project, a regenerative finance network, and a land stewardship initiative all federating their knowledge). The topology follows the governance structure, not a fixed hierarchy.

### How the layers connect

```
[Personal vault]  [Personal vault]  [Personal vault]
      ↕  P2P sync (E2EE)  ↕              |
[Personal node]   [Personal node]   [Personal node]
      ↘  share_document   ↙               ↓
    [Commons node A]              [Commons node B]
    (e.g., bioregional)       (e.g., thematic network)
            ↕  FUN events  ↕
         [Federation layer]
```

### Two examples

**Bioregional:** A practitioner in Greater Victoria documents a salmon monitoring practice in their vault. Their agent extracts entities and links them. They share the practice note to the Salish Sea commons. A coordinator node surfaces it alongside similar practices from Cowichan Valley and the Front Range.

**Trans-local:** A civic governance organization maintains a knowledge garden about participatory design patterns. A regenerative finance network tracks impact methodologies across multiple countries. Both run their own KOI commons nodes. When they federate, a researcher can query: "what participatory governance patterns have been applied to ecological credit systems?" — and get a grounded answer with provenance, drawing from knowledge that spans organizational and geographic boundaries.

### KOI as civic utility

KOI is designed as a **generalizable civic utility**. It works for bioregional networks, thematic communities of practice, distributed teams, trans-local alliances, and global organizations. The protocol doesn't assume geographic co-location — it assumes that groups with sovereign knowledge stores want to selectively connect them.

The bioregional deployment is the reference implementation and the most mature use case. But the same infrastructure is being evaluated by organizations working in civic governance, distributed team coordination, and trans-local knowledge commoning. The question isn't "how does your bioregion use this?" — it's "what knowledge does your community steward, and who do you want to share it with?"

---

## Current Network Status

### Bioregional Nodes

| Node | Location | Role | Entities |
|------|----------|------|----------|
| **Octo** (Salish Sea) | Hetzner (EU) | Coordinator | ~500 |
| **Greater Victoria** | Hetzner (EU) | Leaf node | ~30 |
| **Front Range** | Co-located with Octo | Peer node | ~50 |
| **Cowichan Valley** | OVHcloud | Leaf node | ~1 |

### Personal Nodes

Team members run personal KOI nodes daily on their machines — integrated with Obsidian, Claude Code, and MCP. Used for meeting processing, entity resolution, task management, and semantic search across personal knowledge. Personal nodes serve as the daily driver for KOI development, stress-testing entity resolution and knowledge workflows in production.

### P2P Connections

Personal nodes are connected over end-to-end encrypted channels (WireGuard mesh, X25519 + ChaCha20-Poly1305) with shared directories syncing in real-time. This demonstrates the peer layer working independently of the bioregional federation — team members share working documents, meeting notes, and project context without routing through a commons node.

### Active Sensors

Sensors currently running across the network include connectors for:
- GitHub repositories (Regen Network repos)
- Discourse forums
- Websites
- Obsidian vaults
- Email (Gmail)
- Chat platforms (Telegram, Signal)

### Emerging Use Cases

The same infrastructure is being evaluated by organizations working in:
- **Civic governance** — Distributed governance networks exploring federated knowledge sharing across member organizations
- **Trans-local knowledge commoning** — Organizations that span geographies and want sovereign knowledge stores with selective federation
- **Distributed team coordination** — Teams that need shared context without centralizing in a single platform

### What's Working

- ✅ Node-to-node federation with signed event envelopes
- ✅ Multi-tier entity resolution with contextual disambiguation
- ✅ MCP interfaces for agent-readable knowledge
- ✅ Shared directories with automatic sync
- ✅ Schema-based data exchange
- ✅ Vault sync with end-to-end encryption
- ✅ Personal node → commons sharing workflow
- ✅ Personal node P2P sync over encrypted mesh
- ✅ Daily production use for meeting processing and entity linking
- ✅ Periodic digests and Telegram alerts

### What's In Progress

- 🔄 Scaling beyond the initial network (currently 4 bioregional nodes + active personal nodes)
- 🔄 Onboarding tooling for non-technical organizations
- 🔄 Commons intake governance workflows
- 🔄 Network visualization dashboard

---

## Getting Started

### Option A: Quick Start (30 minutes)

```bash
# One-command bootstrap on a fresh VPS
curl -sSL https://raw.githubusercontent.com/BioregionalKnowledgeCommons/Octo/main/scripts/bootstrap.sh | bash
```

The wizard handles:
1. Docker build and database setup (PostgreSQL + pgvector + Apache AGE)
2. All migrations (70+)
3. ECDSA keypair generation and node identity
4. Workspace files (IDENTITY.md, SOUL.md)
5. Seed entity for your node
6. Optional connection to an existing federation (or start your own)

### Option B: Personal Node (15 minutes)

For individuals who want to connect their personal knowledge environment:

1. Install the personal KOI MCP server
2. Point it at your Obsidian vault
3. Start the backend (`~/.config/personal-koi/start.sh`)
4. Configure Claude Code to use the MCP

### Option C: Manual Setup (2 hours)

For full control over configuration:

1. **Provision** a VPS (2 vCPU, 4GB RAM, 40GB disk)
2. **Clone** the Octo repository
3. **Configure** your node identity, database, and sensors
4. **Establish edges** with other nodes (mutual approval)
5. **Deploy** sensors for your data sources

### Federation Readiness Checklist

Before connecting to other nodes, verify:

- [ ] `KOI_BASE_URL` is peer-reachable and `/koi-net/*` endpoints are exposed
- [ ] Peer public keys are registered in `koi_net_nodes`
- [ ] Edge orientation is correct (source = data provider, target = consumer)
- [ ] Poll + confirm loop returns 200 and counters increase
- [ ] `/koi-net/health` shows expected node identity and protocol flags

---

## FAQ

### Do I need to restructure my knowledge garden?

**No.** Sensor nodes read your data in whatever format it's already in — markdown, Notion, wiki, website. You don't need to add metadata or change your file structure.

### Can anyone scrape my public data with a sensor?

**Yes** — if your data is public, anyone could build a sensor for it (just like anyone can scrape a website). KOI sensors on public data primarily add value by making it **agent-readable** and **semantically searchable**.

For private data, edges require mutual consent and authentication.

### What's the difference between KOI and just scraping?

The KOI protocol adds:
- **Signed envelopes** — You know who sent each signal and can verify authenticity
- **Consent-based edges** — Both parties explicitly agree to share
- **Sovereignty** — Signals, not commands. You decide what to do with incoming data.

Our implementation adds on top of the protocol:
- **Entity resolution** — Automatic deduplication and linking across sources
- **Semantic search** — Not just keyword matching, but meaning-aware queries

### How is this different from a centralized database?

Every node maintains its own database. There's no central server that holds everyone's data. Nodes exchange *signals* about changes, and each node decides what to integrate. You can disconnect at any time without losing your data.

### What does it cost to run a node?

A basic VPS costs ~$5-15/month. The software is open source. The main cost is the time to set up sensors and maintain the node.

### Can I use this without running my own node?

**Yes** — for public data, you can use any existing node's MCP to query the network. For contributing data, you'll need either your own node or access to a shared organizational node.

### How does KOI relate to transclusion and Xanadu?

KOI implements the lower layers of Ted Nelson's Xanadu architecture — persistent identifiers (RIDs) and a reference graph with bidirectional awareness — but deliberately stops before the transclusion rendering and document composition layers. This is because KOI is designed to coordinate knowledge across many different systems (vaults, wikis, forums, code repositories), not to compose documents from fragments. The rendering layer is pluggable: Obsidian, web apps, or AI agents can each present the knowledge graph in their own way. If you think of Xanadu as "reference system + document composition engine," KOI is "reference system + event propagation network." The foundational layers are in place for transclusion to be built on top — KOI just doesn't prescribe how.

### How does this relate to Regen Network?

KOI was originally developed to organize knowledge for Regen Network's ecological credit ecosystem. The protocol is now being generalized for any federated knowledge commons. The Regen Network deployment serves as a reference implementation and the largest current sensor network.

### What is Regen AI?

Regen AI is the team building and operating KOI infrastructure for the Regen Network ecosystem. The team uses KOI daily for meeting processing, entity resolution, client knowledge management, and ecological credit data organization. The Regen AI deployment serves as the primary reference implementation — stress-testing KOI's personal, P2P, and federation capabilities in production. If you want to see what daily use of KOI looks like, Regen AI is the working example.

### Is KOI only for bioregional networks?

**No.** KOI was developed in a bioregional context but is designed as a generalizable protocol for federated knowledge. It works for any group that needs sovereign knowledge management with selective sharing — distributed teams, thematic communities of practice (e.g., civic governance, regenerative finance), trans-local alliances, research networks, and organizations that span multiple geographies. The bioregional deployment is the reference implementation, not the only use case.

---

## Related Repositories

### Protocol & Research

- [BlockScience/koi](https://github.com/BlockScience/koi) — KOI protocol specification (Block Science)
- [koi-research](https://github.com/DarrenZal/koi-research) — Protocol research and analysis

### Node Infrastructure

- [Octo](https://github.com/BioregionalKnowledgeCommons/Octo) — Reference KOI node implementation (coordinator node for the Salish Sea bioregion)
- [koi-processor](https://github.com/gaiaaiagent/koi-processor) — KOI backend processor (entity resolution, federation, semantic search)
- [koi-sensors](https://github.com/gaiaaiagent/koi-sensors) — Sensor nodes for ingesting data from GitHub, Discourse, websites, Notion, chat platforms

### MCP Servers (Agent Integration)

- [regen-koi-mcp](https://github.com/gaiaaiagent/regen-koi-mcp) — Organizational KOI MCP server (makes a node's knowledge queryable by AI agents)
- [personal-koi-mcp](https://github.com/DarrenZal/personal-koi-mcp) — Personal KOI MCP server (connects individual knowledge environments to Claude Code)

### Applications

- [bioregional-commons-web](https://github.com/BioregionalKnowledgeCommons/bioregional-commons-web) — Network visualization dashboard and commons browser
- [flow-funding](https://github.com/BioregionalKnowledgeCommons/flow-funding) — Threshold-based flow funding for commons stewardship

### Documentation

- [BioregionalKnowledgeCommoning](https://github.com/BioregionalKnowledgeCommons/BioregionalKnowledgeCommoning) — Foundations docs, pattern language, operations runbooks

---

## Further Reading

- [How KOI Works](./how-koi-works.md) — Deeper technical explanation with analogies
- [KOI Protocol Alignment](./koi-protocol-alignment-master.md) — Full protocol specification
- [New Bioregion Quickstart](./new-bioregion-quickstart.md) — Step-by-step setup guide
- [Join the Network](./join-the-network.md) — Comprehensive reference for all setup paths
- [Federation Operations Runbook](../BioregionalKnowledgeCommoning/docs/foundations/koi-federation-operations-runbook.md) — Edge management and troubleshooting
- [Knowledge Commoning Meta-Protocol](../BioregionalKnowledgeCommoning/docs/foundations/knowledge-commoning-meta-protocol-v0.1.md) — Governance layer specification

---

*This document is part of the [Bioregional Knowledge Commons](https://github.com/BioregionalKnowledgeCommons) project. Contributions welcome.*
