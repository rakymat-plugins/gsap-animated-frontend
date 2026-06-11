# GSAP Animated Frontend — Claude Code Skill

A comprehensive Claude Code skill that teaches Claude how to build production-grade animated websites and landing pages using **GSAP (GreenSock Animation Platform)**. Instead of generating generic, lifeless UIs, Claude conducts a structured discovery interview to understand your animation vision, then implements exactly what you want using battle-tested GSAP patterns.

---

## What This Skill Does

When you ask Claude to build or animate a website, this skill activates and runs a **4-phase discovery interview** before writing any code. This ensures animations match your vision — not Claude's default assumptions.

### Phase 1: Animation Philosophy

Claude asks about your site's overall animation personality:

| Style | Description | Example Sites |
|-------|-------------|---------------|
| **Subtle & Professional** | Gentle fades, smooth slides, minimal motion | Stripe, Linear, Booking.com |
| **Bold & Cinematic** | Large-scale reveals, dramatic parallax, full-screen transitions | Apple product pages, Awwwards winners |
| **Playful & Bouncy** | Spring physics, elastic easing, overshoots | Slack, Duolingo, Discord |
| **Elegant & Editorial** | Smooth text reveals, staggered typography, refined motion | Vogue, high-end real estate |

Also covers **animation density** (light touch → cinematic) and **scroll behavior** (reveals, parallax, pinned scenes, horizontal scroll).

### Phase 2: Section-by-Section Design

For each page section, Claude presents animation options with recommended defaults:

- **Hero Section** — Text reveal, cinematic zoom, particle backgrounds, morphing gradients, 3D perspective tilt
- **Card Grids** — Staggered fade-up, scale pop, flip reveal, masonry cascade, hover-only
- **Stats/Numbers** — Count up, odometer roll, SVG draw-in, scale + count
- **Testimonials** — Carousel slide, crossfade, stack cards, quote reveal
- **Footer/CTA** — Fade-up, background color shift, magnetic buttons

### Phase 3: Special Effects (Pick & Choose)

18 optional effects with complexity and performance ratings:

| Effect | Complexity | Performance |
|--------|-----------|-------------|
| Magnetic cursor | Medium | Low |
| Custom cursor | Medium | Low |
| Text split animations | Medium | Low-Medium |
| Smooth scroll (Lenis) | Low | Low |
| Page transitions | High | Medium |
| Parallax images | Low | Low |
| Floating elements | Low | Low |
| Reveal masks (clip-path) | Medium | Low |
| Pinned scroll sections | Medium | Medium |
| Horizontal scroll | Medium | Medium |
| SVG path draw | Medium | Low |
| Shape morphing | High | Medium |
| 3D card tilts | Low | Low |
| Stagger grids | Low | Low |
| Typewriter text | Low | Low |
| Number counters | Low | Low |
| Progress indicators | Low | Low |
| Image sequence (Apple-style) | High | High |

### Phase 4: Performance & Accessibility

- Device priority (mobile-first, desktop-focused, or equal)
- `prefers-reduced-motion` support (always enabled)
- Loading strategy (above-fold on load, below-fold on scroll)

---

## File Structure

```
gsap-animated-frontend/
├── SKILL.md                              # Main skill — interview flow + architecture rules
└── references/
    ├── gsap-core-patterns.md             # GSAP API, timelines, easing, React hooks
    ├── scroll-trigger-patterns.md        # ScrollTrigger: reveals, scrub, pinning, batch
    ├── animation-recipes.md              # 20+ copy-paste recipes for every animation type
    └── performance-guide.md              # GPU optimization, mobile, a11y, FOUC prevention
```

### File Details

| File | Lines | What's Inside |
|------|-------|---------------|
| `SKILL.md` | ~350 | Discovery interview questions, recommended options with examples, architecture rules, common mistakes, installation guide |
| `gsap-core-patterns.md` | ~200 | `gsap.to/from/fromTo`, timelines, stagger, easing reference table, `useGSAP` React hook, `gsap.quickTo`, `gsap.matchMedia`, `gsap.context`, utility methods |
| `scroll-trigger-patterns.md` | ~200 | 8 ScrollTrigger patterns (reveal, scrub, pin, horizontal scroll, batch, parallax, progress, class toggle), start/end position reference, responsive setup, debugging |
| `animation-recipes.md` | ~400 | Complete React components: hero animations (3 variants), card effects (stagger, hover lift, 3D tilt), number counters, text animations (word split, typewriter), scroll sections (pinned, color transition), navigation (shrink, mobile menu), special effects (magnetic button, custom cursor, reveal mask, SVG draw), page transitions, Lenis smooth scroll |
| `performance-guide.md` | ~180 | GPU-friendly vs layout-triggering properties, will-change strategy, ScrollTrigger batch optimization, mobile rules, `prefers-reduced-motion`, FOUC prevention, bundle size table, performance checklist |

---

## Installation

### As a Claude Code Personal Skill

Clone into your Claude Code skills directory:

```bash
# macOS/Linux
git clone git@github.com:yousefabdallah171/gsap-animated-frontend.git ~/.claude/skills/gsap-animated-frontend

# Windows
git clone git@github.com:yousefabdallah171/gsap-animated-frontend.git %USERPROFILE%\.claude\skills\gsap-animated-frontend
```

The skill auto-registers on next Claude Code session. No configuration needed.

### Manual Installation

Copy the `SKILL.md` and `references/` folder into your Claude Code skills directory at `~/.claude/skills/gsap-animated-frontend/`.

---

## Triggers

The skill activates when you mention any of these in conversation:

- `animate`, `animation`, `GSAP`, `motion`
- `parallax`, `scroll animation`, `hero animation`
- `landing page`, `micro-interactions`, `page transitions`
- Making a site feel "alive", "premium", "polished"
- Upgrading a static site to feel dynamic
- Referencing animated websites you want to replicate

---

## Example Usage

### Build a new animated landing page

```
> Build me an animated landing page for a school listing platform.
> I want it to feel like Booking.com — professional but alive.
```

Claude will run the full 4-phase interview, then implement with GSAP.

### Add animations to an existing site

```
> Add scroll animations to my homepage. Cards should stagger in,
> hero should have a text reveal, and stats should count up.
```

Claude will use the specific recipes from the cookbook.

### Upgrade a static site

```
> This site feels dead and static. Make it feel premium with
> subtle animations and micro-interactions.
```

Claude will interview you about animation style preferences, then apply targeted improvements.

---

## Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| [GSAP](https://gsap.com/) | 3.x | Core animation engine |
| [ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) | 3.x | Scroll-driven animations |
| [@gsap/react](https://www.npmjs.com/package/@gsap/react) | 2.x | React integration (`useGSAP` hook) |
| [Lenis](https://lenis.darkroom.engineering/) | Latest | Smooth scrolling (optional) |

### Project Setup

```bash
npm install gsap @gsap/react
# Optional:
npm install lenis
```

```tsx
// Register plugins once at app level
"use client";
import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);
```

---

## Architecture Rules

1. **One animation controller per section** — Each section gets one `useGSAP` hook
2. **Always clean up** — `useGSAP` with `scope` handles this automatically in React
3. **Use timelines for sequences** — Never chain `.to()` calls with delays
4. **GPU-friendly properties only** — Animate `transform` and `opacity`, never `width`/`height`/`top`/`left`
5. **Respect `prefers-reduced-motion`** — Always check and disable/simplify animations
6. **Mobile: less is more** — Disable parallax, reduce staggers, simplify scroll animations on touch
7. **Prevent FOUC** — Set initial hidden states in CSS, not just JS

---

## Key Recipes Included

| Category | Recipes |
|----------|---------|
| **Hero** | Text reveal, cinematic zoom, floating shapes background |
| **Cards** | Staggered reveal, hover lift + image zoom, 3D tilt on mouse |
| **Numbers** | Count up animation, stats with trend arrows |
| **Text** | Word-by-word reveal (no plugin needed), typewriter effect |
| **Scroll** | Pinned scene transitions, background color shift on scroll |
| **Nav** | Shrink on scroll, mobile menu reveal |
| **Effects** | Magnetic button, custom cursor, clip-path reveal mask, SVG line draw |
| **Integration** | Page transitions (Next.js), Lenis smooth scroll provider |

---

## Performance Targets

- Only animate GPU-composited properties (`transform`, `opacity`)
- `< 20` active ScrollTriggers per page
- Use `ScrollTrigger.batch()` for grids instead of individual triggers
- Mobile: no parallax, no pinning, shorter durations
- Bundle: ~41 KB total (gsap + ScrollTrigger + @gsap/react + Lenis)

---

## License

MIT

---

## Author

Built by [@yousefabdallah171](https://github.com/yousefabdallah171) as a Claude Code skill for creating production-grade animated frontends.