# Claude Skills — Vince Davis

A portable backup of the [Claude Code](https://claude.com/claude-code) **agent skills** installed under `~/.claude/skills/`. Everything here is self-contained (real file content, no symlinks), so you can drop it into any other Claude account or machine.

- **38 skills**, ~0.65 MB, plain Markdown + a few helper scripts
- **34** were installed skills (originally junctioned into `~/.agents/skills/`)
- **4** are local/custom skills that live directly in `~/.claude/skills/`: `ipra-growthzone-beaver-builder`, `new-project`, `remotion`, and the self-authored `web-animation-design`
- No secrets, `node_modules`, or large binaries — safe to keep private

---

## How to restore on another Claude account / machine

Each skill is a folder containing a `SKILL.md` (plus any bundled `scripts/`, `references/`, etc.). To install, copy the folders into that machine's Claude skills directory.

**Windows (PowerShell):**
```powershell
git clone https://github.com/Prince-Vince/claude-skills.git
Copy-Item ".\claude-skills\skills\*" "$env:USERPROFILE\.claude\skills\" -Recurse -Force
```

**macOS / Linux:**
```bash
git clone https://github.com/Prince-Vince/claude-skills.git
mkdir -p ~/.claude/skills
cp -R claude-skills/skills/* ~/.claude/skills/
```

Restart Claude Code (or start a new session) and the skills will be discovered automatically. Skills that ship a script (`gsap`, `hyperframes`, `git-guardrails-claude-code`, `valyu-best-practices`) need their interpreter available — `bash`, `python3`, or `node` as noted below.

---

## Beyond the skills — full environment

The skills are only half the setup. To fully reproduce this Claude environment on another machine/account:

| Folder | What it covers |
|---|---|
| [`mcp/`](mcp/) | MCP servers — the claude.ai connectors (Google Drive, Higgsfield, Supabase, M365) re-add checklist + local Playwright MCP registration |
| [`clis/`](clis/) | Every CLI the skills depend on, plus [`clis/setup.ps1`](clis/setup.ps1) to install them all on a fresh Windows box |
| [`.env.example`](.env.example) | The API-key variable **names** the skills expect (Firecrawl, Valyu, …) — copy to a git-ignored `.env` and fill in |

---

## Added skills (2026-09-14)

- **skill-inspector** — NVIDIA SkillSpector-backed security review of agent skills.
- **archify** — interactive architecture, workflow, sequence, data-flow, and lifecycle diagrams.

Both folders include their bundled resources and licenses. See [source revisions and restore instructions](SKILL-SOURCES.md). The original inventory below describes the earlier 38-skill snapshot; the backup currently contains 41 skill folders.
## Inventory

Source key: **installed** = came from the agent-skills library · **local** = lives directly in `~/.claude/skills/` (custom / self-authored).

### 🔎 Web scraping, search & research (9)

| Skill | What it does | Source | Notes |
|---|---|---|---|
| `firecrawl` | Web scraping, search, crawling, and page interaction via the Firecrawl CLI — real-time web search with full page-content extraction beyond native tools. | installed | |
| `firecrawl-search` | Web search that returns real results **with** full-page markdown, not just snippets. | installed | |
| `firecrawl-scrape` | Extract clean markdown from any URL, including JS-rendered SPAs. Preferred over WebFetch for page content. | installed | |
| `firecrawl-map` | Discover and list all URLs on a site, with optional search filtering — find the exact page on a large domain. | installed | |
| `firecrawl-crawl` | Bulk-extract content from an entire site or section, with depth limits and path filtering. | installed | |
| `firecrawl-download` | Download a whole site as local files (markdown / screenshots) for offline reference. | installed | |
| `firecrawl-agent` | AI-powered autonomous extraction that navigates complex sites and returns structured JSON to a schema. | installed | |
| `firecrawl-browser` | **Deprecated** — page interaction (click, fill forms, log in, paginate). Use scrape + interact instead. | installed | |
| `valyu-best-practices` | Complete Valyu API toolkit: real-time search across web / academic / medical / financial sources, extraction, cited answers, deep research reports. | installed | ships `scripts/` (node) |

### 🎬 Video, motion & frontend design (8)

| Skill | What it does | Source | Notes |
|---|---|---|---|
| `hyperframes` | Author HTML-based video compositions — animations, title cards, captions, voiceovers, audio-reactive visuals, scene transitions. | installed | ships `scripts/` (node) |
| `hyperframes-cli` | The HyperFrames CLI: init, lint, preview, render, transcribe, tts, doctor, and more. | installed | |
| `hyperframes-registry` | Install and wire registry blocks/components into HyperFrames compositions. | installed | |
| `gsap` | GSAP animation reference for HyperFrames — tweens, easing, stagger, timelines, performance patterns. | installed | ships `scripts/` (python) |
| `remotion` | Build React-based programmatic video with Remotion (`<Composition>`, `useCurrentFrame`, `interpolate`, transitions, MP4 rendering). | local | |
| `website-to-hyperframes` | Capture a website and turn it into a HyperFrames video (promos, social ads, product tours). | installed | |
| `web-animation-design` | Research + implement modern scroll animations and micro-interactions; references Dribbble / Jitter / Mobbin. | local | **self-authored**; ships example HTML |
| `frontend-design` | Create distinctive, production-grade frontend interfaces that avoid generic AI aesthetics. | installed | |

### 📋 Product & project planning (7)

| Skill | What it does | Source | Notes |
|---|---|---|---|
| `write-a-prd` | Create a PRD via user interview + codebase exploration, then submit it as a GitHub issue. | installed | |
| `prd-to-plan` | Turn a PRD into a multi-phase implementation plan (tracer-bullet slices), saved to `./plans/`. | installed | |
| `prd-to-issues` | Break a PRD into independently-grabbable GitHub issues as vertical slices. | installed | |
| `new-project` | Scaffold a new project — AI-filled spec, plan, tasks, and CLAUDE.md from a one-line description. | local | |
| `design-an-interface` | Generate multiple radically different interface designs for a module using parallel sub-agents ("design it twice"). | installed | |
| `grill-me` | Interview you relentlessly about a plan/design until every branch of the decision tree is resolved. | installed | |
| `ubiquitous-language` | Extract a DDD-style glossary from the conversation, flag ambiguities, propose canonical terms → `UBIQUITOUS_LANGUAGE.md`. | installed | |

### 🛠️ Dev workflow & code quality (9)

| Skill | What it does | Source | Notes |
|---|---|---|---|
| `tdd` | Test-driven development with a red-green-refactor loop and integration tests. | installed | |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type-checking, and tests. | installed | |
| `git-guardrails-claude-code` | Add Claude Code hooks that block dangerous git commands (`push`, `reset --hard`, `clean`, `branch -D`) before they run. | installed | ships `scripts/` (bash) |
| `improve-codebase-architecture` | Find architectural improvements — deepen shallow modules to make the codebase more testable and AI-navigable. | installed | |
| `migrate-to-shoehorn` | Migrate test files from `as` type assertions to `@total-typescript/shoehorn`. | installed | |
| `request-refactor-plan` | Create a detailed refactor plan with tiny commits via interview, then file it as a GitHub issue. | installed | |
| `triage-issue` | Triage a bug — explore the codebase for root cause, then open a GitHub issue with a TDD fix plan. | installed | |
| `qa` | Conversational QA session: you report bugs, the agent explores for context and files GitHub issues. | installed | |
| `scaffold-exercises` | Create exercise directory structures (sections, problems, solutions, explainers) that pass linting. | installed | |

### ✍️ Writing & knowledge (2)

| Skill | What it does | Source | Notes |
|---|---|---|---|
| `edit-article` | Edit and improve article drafts — restructure sections, improve clarity, tighten prose. | installed | |
| `obsidian-vault` | Search, create, and manage Obsidian notes with wikilinks and index notes. | installed | |

### 🧩 Meta / skill management (2)

| Skill | What it does | Source | Notes |
|---|---|---|---|
| `find-skills` | Help discover and install agent skills when you ask "how do I do X" or "is there a skill for…". | installed | |
| `write-a-skill` | Create new agent skills with proper structure, progressive disclosure, and bundled resources. | installed | |

### 🏛️ IPRA-specific (1)

| Skill | What it does | Source | Notes |
|---|---|---|---|
| `ipra-growthzone-beaver-builder` | Field guide for rebuilding IPRA pages in GrowthZone's Beaver Builder (+ PowerPack) — quirks, sanitizer landmines, proven CSS/layout patterns. | local | **custom** |

---

*Generated as a backup snapshot. To refresh after installing/updating skills, re-copy `~/.claude/skills/` (dereferencing junctions) and update this inventory.*
