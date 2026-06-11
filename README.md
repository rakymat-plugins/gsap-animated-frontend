<p align="center">
  <img src="https://raw.githubusercontent.com/yousefabdallah171/gsap-animated-frontend/main/assets/gsap-skill-banner.svg" alt="GSAP Animated Frontend" width="800" />
</p>

<p align="center">
  <a href="#installation"><img src="https://img.shields.io/badge/Claude_Code-Skill-blueviolet?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0wIDE4Yy00LjQyIDAtOC0zLjU4LTgtOHMzLjU4LTggOC04IDggMy41OCA4IDgtMy41OCA4LTggOHoiLz48L3N2Zz4=" alt="Claude Code Skill" /></a>
  <a href="#cli-toolkit"><img src="https://img.shields.io/badge/Python-CLI_Toolkit-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python CLI" /></a>
  <a href="#animation-recipes"><img src="https://img.shields.io/badge/Recipes-20+-green?style=for-the-badge" alt="20+ Recipes" /></a>
  <a href="https://gsap.com"><img src="https://img.shields.io/badge/GSAP-3.12-88CE02?style=for-the-badge&logo=greensock&logoColor=white" alt="GSAP 3.12" /></a>
  <a href="#performance"><img src="https://img.shields.io/badge/Bundle-~41KB-orange?style=for-the-badge" alt="~41KB Bundle" /></a>
</p>

<p align="center">
  <b>A comprehensive Claude Code skill + Python CLI toolkit for building production-grade animated websites using GSAP.</b><br/>
  <sub>Discovery interview → Animation plan → Battle-tested implementation → Real-time audit</sub>
</p>

---

<!-- Animated floating elements using SVG animation -->
<p align="center">
  <svg width="600" height="120" viewBox="0 0 600 120" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#3b82f6;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:1" />
      </linearGradient>
      <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" style="stop-color:#22c55e;stop-opacity:0.8" />
        <stop offset="100%" style="stop-color:#06b6d4;stop-opacity:0.8" />
      </linearGradient>
    </defs>
    <!-- Floating circles -->
    <circle cx="50" cy="60" r="8" fill="url(#grad1)" opacity="0.7">
      <animate attributeName="cy" values="60;40;60" dur="3s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.7;1;0.7" dur="3s" repeatCount="indefinite" />
    </circle>
    <circle cx="150" cy="50" r="12" fill="url(#grad2)" opacity="0.5">
      <animate attributeName="cy" values="50;70;50" dur="4s" repeatCount="indefinite" />
      <animate attributeName="r" values="12;15;12" dur="4s" repeatCount="indefinite" />
    </circle>
    <circle cx="300" cy="60" r="6" fill="#febb02" opacity="0.8">
      <animate attributeName="cy" values="60;35;60" dur="2.5s" repeatCount="indefinite" />
      <animate attributeName="cx" values="300;310;300" dur="2.5s" repeatCount="indefinite" />
    </circle>
    <circle cx="450" cy="55" r="10" fill="url(#grad1)" opacity="0.6">
      <animate attributeName="cy" values="55;75;55" dur="3.5s" repeatCount="indefinite" />
    </circle>
    <circle cx="550" cy="65" r="7" fill="#ef4444" opacity="0.5">
      <animate attributeName="cy" values="65;45;65" dur="3s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.5;0.9;0.5" dur="3s" repeatCount="indefinite" />
    </circle>
    <!-- Floating rectangles -->
    <rect x="90" y="30" width="16" height="16" rx="3" fill="url(#grad2)" opacity="0.4" transform="rotate(15 98 38)">
      <animate attributeName="y" values="30;50;30" dur="4s" repeatCount="indefinite" />
      <animateTransform attributeName="transform" type="rotate" values="15 98 38;45 98 58;15 98 38" dur="4s" repeatCount="indefinite" />
    </rect>
    <rect x="380" y="40" width="14" height="14" rx="3" fill="#febb02" opacity="0.5" transform="rotate(-10 387 47)">
      <animate attributeName="y" values="40;25;40" dur="3s" repeatCount="indefinite" />
      <animateTransform attributeName="transform" type="rotate" values="-10 387 47;20 387 32;-10 387 47" dur="3s" repeatCount="indefinite" />
    </rect>
    <!-- Pulse rings -->
    <circle cx="220" cy="60" r="20" fill="none" stroke="url(#grad1)" stroke-width="1" opacity="0">
      <animate attributeName="r" values="10;30;10" dur="3s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.6;0;0.6" dur="3s" repeatCount="indefinite" />
    </circle>
    <circle cx="500" cy="60" r="15" fill="none" stroke="url(#grad2)" stroke-width="1" opacity="0">
      <animate attributeName="r" values="8;25;8" dur="2.5s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="0.5;0;0.5" dur="2.5s" repeatCount="indefinite" />
    </circle>
    <!-- Center text -->
    <text x="300" y="105" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" fill="#94a3b8" opacity="0.8">
      <animate attributeName="opacity" values="0.5;1;0.5" dur="4s" repeatCount="indefinite" />
      ✦ every element animated with purpose ✦
    </text>
  </svg>
</p>

---

## Table of Contents

- [What This Skill Does](#what-this-skill-does)
- [Installation](#installation)
- [CLI Toolkit](#cli-toolkit)
- [The Discovery Interview](#the-discovery-interview)
- [Animation Recipes](#animation-recipes)
- [Complete GSAP API Coverage](#complete-gsap-api-coverage)
- [Performance](#performance)
- [File Structure](#file-structure)
- [Triggers](#triggers)
- [Example Usage](#example-usage)
- [Technology Stack](#technology-stack)
- [Architecture Rules](#architecture-rules)
- [License](#license)

---

## What This Skill Does

<table>
<tr>
<td width="50%">

### Without This Skill ❌
- Claude adds basic `opacity` fades everywhere
- No discovery — guesses what animations you want
- No performance checks
- No accessibility (`prefers-reduced-motion`)
- Generic, lifeless motion
- No tooling or automation

</td>
<td width="50%">

### With This Skill ✅
- **4-phase discovery interview** before any code
- **20+ battle-tested recipes** with copy-paste components
- **Python CLI** that scans, audits, and watches in real-time
- **Accessibility-first** — reduced motion always respected
- **Performance-audited** — GPU-only properties, bundle-aware
- **Full GSAP API knowledge** from Context7 docs

</td>
</tr>
</table>

<!-- Animated divider -->
<p align="center">
  <svg width="400" height="30" viewBox="0 0 400 30" xmlns="http://www.w3.org/2000/svg">
    <line x1="0" y1="15" x2="400" y2="15" stroke="#1e293b" stroke-width="1"/>
    <circle cx="200" cy="15" r="4" fill="#3b82f6">
      <animate attributeName="r" values="4;6;4" dur="2s" repeatCount="indefinite"/>
      <animate attributeName="fill" values="#3b82f6;#8b5cf6;#3b82f6" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="180" cy="15" r="2" fill="#22c55e" opacity="0.6">
      <animate attributeName="cx" values="180;170;180" dur="3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="220" cy="15" r="2" fill="#febb02" opacity="0.6">
      <animate attributeName="cx" values="220;230;220" dur="3s" repeatCount="indefinite"/>
    </circle>
  </svg>
</p>

---

## Installation

### As a Claude Code Personal Skill (Recommended)

```bash
# macOS / Linux
git clone git@github.com:yousefabdallah171/gsap-animated-frontend.git ~/.claude/skills/gsap-animated-frontend

# Windows
git clone git@github.com:yousefabdallah171/gsap-animated-frontend.git %USERPROFILE%\.claude\skills\gsap-animated-frontend
```

The skill auto-registers on next Claude Code session. No configuration needed.

### Install Python CLI Dependencies

```bash
cd ~/.claude/skills/gsap-animated-frontend
pip install -r requirements.txt
```

Or install manually:

```bash
pip install rich click pyyaml jinja2 watchdog
```

---

## CLI Toolkit

The skill includes a real Python CLI that performs background automation — not just documentation, **actual tooling**.

<!-- Animated CLI showcase -->
<p align="center">
  <svg width="600" height="40" viewBox="0 0 600 40" xmlns="http://www.w3.org/2000/svg">
    <rect width="600" height="40" rx="8" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
    <text x="15" y="25" font-family="monospace" font-size="13" fill="#22c55e">$</text>
    <text x="30" y="25" font-family="monospace" font-size="13" fill="#f1f5f9">python gsap_cli.py</text>
    <text x="195" y="25" font-family="monospace" font-size="13" fill="#3b82f6">
      <animate attributeName="opacity" values="1;1;1;1;1;1" dur="12s" repeatCount="indefinite"/>
      scan
      <set attributeName="textContent" to="scan" begin="0s" dur="2s"/>
      <set attributeName="textContent" to="audit" begin="2s" dur="2s"/>
      <set attributeName="textContent" to="init" begin="4s" dur="2s"/>
      <set attributeName="textContent" to="report" begin="6s" dur="2s"/>
      <set attributeName="textContent" to="recipes" begin="8s" dur="2s"/>
      <set attributeName="textContent" to="watch" begin="10s" dur="2s"/>
    </text>
    <rect x="570" y="10" width="8" height="20" fill="#3b82f6" opacity="0.8">
      <animate attributeName="opacity" values="0.8;0;0.8" dur="1s" repeatCount="indefinite"/>
    </rect>
  </svg>
</p>

### Commands

| Command | Description | When to Use |
|---------|-------------|-------------|
| **`gsap init`** | Install GSAP deps, create config, scaffold hooks + CSS | Starting a new project or adding GSAP to existing |
| **`gsap scan`** | Scan project for GSAP usage + find opportunities | Before adding animations — see what's there and what's missing |
| **`gsap audit`** | Check performance, a11y, best practices. Health score 0-100 | After implementing animations — catch issues early |
| **`gsap report`** | Full report: coverage %, features used, score, recommendations | Before code review or deployment |
| **`gsap recipes`** | Browse all 20 recipes with descriptions and style tags | Choosing which animations to implement |
| **`gsap watch`** | Real-time file watcher — reports issues as you code | During active development |
| **`gsap config`** | Display/edit animation config (gsap-animations.yaml) | Reviewing or adjusting animation settings |

### What `gsap init` Scaffolds

```
your-project/
├── gsap-animations.yaml          ← Animation config (philosophy, sections, effects)
└── src/lib/animations/
    ├── use-animations.tsx         ← Hooks: useScrollReveal, useCountUp, useHoverLift, useMagneticButton
    ├── use-reduced-motion.tsx     ← prefers-reduced-motion React hook
    └── gsap-initial-states.css   ← Anti-FOUC classes + reduced-motion fallbacks
```

### What `gsap audit` Checks

| Check | Severity | What It Detects |
|-------|----------|-----------------|
| Layout-thrashing properties | 🔴 HIGH | Animating `width`/`height`/`top`/`left` instead of transforms |
| Missing useGSAP hook | 🟡 MEDIUM | GSAP in `useEffect` without cleanup — memory leaks |
| No reduced-motion check | 🔴 HIGH | ScrollTrigger used without `prefers-reduced-motion` |
| Too many ScrollTriggers | 🟡 MEDIUM | >15 individual triggers — should use `batch()` |
| Delay vs timeline | 🟢 LOW | Using `delay` instead of timeline position params |
| Static will-change | 🟢 LOW | CSS `will-change` left permanently — GSAP manages this |

### What `gsap scan` Finds

The scanner detects **18 GSAP patterns** in your code:

```
gsap.to  ·  gsap.from  ·  gsap.fromTo  ·  gsap.set  ·  gsap.timeline
ScrollTrigger  ·  useGSAP  ·  gsap.matchMedia  ·  gsap.context
gsap.quickTo  ·  gsap.registerPlugin  ·  Lenis  ·  ScrollSmoother
Flip  ·  Draggable  ·  SplitText  ·  MotionPath  ·  Observer
```

And identifies **animation opportunities** in un-animated sections:
- Hero sections without entrance animations
- Card grids without stagger effects
- Stats/numbers without count-up animations
- Images without hover effects
- Navigation without scroll behavior

---

## The Discovery Interview

Before writing ANY animation code, Claude runs a **4-phase structured interview**.

### Phase 1: Animation Philosophy

<table>
<tr><th>Question</th><th>Options</th></tr>
<tr>
<td><b>Q1: Animation personality?</b></td>
<td>

| Style | Feel | Examples |
|-------|------|----------|
| 🎯 **Subtle & Professional** | Clean, trustworthy | Stripe, Linear, Booking.com |
| 🎬 **Bold & Cinematic** | High impact, dramatic | Apple product pages |
| 🎪 **Playful & Bouncy** | Fun, spring physics | Slack, Duolingo |
| ✨ **Elegant & Editorial** | Refined, premium | Vogue, luxury real estate |

</td>
</tr>
<tr>
<td><b>Q2: Animation density?</b></td>
<td>

| Level | What Animates | Performance |
|-------|---------------|-------------|
| 💡 **Light Touch** | Hero + CTAs only | Excellent |
| ⚡ **Moderate** | Hero + sections + cards + hovers | Good |
| 🔥 **Heavy** | Everything + backgrounds + continuous | Moderate |
| 🎥 **Cinematic** | Each scroll section = choreographed scene | Variable |

</td>
</tr>
<tr>
<td><b>Q3: Scroll behavior?</b></td>
<td>

| Type | Plugin |
|------|--------|
| 📜 **Scroll-triggered reveals** | ScrollTrigger |
| 🏔️ **Parallax layers** | ScrollTrigger + scrub |
| 📌 **Scroll-locked scenes** | ScrollTrigger pin + scrub |
| ↔️ **Horizontal scroll** | ScrollTrigger + pin |
| ❌ **No scroll animations** | Core GSAP only |

</td>
</tr>
</table>

### Phase 2: Section-by-Section Design

For each page section, Claude presents options with recommended defaults:

```
┌─── Hero ───────────────────────────────────────────────────┐
│  ◉ Text Reveal (recommended)    ○ Cinematic Zoom           │
│  ○ Particle Background          ○ Video + Overlay           │
│  ○ Morphing Gradient            ○ 3D Perspective Tilt       │
└────────────────────────────────────────────────────────────┘

┌─── Cards ──────────────────────────────────────────────────┐
│  ◉ Staggered Fade-Up (rec.)    ○ Scale Pop                 │
│  ○ Flip Reveal                  ○ Masonry Cascade           │
│  ○ Hover Lift Only                                          │
└────────────────────────────────────────────────────────────┘

┌─── Stats ──────────────────────────────────────────────────┐
│  ◉ Count Up (rec.)             ○ Odometer Roll              │
│  ○ SVG Draw Icons              ○ Scale + Count              │
└────────────────────────────────────────────────────────────┘
```

### Phase 3: Special Effects (Pick & Choose)

18 optional effects with complexity and performance ratings:

<!-- Animated effects grid -->
<p align="center">
  <svg width="600" height="200" viewBox="0 0 600 200" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="card-bg" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" style="stop-color:#1e293b;stop-opacity:1" />
        <stop offset="100%" style="stop-color:#0f172a;stop-opacity:1" />
      </linearGradient>
    </defs>
    <!-- Row 1 -->
    <rect x="10" y="10" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="10;6;10" dur="3s" repeatCount="indefinite"/>
    </rect>
    <text x="75" y="32" text-anchor="middle" font-family="system-ui" font-size="11" fill="#3b82f6">🧲 Magnetic</text>
    <text x="75" y="48" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Cursor</text>

    <rect x="155" y="10" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="10;6;10" dur="3.5s" repeatCount="indefinite"/>
    </rect>
    <text x="220" y="32" text-anchor="middle" font-family="system-ui" font-size="11" fill="#22c55e">✂️ Text Split</text>
    <text x="220" y="48" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Animations</text>

    <rect x="300" y="10" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="10;6;10" dur="4s" repeatCount="indefinite"/>
    </rect>
    <text x="365" y="32" text-anchor="middle" font-family="system-ui" font-size="11" fill="#febb02">🌊 Smooth</text>
    <text x="365" y="48" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Scroll (Lenis)</text>

    <rect x="445" y="10" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="10;6;10" dur="3.2s" repeatCount="indefinite"/>
    </rect>
    <text x="510" y="32" text-anchor="middle" font-family="system-ui" font-size="11" fill="#ef4444">📌 Pinned</text>
    <text x="510" y="48" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Scroll Scenes</text>

    <!-- Row 2 -->
    <rect x="10" y="75" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="75;71;75" dur="3.8s" repeatCount="indefinite"/>
    </rect>
    <text x="75" y="97" text-anchor="middle" font-family="system-ui" font-size="11" fill="#8b5cf6">↔️ Horizontal</text>
    <text x="75" y="113" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Scroll</text>

    <rect x="155" y="75" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="75;71;75" dur="2.8s" repeatCount="indefinite"/>
    </rect>
    <text x="220" y="97" text-anchor="middle" font-family="system-ui" font-size="11" fill="#06b6d4">🎭 Reveal</text>
    <text x="220" y="113" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Masks</text>

    <rect x="300" y="75" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="75;71;75" dur="3.3s" repeatCount="indefinite"/>
    </rect>
    <text x="365" y="97" text-anchor="middle" font-family="system-ui" font-size="11" fill="#f97316">🎨 SVG</text>
    <text x="365" y="113" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Line Draw</text>

    <rect x="445" y="75" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="75;71;75" dur="4.2s" repeatCount="indefinite"/>
    </rect>
    <text x="510" y="97" text-anchor="middle" font-family="system-ui" font-size="11" fill="#ec4899">🔮 3D Card</text>
    <text x="510" y="113" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Tilt</text>

    <!-- Row 3 -->
    <rect x="80" y="140" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="140;136;140" dur="3.6s" repeatCount="indefinite"/>
    </rect>
    <text x="145" y="162" text-anchor="middle" font-family="system-ui" font-size="11" fill="#a3e635">🏔️ Parallax</text>
    <text x="145" y="178" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Layers</text>

    <rect x="225" y="140" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="140;136;140" dur="2.5s" repeatCount="indefinite"/>
    </rect>
    <text x="290" y="162" text-anchor="middle" font-family="system-ui" font-size="11" fill="#38bdf8">⌨️ Typewriter</text>
    <text x="290" y="178" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Text</text>

    <rect x="370" y="140" width="130" height="50" rx="8" fill="url(#card-bg)" stroke="#334155" stroke-width="1">
      <animate attributeName="y" values="140;136;140" dur="3.1s" repeatCount="indefinite"/>
    </rect>
    <text x="435" y="162" text-anchor="middle" font-family="system-ui" font-size="11" fill="#fbbf24">🔢 Counter</text>
    <text x="435" y="178" text-anchor="middle" font-family="system-ui" font-size="9" fill="#64748b">Animation</text>
  </svg>
</p>

### Phase 4: Performance & Accessibility

- Device priority: Mobile-first / Desktop-focused / Equal
- `prefers-reduced-motion`: **Always enabled** (non-negotiable)
- Loading strategy: Above-fold on load, below-fold on scroll

---

## Animation Recipes

### 20+ Production-Ready Recipes

Each recipe is a **complete, copy-paste React component** — not pseudocode.

<table>
<tr>
<th>Category</th>
<th>Recipe</th>
<th>Style</th>
<th>Description</th>
</tr>

<tr><td rowspan="3"><b>🎬 Hero</b></td>
<td><code>hero-text-reveal</code></td><td>Subtle</td>
<td>Headlines slide up with stagger, subtitle fades, CTA bounces</td></tr>
<tr><td><code>hero-cinematic-zoom</code></td><td>Bold</td>
<td>Background scales 1.3→1.0, content fades over gradient</td></tr>
<tr><td><code>hero-floating-shapes</code></td><td>Playful</td>
<td>Geometric shapes float continuously behind content</td></tr>

<tr><td rowspan="3"><b>🃏 Cards</b></td>
<td><code>staggered-card-reveal</code></td><td>Subtle</td>
<td>Cards fade-up one by one as row enters viewport</td></tr>
<tr><td><code>card-hover-lift</code></td><td>Subtle</td>
<td>Lift + shadow + image zoom on mouse enter</td></tr>
<tr><td><code>card-3d-tilt</code></td><td>Bold</td>
<td>Cards tilt in 3D space following mouse position</td></tr>

<tr><td rowspan="2"><b>🔢 Stats</b></td>
<td><code>count-up-numbers</code></td><td>Subtle</td>
<td>Numbers animate 0→target when visible</td></tr>
<tr><td><code>stats-trend-arrows</code></td><td>Subtle</td>
<td>Numbers count up with animated trend indicators</td></tr>

<tr><td rowspan="2"><b>✏️ Text</b></td>
<td><code>word-by-word-reveal</code></td><td>Elegant</td>
<td>Each word fades up individually with stagger</td></tr>
<tr><td><code>typewriter-effect</code></td><td>Playful</td>
<td>Characters appear one by one like typing</td></tr>

<tr><td rowspan="4"><b>📜 Scroll</b></td>
<td><code>pinned-scene-transitions</code></td><td>Cinematic</td>
<td>Section pins while content transitions inside</td></tr>
<tr><td><code>background-color-shift</code></td><td>Elegant</td>
<td>Background color morphs as you scroll between sections</td></tr>
<tr><td><code>parallax-layers</code></td><td>Cinematic</td>
<td>Background/mid/foreground at different scroll speeds</td></tr>
<tr><td><code>horizontal-scroll</code></td><td>Cinematic</td>
<td>Section scrolls horizontally on vertical scroll input</td></tr>

<tr><td rowspan="2"><b>🧭 Nav</b></td>
<td><code>navbar-shrink-scroll</code></td><td>Subtle</td>
<td>Navbar shrinks + adds blur on scroll down</td></tr>
<tr><td><code>mobile-menu-reveal</code></td><td>Subtle</td>
<td>Menu items stagger in from right on open</td></tr>

<tr><td rowspan="4"><b>✨ Effects</b></td>
<td><code>magnetic-button</code></td><td>Playful</td>
<td>Buttons subtly follow cursor on hover</td></tr>
<tr><td><code>custom-cursor</code></td><td>Bold</td>
<td>Replace default cursor with animated follower</td></tr>
<tr><td><code>clip-path-reveal</code></td><td>Elegant</td>
<td>Content revealed through animated clip-path mask</td></tr>
<tr><td><code>svg-line-draw</code></td><td>Elegant</td>
<td>SVG strokes draw themselves on screen</td></tr>

<tr><td><b>🌊 Global</b></td>
<td><code>smooth-scroll-lenis</code></td><td>Subtle</td>
<td>Replace native scroll with Lenis smooth scroll</td></tr>
</table>

---

## Complete GSAP API Coverage

This skill has **complete knowledge** of the GSAP ecosystem, sourced from Context7 documentation (7,900+ code snippets).

### Core Methods

```
gsap.to()          gsap.from()         gsap.fromTo()       gsap.set()
gsap.timeline()    gsap.registerPlugin()  gsap.matchMedia()  gsap.context()
gsap.quickTo()     gsap.quickSetter()  gsap.registerEffect()  gsap.defaults()
gsap.getProperty() gsap.killTweensOf() gsap.exportRoot()   gsap.globalTimeline
```

### All Special Properties

```
duration · ease · delay · stagger · repeat · yoyo · yoyoEase · paused
reversed · overwrite · onStart · onUpdate · onComplete · onRepeat
onReverseComplete · onInterrupt · keyframes · startAt · invalidate
repeatDelay · repeatRefresh · runBackwards · lazy · immediateRender · id
```

### ScrollTrigger (Complete API)

```
trigger · start · end · endTrigger · scrub · pin · pinSpacing · snap
toggleActions · toggleClass · markers · anticipatePin · containerAnimation
preventOverlaps · fastScrollEnd · onEnter · onLeave · onEnterBack
onLeaveBack · onUpdate · onToggle · onRefresh · once · invalidateOnRefresh
```

### 30+ Easing Functions

```
power1-4 (.in .out .inOut) · back · bounce · elastic · expo · circ · sine
linear · none · steps(N) · slow(0.7, 0.7, false) · CustomEase.create()
rough({ strength, points, template }) · expoScale(1, 10, "power2.inOut")
```

### All Utility Methods

```
toArray · snap · clamp · mapRange · normalize · wrap · wrapYoyo
distribute · interpolate · random · pipe · shuffle · selector · unitize
```

### All Plugins

| Plugin | Type | What It Does |
|--------|------|-------------|
| **ScrollTrigger** | Free | Scroll-driven animations & triggers |
| **Observer** | Free | Unified touch/scroll/pointer events |
| **Flip** | Free | Layout transition animations (FLIP technique) |
| **Draggable** | Free | Drag-and-drop with inertia |
| **MotionPathPlugin** | Free | Animate along SVG/custom paths |
| **TextPlugin** | Free | Animate text content changes |
| **EaselPlugin** | Free | Adobe Animate/CreateJS integration |
| **PixiPlugin** | Free | PixiJS renderer integration |
| **SplitText** | Club | Character/word/line splitting |
| **ScrollSmoother** | Club | Smooth scrolling with effects |
| **MorphSVGPlugin** | Club | Shape morphing between SVG paths |
| **DrawSVGPlugin** | Club | Animate SVG stroke drawing |
| **ScrambleTextPlugin** | Club | Scramble text characters |
| **CustomEase** | Club | Bezier curve easing editor |
| **CustomWiggle** | Club | Random wiggle easings |
| **GSDevTools** | Club | Visual animation debugger |

---

## Performance

<!-- Animated performance badge -->
<p align="center">
  <svg width="500" height="80" viewBox="0 0 500 80" xmlns="http://www.w3.org/2000/svg">
    <rect width="500" height="80" rx="12" fill="#0f172a" stroke="#1e293b" stroke-width="1"/>
    <!-- Bundle size bar -->
    <text x="20" y="25" font-family="system-ui" font-size="11" fill="#94a3b8">Bundle Size</text>
    <rect x="120" y="14" width="200" height="16" rx="4" fill="#1e293b"/>
    <rect x="120" y="14" width="82" height="16" rx="4" fill="#22c55e">
      <animate attributeName="width" values="0;82" dur="1.5s" fill="freeze"/>
    </rect>
    <text x="330" y="26" font-family="monospace" font-size="11" fill="#22c55e">~41KB gzipped</text>
    <!-- Performance score -->
    <text x="20" y="55" font-family="system-ui" font-size="11" fill="#94a3b8">GPU Properties</text>
    <rect x="120" y="44" width="200" height="16" rx="4" fill="#1e293b"/>
    <rect x="120" y="44" width="200" height="16" rx="4" fill="#3b82f6">
      <animate attributeName="width" values="0;200" dur="1.5s" fill="freeze"/>
    </rect>
    <text x="330" y="56" font-family="monospace" font-size="11" fill="#3b82f6">100% composited</text>
  </svg>
</p>

### Bundle Breakdown

| Package | Size (gzip) | Required |
|---------|-------------|----------|
| gsap core | ~24 KB | ✅ Yes |
| ScrollTrigger | ~10 KB | ✅ Most projects |
| @gsap/react | ~2 KB | ✅ React projects |
| Lenis | ~5 KB | ❌ Optional |
| **Total** | **~41 KB** | |

### Performance Rules

| Rule | Why |
|------|-----|
| **Only animate `transform` + `opacity`** | These are GPU-composited — no layout reflow |
| **`< 20` ScrollTriggers per page** | Each trigger listens to scroll events |
| **Use `ScrollTrigger.batch()`** | 1 trigger for 50 cards > 50 individual triggers |
| **Mobile: no parallax/pinning** | Touch scroll + pinning = janky experience |
| **`scrub: 1`** not `scrub: true` | Smoothing prevents jerky scroll-linked motion |
| **Always `prefers-reduced-motion`** | Accessibility is non-negotiable |
| **CSS initial states** | Prevent FOUC (Flash of Unstyled Content) |

### Performance Checklist

```
✅ Only animating transform and opacity
✅ ScrollTrigger.batch() for repeated elements
✅ < 20 active ScrollTriggers per page
✅ Mobile: no parallax, no pinning, simplified animations
✅ prefers-reduced-motion respected
✅ CSS initial states prevent FOUC
✅ Above-fold animates on load, below-fold on scroll
✅ Unused GSAP plugins not imported
✅ ScrollTrigger.refresh() called after dynamic content
✅ Animations cleaned up on component unmount
```

---

## File Structure

```
gsap-animated-frontend/
├── SKILL.md                              # Main skill — interview + rules + CLI docs + full API
├── gsap_cli.py                           # Python CLI toolkit (scan, audit, init, watch, recipes)
├── requirements.txt                      # Python dependencies
├── README.md                             # This file
├── assets/
│   └── gsap-skill-banner.svg            # Animated banner
└── references/
    ├── gsap-core-patterns.md             # GSAP API, timelines, easing, React hooks
    ├── scroll-trigger-patterns.md        # ScrollTrigger: reveals, scrub, pinning, batch
    ├── animation-recipes.md              # 20+ copy-paste component recipes
    └── performance-guide.md              # GPU optimization, mobile, a11y, FOUC prevention
```

| File | What's Inside | Lines |
|------|---------------|-------|
| `SKILL.md` | Discovery interview, CLI commands, full GSAP API reference, architecture rules | ~350 |
| `gsap_cli.py` | 7 CLI commands with Rich UI — real project scanning, auditing, scaffolding | ~700 |
| `gsap-core-patterns.md` | Tweens, timelines, easing table, useGSAP, matchMedia, context, utilities | ~200 |
| `scroll-trigger-patterns.md` | 8 patterns: reveal, scrub, pin, horizontal, batch, parallax, progress, toggle | ~200 |
| `animation-recipes.md` | Complete React components for every animation type | ~400 |
| `performance-guide.md` | GPU properties, ScrollTrigger optimization, mobile, a11y, FOUC, bundle | ~180 |

---

## Triggers

The skill activates when you mention any of these:

```
animate · animation · GSAP · motion · parallax · scroll animation
hero animation · landing page · micro-interactions · page transitions
make it alive · make it premium · make it polished · upgrade the UI
add motion · scroll effects · hover effects · entrance animations
```

---

## Example Usage

### Build a new animated landing page

```
> Build me an animated landing page for a school listing platform.
> I want it to feel like Booking.com — professional but alive.
```

Claude runs the full 4-phase interview, generates `gsap-animations.yaml`, then implements.

### Add animations to existing site

```
> Add scroll animations to my homepage. Cards should stagger in,
> hero should have a text reveal, and stats should count up.
```

Claude uses specific recipes from the cookbook.

### Audit existing animations

```
> Run gsap audit on my project and fix any issues.
```

Claude runs the Python CLI, gets the health score, then fixes detected issues.

### Scan for opportunities

```
> What animations could we add to this site? Scan it first.
```

Claude runs `gsap scan`, reviews opportunities, then proposes an animation plan.

---

## Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| [GSAP](https://gsap.com/) | 3.12+ | Core animation engine |
| [ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) | 3.12+ | Scroll-driven animations |
| [@gsap/react](https://www.npmjs.com/package/@gsap/react) | 2.x | React integration (`useGSAP` hook) |
| [Lenis](https://lenis.darkroom.engineering/) | Latest | Smooth scrolling (optional) |
| [Python](https://python.org) | 3.8+ | CLI toolkit |
| [Rich](https://github.com/Textualize/rich) | 13+ | Beautiful CLI output |
| [Click](https://click.palletsprojects.com/) | 8+ | CLI framework |
| [Watchdog](https://github.com/gorakhargosh/watchdog) | 3+ | File system watcher |

---

## Architecture Rules

1. **One animation controller per section** — Each section gets one `useGSAP` hook
2. **Always clean up** — `useGSAP` with `scope` handles this automatically in React
3. **Use timelines for sequences** — Never chain `.to()` calls with delays
4. **GPU-friendly properties only** — Animate `transform` and `opacity`, never `width`/`height`/`top`/`left`
5. **Respect `prefers-reduced-motion`** — Always check and disable/simplify animations
6. **Mobile: less is more** — Disable parallax, reduce staggers, simplify scroll animations on touch
7. **Prevent FOUC** — Set initial hidden states in CSS, not just JS
8. **ScrollTrigger.batch()** — Use for any group of >5 similar elements
9. **ScrollTrigger.refresh()** — Call after dynamic content loads or layout shifts
10. **Config-driven** — Animation choices stored in `gsap-animations.yaml`, not hardcoded

---

## License

MIT

---

<p align="center">
  <svg width="400" height="60" viewBox="0 0 400 60" xmlns="http://www.w3.org/2000/svg">
    <text x="200" y="25" text-anchor="middle" font-family="system-ui, sans-serif" font-size="14" fill="#64748b">
      Built with ✦ by
    </text>
    <text x="200" y="48" text-anchor="middle" font-family="system-ui, sans-serif" font-size="13" font-weight="bold" fill="#3b82f6">
      @yousefabdallah171
      <animate attributeName="fill" values="#3b82f6;#8b5cf6;#3b82f6" dur="3s" repeatCount="indefinite"/>
    </text>
    <!-- Floating dots around author -->
    <circle cx="120" cy="35" r="3" fill="#22c55e" opacity="0.5">
      <animate attributeName="cy" values="35;28;35" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="280" cy="35" r="3" fill="#febb02" opacity="0.5">
      <animate attributeName="cy" values="35;42;35" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="140" cy="45" r="2" fill="#ef4444" opacity="0.4">
      <animate attributeName="cx" values="140;135;140" dur="3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="260" cy="25" r="2" fill="#8b5cf6" opacity="0.4">
      <animate attributeName="cx" values="260;265;260" dur="3s" repeatCount="indefinite"/>
    </circle>
  </svg>
</p>

<p align="center">
  <sub>A Claude Code skill for creating production-grade animated frontends with GSAP.</sub>
</p>