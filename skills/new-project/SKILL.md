---
name: new-project
description: |
  Scaffold a new project by generating AI-filled spec, plan, tasks, and CLAUDE.md files from a one-line description. Creates specs/###-slug/ in the current working directory. Use when starting any new project, feature, or initiative and the user says "new project", "start a project", "scaffold", or provides a description to kick off structured project work.
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - PowerShell
---

# New Project Scaffolder

Generate a complete, AI-filled project spec package from a one-sentence description. Output goes into `specs/###-slug/` in the current working directory.

## Templates location

All 4 master templates live at:
```
C:\Users\VinceDavis\OneDrive - Illinois Park & Recreation Association\Desktop\Vince Work Hub\10-Tools, Apps & Automation\Scripts\Scripts\GardenApp\templates\
  spec-template.md
  plan-template.md
  tasks-template.md
  agent-file-template.md
```

Read these templates before generating output so you match their exact structure and section names.

## Steps

### 1. Parse arguments

The user's project description comes in as `$ARGUMENTS`. If empty, ask: "What is this project? Give me a one-sentence description."

### 2. Determine next project number

Scan the current working directory for a `specs/` folder. If it exists, find all subdirectories matching the pattern `###-*` (3-digit prefix), take the highest number, and increment by 1. If no `specs/` folder or no numbered folders exist, start at `001`.

### 3. Generate slug

Convert the description to a slug:
- Lowercase
- Replace spaces and special characters with hyphens
- Max 5 words / 40 characters
- Example: "Build a scoring dashboard for DA Committee" → `scoring-dashboard-da-committee`

### 4. Create folder

Create: `specs/###-slug/` in the current working directory.

### 5. Read templates

Read all 4 template files from the templates location above. Use them as the structural skeleton — keep every section heading, checklist, and field. Replace placeholder content with real project-specific content derived from the description.

### 6. Generate spec.md

Fill in the spec template with:
- **Feature name**: Derived from the description
- **Branch name**: `###-slug`
- **Date**: Today's date
- **Status**: Draft
- **Primary User Story**: Who will use this and what they'll accomplish
- **Acceptance Scenarios**: 3–5 Given/When/Then scenarios specific to this project
- **Edge Cases**: 2–3 realistic edge cases for this project
- **Functional Requirements**: FR-001 through FR-006 minimum, written as concrete testable statements (not placeholders). Mark anything genuinely unclear with `[NEEDS CLARIFICATION: specific question]`
- **Key Entities**: If the project involves data, name the entities and their key attributes

Do not leave any `[FEATURE NAME]` or similar placeholders — fill them all in.

### 7. Generate plan.md

Fill in the plan template with:
- **Feature**: The project name
- **Branch**: `###-slug`
- **Date**: Today's date
- **Spec link**: `./spec.md`
- **Technical Context**: Fill in Language/Version, Dependencies, Storage, Testing, Platform, Project Type, Performance Goals, Constraints, Scale/Scope based on what's inferable from the description. Mark genuinely unknown fields `NEEDS CLARIFICATION`.
- **Constitution Check**: Fill in reasonable initial values based on project type (single/web/mobile). Set to "Pending" where not yet determinable.
- **Project Structure**: Choose the right option (single/web/mobile) based on description and fill in structure accordingly.
- **Phase 0, 1, 2**: Keep the execution steps but annotate them with project-specific notes where helpful.
- **Progress Tracking**: Leave all checkboxes unchecked (this is a fresh plan).

### 8. Generate tasks.md

Fill in the tasks template with:
- **Feature name**: The project name
- **Phase 3.1 Setup**: 3 specific setup tasks for this project's actual tech stack
- **Phase 3.2 Tests**: 4–6 specific test tasks with real file paths (e.g., `tests/contract/test_scores_post.py`)
- **Phase 3.3 Core Implementation**: 6–8 implementation tasks with real file paths
- **Phase 3.4 Integration**: 3–5 integration tasks relevant to the project
- **Phase 3.5 Polish**: 4–5 polish/validation tasks
- Number all tasks T001, T002... sequentially
- Mark parallel-safe tasks with `[P]`
- Fill in the Dependencies and Parallel Example sections with real task IDs

### 9. Generate CLAUDE.md

Fill in the agent-file template with:
- **Project name**: The project name
- **Date**: Today's date
- **Active Technologies**: The stack inferred from the description (ask yourself: what would Vince most likely use for this given his stack — React/Vite, Flask, Python, vanilla JS, etc.)
- **Project Structure**: Match what was decided in plan.md
- **Commands**: Relevant dev commands for the chosen stack (e.g., `npm run dev`, `python -m flask run`)
- **Code Style**: Language-specific style notes
- **Recent Changes**: Leave this section as `[Initial scaffold — no changes yet]`
- Keep the `<!-- MANUAL ADDITIONS START/END -->` markers intact

### 10. Write files

Write all 4 files:
- `specs/###-slug/spec.md`
- `specs/###-slug/plan.md`
- `specs/###-slug/tasks.md`
- `specs/###-slug/CLAUDE.md`

### 11. Report

After writing, output a tight summary:
```
Created specs/###-slug/ with 4 files:
  spec.md    — [X] FRs, [X] acceptance scenarios
  plan.md    — [tech stack], [single/web/mobile] structure
  tasks.md   — T001–T0XX across 5 phases
  CLAUDE.md  — agent context ready

Next: review spec.md for any [NEEDS CLARIFICATION] items, then run /plan to execute Phase 0.
```

## Rules

- Never leave template placeholders like `[FEATURE NAME]`, `[DATE]`, `[LANGUAGE]` in the output. Fill them all in.
- If you can't confidently infer something from the description, mark it `NEEDS CLARIFICATION: <specific question>` rather than guessing.
- Default to Vince's stack when ambiguous: JS/React/Vite for frontend, Python/Flask for backend, vanilla JS for standalone tools.
- Keep CLAUDE.md under 150 lines.
- Do not create a `research.md`, `data-model.md`, or `contracts/` folder — those are generated later by the `/plan` command.
