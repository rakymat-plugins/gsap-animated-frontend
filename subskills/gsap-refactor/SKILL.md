---
name: gsap-refactor
description: Orchestrate safe GSAP improvements for existing pages or components. Use when the page already exists and needs better animation quality, cleanup, performance fixes, accessibility hardening, or a more coherent motion system. Read current code and .gsap artifacts first, audit the current motion system, build a refactor plan, apply safe improvements, then update artifacts.
---

# GSAP Refactor

Use this workflow for existing pages/components that already have code and may already have motion.

## Sequence

1. Read `.gsap` artifacts first.
2. Read the actual implementation files.
3. Run internal audit and scan helpers.
4. Identify what to preserve, remove, simplify, or improve.
5. Update `.gsap/audit-report.md` and `.gsap/animation-plan.md`.
6. Apply safe changes.
7. Update page artifact statuses and notes.

## Internal Helper

Use:

```bash
python scripts/gsap_workflow.py gsap-refactor --path "<project>" --page "<page>"
```

This command should gather current workflow state and write audit/refactor notes. It is the only public helper command for this mode.

## Refactor Rules

- preserve good motion when possible
- remove noisy or redundant effects
- add reduced-motion handling where missing
- reduce mobile-heavy patterns before adding more spectacle
- do not change the motion direction without updating `.gsap` artifacts

## Completion

Before finishing, ensure:

- `.gsap/audit-report.md` records major findings and fixes
- `.gsap/animation-plan.md` reflects the refactor priorities
- `.gsap/pages/<page>.animation.md` reflects the final status
