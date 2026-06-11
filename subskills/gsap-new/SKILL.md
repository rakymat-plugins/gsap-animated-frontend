---
name: gsap-new
description: Orchestrate new GSAP work for new pages, new sections, or greenfield animation systems. Use when the user wants to add animations where there is no established motion implementation yet. Create or update .gsap artifacts, interview only when required, generate the animation specification and implementation plan, then apply implementation.
---

# GSAP New

Use this workflow for new pages, new sections, and greenfield animation work.

## Sequence

1. Read existing `.gsap` artifacts if present.
2. Inspect the real page/component files.
3. Run internal bootstrap helpers if artifacts are missing.
4. Interview only for missing decisions.
5. Update `.gsap/animation-spec.md` and `.gsap/pages/<page>.animation.md`.
6. Generate or refresh `.gsap/animation-plan.md`.
7. Implement section by section.
8. Update statuses in the page artifact.

## Internal Helper

Use:

```bash
python scripts/gsap_workflow.py gsap-new --path "<project>" --page "<page>"
```

This command should scaffold artifacts and prepare workflow state. It is the only public helper command for this mode.

## Interview Policy

Ask only for missing data:

- motion personality
- density
- scroll behavior
- section-level recipe choice
- mobile downgrade rules
- reduced-motion fallback

If the artifacts already contain these answers, continue without re-interviewing.

## Implementation Output

Before finishing, ensure:

- `.gsap/pages/<page>.animation.md` reflects actual status
- `.gsap/animation-plan.md` reflects the latest section order and recipes
- implementation follows current code, not generic examples
