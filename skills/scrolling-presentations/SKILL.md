---
name: scrolling-presentations
description: Build concise, animated HTML presentations that people scroll through in a browser. Use for Jack Roberts style localhost presentations, visual explainers, tool comparisons, or connected workflow stories; not for exporting a video or PowerPoint deck.
---

# Scrolling presentations

Create a working browser presentation with brief editorial copy and animated diagrams that explain the topic. Deliver the files and a tested preview. A localhost URL is a local development server, not an animation product.

## Start with the actual brief

Use the user's topic, audience, reference, and existing design choices. If a reference is already selected, build from that direction without another design approval loop. Ask only for missing information that materially changes the result. For business audiences, choose one practical scenario and carry it through the presentation.

“Jack Roberts style” here means an original editorial scrolling page: numbered chapters, generous spacing, large display headings, and contained motion scenes. It is not a claim about Jack's exact software stack or an instruction to copy his assets.

## Make a small storyboard

- Give each chapter one explanatory job: a role, a difference, a process, or a decision.
- Lead with the use case. Use plain language before introducing product terminology.
- Keep the main view concise: a short heading, one sentence, and labels in the diagram. About 80–105 visible words including labels worked in the bundled example; this is a ceiling to question, not a target to fill.
- Move caveats, implementation notes, and sources into accessible disclosure sections. Source links must open their enclosing disclosure before navigating.
- Explain overlapping tools honestly. Distinguish a practical recommendation from an exclusive capability boundary. Do not imply every tool in an ecosystem is required.
- Verify current product claims against primary documentation. Mark illustrative records and interactions as examples. Do not turn a demonstration into a claim of live integration.

## Implement the page

Prefer plain HTML, CSS, and JavaScript for a portable presentation. No framework or animation package is required. Use the environment's available tools; do not assume Codex browser APIs, Firecrawl credentials, a specific operating system, or local usernames exist elsewhere.

The bundled [Microsoft example](assets/microsoft-example/index.html) is a working starting point with seven tools, a workflow walkthrough, a tool selector, and a sample supplier portal. Read [template-map.md](references/template-map.md) when adapting it. To copy it into a **new** output folder:

```sh
python scripts/create_presentation.py /path/to/new-presentation
```

Resolve the script relative to this skill's directory, not the project's current directory. The helper refuses an existing destination. The copied example still contains Microsoft content: replace its subject, sources, diagrams, and branding before calling it a presentation on another topic.

Use native document scroll, chapter anchors, a reading indicator, and responsive diagrams. Use CSS transforms and opacity for most movement, IntersectionObserver for entrance and offscreen pausing, and a small state machine for a walkthrough. Keep the number of steps and navigation count derived from content. Pause or stop walkthrough playback when it leaves view or the document is hidden. Respect reduced-motion preferences and provide a motion toggle.

## Avoid generic design

Use a clear editorial direction rather than a collection of interchangeable cards. Choose typography, spacing, and one restrained accent deliberately. Make diagrams do explanatory work: show a record changing, a handoff occurring, or one path becoming active. Remove repeated recap strips, decorative statistics, filler headings, and paragraphs that restate the diagram.

The companion `frontend-design` skill is the user's anti-slop skill. `web-animation-design` supplies additional motion patterns, and `reference-led-ui` supports visual matching. Use them when useful; this skill does not depend on them being installed. Preserve approved reference choices over generic style advice.

## Validate and deliver

Read [quality-bar.md](references/quality-bar.md). Inspect actual desktop and mobile screenshots. Test the meaningful controls, responsive bounds, image loading, source anchors, and playback state; syntax checks alone do not prove the page works. Reload after changes if there is no hot reload.

Open `index.html` directly, or serve the output directory with a local static server:

```sh
python -m http.server 4180 --bind 127.0.0.1 --directory /path/to/presentation
```

Use another free port if needed. Explain that the localhost link works only on the machine running that server. Include all local assets when packaging the result; omit caches, credentials, environments, research downloads, and machine-specific paths. Preserve third-party icon terms. Share a public hosted URL only after a deployment is actually authorized and completed.
