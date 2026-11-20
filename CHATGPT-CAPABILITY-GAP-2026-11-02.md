# ChatGPT skill/tool comparison — 2026-11-02

Repository inspected: [Prince-Vince/claude-skills](https://github.com/Prince-Vince/claude-skills), which contained 67 SKILL.md definitions at the time of comparison.

This document compares **portable skill workflows**, not the account access or runtime abilities of platforms. The currently installed ChatGPT skill catalog includes capabilities that this repository did not already define by the exact indicated names.

## Added as newly authored portable skills
- `skills/seo-audit/`: inspect page SEO and indexing eligibility; independently verify Google indexing via Search Console.
- `skills/ai-search-visibility/`: consistent non-branded public search benchmarking without false LLM recommendation claims.
- `skills/competitor-content-gap/`: research what competitors publish and identify genuine content gaps.
- `skills/linkedin-content-engine/`: turn expertise and article content into measurable LinkedIn publishing plans.

These are original portable workflow descriptions designed to complement the repository's existing Firecrawl skill. They do **not** incorporate proprietary plugin code, MCP implementations, paid products, account tokens or live connections.

## Other ChatGPT skill families visible here but not copied
- Firecrawl specialist skills for finding leads, enriching leads, business contact research, SEO, developer documentation, and current job postings. The repo already has a comprehensive Firecrawl CLI skill; some of those workflows can be authored separately if wanted.
- Google Drive / Docs / Sheets / Slides, Notion, Gmail and other app-connected workflows. Their ChatGPT connector integrations **cannot be installed by copying a Markdown skill**. Appropriate connector credentials and access controls must be configured independently.
- Document, spreadsheet, presentation and PDF production, plus stock templates: many rely on platform-specific artifact tooling or bundled templates and should not be copied blindly.
- Video tools and Remotion/HyperFrames: much of this capability already exists in this repository, so duplicate uploads were avoided.

## Security and provenance
- No imported skill files from installed ChatGPT plugins were replicated verbatim.
- No secret credentials, connected-user data, proprietary tool implementations, internal system prompts, binaries or bundled third-party assets are included.
- A skill can describe a process but cannot grant access to Google Search Console, LinkedIn APIs, or ChatGPT-connected accounts.
- Use existing `skills/firecrawl/` with a separately authenticated Firecrawl CLI for external research.

## Suggested next additions
If useful, implement additional original workflows for Search Console CSV analysis, prospective-customer research, and a local AI governance editorial review. Validate compatibility in Claude Code before enabling automated publishing or writes.
