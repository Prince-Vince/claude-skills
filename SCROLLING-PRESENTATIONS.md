# Make a Jack Roberts style scrolling presentation

Everything needed for the browser presentation workflow is in this repository. The primary skill is **scrolling-presentations**. You can use it in Claude Code, Codex, or another agent that supports `SKILL.md` folders.

## Start here

| Skill | Purpose | Required? |
|---|---|---|
| [scrolling-presentations](skills/scrolling-presentations/SKILL.md) | The complete workflow and working HTML example | Yes |
| [frontend-design](skills/frontend-design/SKILL.md) | The anti-slop design guidance used in this presentation | Useful companion |
| [web-animation-design](skills/web-animation-design/SKILL.md) | Scroll and motion patterns | Useful companion |
| [reference-led-ui](skills/reference-led-ui/SKILL.md) | Work from a visual reference and inspect the result | Useful companion |
| [rtf](skills/rtf/SKILL.md) | Transcript timing and graphic placement in an existing video | Optional |

You do not need Remotion, HyperFrames, GSAP, Firecrawl, Microsoft accounts, or API keys to view or adapt the bundled static presentation. Research and browser-testing capabilities are useful while creating a new one. Exporting a finished video is a separate workflow.

## Install on another machine

Clone or download this repository. Copy the four presentation skill folders into your agent's installed-skills directory. The helper below copies them and refuses to overwrite an existing skill.

Windows PowerShell — Codex:

```powershell
git clone https://github.com/Prince-Vince/claude-skills.git
python .\claude-skills\scripts\install-presentation-skills.py --destination "$env:USERPROFILE\.agents\skills"
```

Windows PowerShell — Claude Code: use `--destination "$env:USERPROFILE\.claude\skills"` instead.

macOS / Linux — Codex:

```sh
git clone https://github.com/Prince-Vince/claude-skills.git
python3 claude-skills/scripts/install-presentation-skills.py --destination "$HOME/.agents/skills"
```

For Claude Code use `--destination "$HOME/.claude/skills"`. For another skill-compatible agent, supply its documented skill directory. If you already have some of these skills installed, review them and manually copy only the missing folders instead of overwriting them. Start a fresh agent session after copying.

To include the optional RTF helper, add `--include-rtf` on a fresh install. It has separate Python dependencies; see its [setup guide](skills/rtf/PORTABILITY.md). Those dependencies are not installed automatically.

## The prompt to use

> Use the scrolling-presentations skill to build a Jack Roberts style scrolling presentation about [topic] for [audience]. Keep the text minimal. Apply frontend-design for the anti-slop pass. Use one practical example, animated diagrams, a clear comparison, and expandable notes. Verify current factual claims, then test desktop and mobile layouts. Deliver a portable folder and a local preview.

In Codex you can explicitly name `$scrolling-presentations`. In Claude Code use the skill by name or the agent's skill invocation interface. You do not need to remember the companion skills for routine use; the primary skill explains when they help.

## Open the working example

Open [index.html](skills/scrolling-presentations/assets/microsoft-example/index.html) from a downloaded copy of this repository. GitHub's file viewer shows source; it is not a hosted preview.

Or make a separate copy from the repository root:

```sh
python skills/scrolling-presentations/scripts/create_presentation.py ../my-presentation
python -m http.server 4180 --bind 127.0.0.1 --directory ../my-presentation
```

Use `python3` where appropriate. Visit `http://127.0.0.1:4180/` on that machine. The output folder must be new. A new topic still needs new content; the copied files retain the Microsoft example until you adapt them.

The example covers Microsoft 365 chat agents, agent flows, Power Automate, Power Apps, Power Pages, Dataverse, and Foundry. It includes the flow comparison, a supplier-portal demo, a six-step walkthrough, motion controls, a tool selector, and expandable sources. All business interactions are illustrative.

## What's deliberately excluded

No private environment configuration, credentials, local browser state, cached research, video downloads, Python environments, or absolute personal paths are needed for this kit. Microsoft icon notices remain with the educational example. Existing third-party skills retain their attribution; no blanket license is imposed on them. The kit is independent and is not endorsed by Jack Roberts or Microsoft.
