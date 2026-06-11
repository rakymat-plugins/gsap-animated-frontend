# GSAP Animated Frontend

<p align="center">
  <img src="https://raw.githubusercontent.com/yousefabdallah171/gsap-animated-frontend/main/assets/gsap-skill-banner.svg" alt="GSAP Animated Frontend" width="800" />
</p>

<p align="center">
  <b>A persistent, recoverable GSAP workflow for coding agents.</b><br/>
  <sub>Two user-facing commands. Internal helpers. Persistent phased artifacts as the source of truth.</sub>
</p>

---

## What This Repo Is

This repo is a GSAP animation skill/workflow package designed to work across coding agents, not only one model.

It is built to work well with:

- Claude Code
- Codex CLI
- Cursor
- Gemini CLI
- any agent that can follow `SKILL.md`-style instructions

The core design goal is simple:

- only **2 user-facing commands**
- persistent workflow state in `.gsap/`
- recoverable progress after interruption
- internal Python helpers for scanning, artifact generation, interview generation, and phased workflow orchestration

---

## The 2 Commands

These are the only primary commands the user should see:

### `gsap-new`

Use for:

- new pages
- new sections
- greenfield animation work

What it does:

1. Creates or updates `.gsap` artifacts
2. Discovers framework, packages, structure, brand signals, and motion opportunities
3. Interviews only when required
4. Generates animation specifications
5. Generates a phased implementation plan
6. Prepares one-section-at-a-time task files

### `gsap-refactor`

Use for:

- existing pages/components
- improving current motion systems
- cleanup, accessibility, and performance hardening

What it does:

1. Reads existing code
2. Reads existing `.gsap` artifacts
3. Audits the current motion system
4. Generates a phased refactor plan
5. Applies safe improvements section by section
6. Updates artifacts

---

## Persistent State

The workflow state lives in the project being animated, not in chat history.

```text
your-project/
└── .gsap/
    ├── animation-spec.md
    ├── animation-plan.md
    ├── audit-report.md
    ├── tasks/
    │   └── homepage.tasks.md
    ├── phases/
    │   └── homepage/
    │       ├── p01-hero.md
    │       └── p02-feature-grid.md
    └── pages/
        ├── homepage.animation.md
        ├── schools.animation.md
        └── dashboard.animation.md
```

This means a fresh agent session can resume by reading `.gsap` files without needing prior conversation context.

---

## Architecture

```text
gsap-animated-frontend/
├── SKILL.md
├── gsap_cli.py
├── requirements.txt
├── scripts/
│   ├── gsap_workflow.py
│   ├── brand_extractor.py
│   ├── structure_search.py
│   ├── interview_generator.py
│   └── phase_planner.py
├── subskills/
│   ├── gsap-new/
│   │   └── SKILL.md
│   └── gsap-refactor/
│       └── SKILL.md
├── templates/
│   ├── animation-spec.md
│   ├── animation-plan.md
│   ├── audit-report.md
│   ├── animation-tasks.md
│   ├── page-animation.md
│   └── phase.md
├── references/
│   ├── animation-recipes.md
│   ├── gsap-core-patterns.md
│   ├── performance-guide.md
│   └── scroll-trigger-patterns.md
└── assets/
    └── gsap-skill-banner.svg
```

### Design Rules

- `SKILL.md` is the root router
- `subskills/gsap-new` and `subskills/gsap-refactor` are the only public workflows
- `scripts/gsap_workflow.py` orchestrates the workflow
- dedicated helper scripts extract brand signals, discover structure, generate interview questions, and build phases
- `templates/` creates persistent `.gsap` state for spec-driven execution
- `references/` holds optional detailed guidance

---

## Internal Helpers

The system may use internal script commands such as:

- artifact bootstrap
- brand extraction
- structure search
- interview question generation
- phase planning
- workflow state updates
- code inspection
- motion audit prep
- refactor plan preparation

These are internal implementation helpers, not part of the intended public UX.

The public UX stays centered on:

- `gsap-new`
- `gsap-refactor`

## Spec-Driven Workflow

This package is now designed to behave more like spec-driven development than a one-shot animation prompt.

The engine should:

1. discover the real project structure and visual language
2. write findings into `.gsap` artifacts
3. generate a phased plan
4. generate per-page task files
5. generate one phase file per section
6. implement one major section at a time

This prevents agents from trying to rebuild an entire page in one pass and usually leads to cleaner motion hierarchy, better reduced-motion coverage, and better final quality.

---

## Installation

### Install via skills.sh CLI

The official `skills.sh` docs recommend installing skills from your project root with:

```bash
npx skills add yousefabdallah171/gsap-animated-frontend
```

This is the best cross-agent install path for:

- Claude Code
- Codex
- Gemini
- Cursor
- other agents that support repo-scoped `SKILL.md` discovery

After installation, start a new agent session in that project so the skill files are picked up.

### Agent Notes

- Claude Code: run `npx skills add yousefabdallah171/gsap-animated-frontend` from the project root, then start a new Claude Code session.
- Codex: run `npx skills add yousefabdallah171/gsap-animated-frontend` from the project root, then start a new Codex session.
- Gemini: run `npx skills add yousefabdallah171/gsap-animated-frontend` from the project root, then start a new Gemini session.

### Clone as a skill package

```bash
git clone https://github.com/yousefabdallah171/gsap-animated-frontend.git
```

This manual clone option is still useful when you want to inspect or customize the skill package directly.

### Install Python dependencies

```bash
cd gsap-animated-frontend
pip install -r requirements.txt
```

---

## Usage

### Install into a project with skills.sh

```bash
npx skills add yousefabdallah171/gsap-animated-frontend
```

Then restart your agent session in that project.

### New animation work

```bash
python gsap_cli.py gsap-new --path "<project-path>" --page "homepage"
```

### Refactor existing animation work

```bash
python gsap_cli.py gsap-refactor --path "<project-path>" --page "homepage"
```

### What the install command does

The `skills` CLI installs the skill files into your repository so agents can reference `SKILL.md` and related files across sessions. This repo keeps the public workflow centered on:

- `gsap-new`
- `gsap-refactor`

---

## Philosophy

This repo is optimized around:

- purposeful motion, not random effects
- recoverable workflows, not chat-only memory
- simple UX, not command overload
- cross-agent compatibility, not one-tool lock-in
- persistent artifacts, not fragile context

---

## License

MIT
