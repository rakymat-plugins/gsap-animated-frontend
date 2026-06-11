#!/usr/bin/env python3
"""
GSAP Animated Frontend — CLI Toolkit
=====================================
Real tooling that powers the GSAP animation skill.
Scans projects, generates animation configs, scaffolds components,
audits performance, and watches for animation issues in real-time.

Commands:
  gsap init          — Initialize GSAP in a project (install deps, register plugins)
  gsap scan          — Scan project for animation opportunities & current GSAP usage
  gsap generate      — Generate animation components from interview config
  gsap audit         — Audit existing animations for performance & accessibility
  gsap watch         — Watch project files and report animation issues in real-time
  gsap recipes       — Interactive recipe browser — pick and scaffold animations
  gsap config        — Generate/edit animation config from interview answers
  gsap report        — Full animation report: coverage, performance score, a11y
"""

import os
import sys
import json
import re
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

try:
    import click
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.tree import Tree
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.syntax import Syntax
    from rich.markdown import Markdown
    from rich import box
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    from jinja2 import Environment, BaseLoader
    HAS_JINJA = True
except ImportError:
    HAS_JINJA = False


# ─── Constants ────────────────────────────────────────────────────────────────

GSAP_VERSION = "3.12"
ANIMATION_CONFIG_FILE = "gsap-animations.yaml"
SUPPORTED_FRAMEWORKS = ["next", "react", "vue", "svelte", "vanilla"]

GPU_SAFE_PROPERTIES = {"x", "y", "z", "scale", "scaleX", "scaleY", "rotation",
                       "rotateX", "rotateY", "rotateZ", "opacity", "xPercent",
                       "yPercent", "skewX", "skewY"}

LAYOUT_THRASHING_PROPERTIES = {"width", "height", "top", "left", "right", "bottom",
                                "margin", "marginTop", "marginBottom", "marginLeft",
                                "marginRight", "padding", "paddingTop", "paddingBottom",
                                "paddingLeft", "paddingRight", "fontSize", "lineHeight",
                                "borderWidth"}

console = Console(force_terminal=True) if HAS_RICH else None


# ─── Utilities ────────────────────────────────────────────────────────────────

def find_project_root(start_path="."):
    """Walk up to find package.json or nearest git root."""
    p = Path(start_path).resolve()
    while p != p.parent:
        if (p / "package.json").exists():
            return p
        if (p / ".git").exists():
            return p
        p = p.parent
    return Path(start_path).resolve()


def detect_framework(root: Path) -> str:
    """Detect which framework the project uses."""
    pkg = root / "package.json"
    if not pkg.exists():
        return "vanilla"
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        if "next" in deps:
            return "next"
        if "react" in deps or "react-dom" in deps:
            return "react"
        if "vue" in deps:
            return "vue"
        if "svelte" in deps:
            return "svelte"
    except Exception:
        pass
    return "vanilla"


def scan_files(root: Path, extensions=(".tsx", ".ts", ".jsx", ".js", ".vue", ".svelte")):
    """Recursively find all source files, excluding node_modules."""
    files = []
    skip_dirs = {"node_modules", ".next", "dist", ".git", ".pnpm", "__pycache__", ".turbo"}

    def _walk(directory: Path):
        try:
            for entry in directory.iterdir():
                if entry.is_dir():
                    if entry.name not in skip_dirs:
                        _walk(entry)
                elif entry.suffix in extensions:
                    files.append(entry)
        except (PermissionError, OSError):
            pass

    src_dir = root / "src"
    if src_dir.exists():
        _walk(src_dir)
    # Also check root-level files and common dirs
    for d in ["app", "pages", "components", "lib", "packages"]:
        p = root / d
        if p.exists() and p != src_dir:
            _walk(p)
    # Check packages in monorepo
    packages_dir = root / "packages"
    if packages_dir.exists():
        _walk(packages_dir)
    # Check apps in monorepo
    apps_dir = root / "apps"
    if apps_dir.exists():
        _walk(apps_dir)

    return sorted(set(files))


def find_gsap_usage(file_path: Path):
    """Parse a file for GSAP usage patterns."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    findings = []
    lines = content.split("\n")

    patterns = {
        "gsap.to": r"gsap\.to\s*\(",
        "gsap.from": r"gsap\.from\s*\(",
        "gsap.fromTo": r"gsap\.fromTo\s*\(",
        "gsap.set": r"gsap\.set\s*\(",
        "gsap.timeline": r"gsap\.timeline\s*\(",
        "ScrollTrigger": r"ScrollTrigger",
        "useGSAP": r"useGSAP\s*\(",
        "gsap.matchMedia": r"gsap\.matchMedia\s*\(",
        "gsap.context": r"gsap\.context\s*\(",
        "gsap.quickTo": r"gsap\.quickTo\s*\(",
        "gsap.registerPlugin": r"gsap\.registerPlugin\s*\(",
        "Lenis": r"new\s+Lenis\s*\(",
        "ScrollSmoother": r"ScrollSmoother",
        "Flip": r"Flip\.(fit|from|to|getState)",
        "Draggable": r"Draggable\.create",
        "SplitText": r"new\s+SplitText\s*\(",
        "MotionPath": r"MotionPathPlugin",
        "Observer": r"Observer\.create",
    }

    for i, line in enumerate(lines, 1):
        for name, pattern in patterns.items():
            if re.search(pattern, line):
                findings.append({
                    "type": name,
                    "line": i,
                    "code": line.strip()[:120],
                    "file": str(file_path),
                })

    return findings


def find_animation_issues(file_path: Path):
    """Find performance and accessibility issues in GSAP code."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    issues = []
    lines = content.split("\n")

    for i, line in enumerate(lines, 1):
        # Check for layout-thrashing properties
        for prop in LAYOUT_THRASHING_PROPERTIES:
            if re.search(rf'["\'{{\s]{prop}\s*:', line) and ("gsap." in line or "tl." in line or ".to(" in line or ".from(" in line):
                issues.append({
                    "severity": "HIGH",
                    "line": i,
                    "issue": f"Animating layout property '{prop}' — causes reflow. Use transform (x/y/scale) instead.",
                    "file": str(file_path),
                })

        # Check for missing cleanup
        if "gsap.to(" in line or "gsap.from(" in line or "gsap.timeline(" in line:
            if "useEffect" in content and "useGSAP" not in content:
                issues.append({
                    "severity": "MEDIUM",
                    "line": i,
                    "issue": "GSAP in useEffect without useGSAP hook — animations won't auto-cleanup on unmount.",
                    "file": str(file_path),
                })
                break

        # Check for delay instead of timeline
        if re.search(r"delay\s*:\s*\d", line) and ("gsap.to" in line or "gsap.from" in line):
            issues.append({
                "severity": "LOW",
                "line": i,
                "issue": "Using 'delay' in standalone tween — consider timeline position parameters instead.",
                "file": str(file_path),
            })

        # Check for missing reduced-motion
        if "ScrollTrigger" in content and "prefers-reduced-motion" not in content and "matchMedia" not in content:
            if "ScrollTrigger" in line:
                issues.append({
                    "severity": "HIGH",
                    "line": i,
                    "issue": "ScrollTrigger used without prefers-reduced-motion check. Accessibility issue.",
                    "file": str(file_path),
                })
                break

        # Check for too many individual ScrollTriggers
        if "scrollTrigger:" in line or "ScrollTrigger.create" in line:
            st_count = content.count("scrollTrigger:") + content.count("ScrollTrigger.create")
            if st_count > 15:
                issues.append({
                    "severity": "MEDIUM",
                    "line": i,
                    "issue": f"{st_count} ScrollTriggers in one file — consider ScrollTrigger.batch() for repeated elements.",
                    "file": str(file_path),
                })
                break

        # Check for will-change left permanently
        if "will-change" in line and ".css" not in str(file_path) and "willChange" not in line:
            issues.append({
                "severity": "LOW",
                "line": i,
                "issue": "Static 'will-change' found — GSAP manages this automatically. Remove to avoid GPU memory waste.",
                "file": str(file_path),
            })

    return issues


def find_animation_opportunities(file_path: Path):
    """Find elements that could benefit from animations."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    opportunities = []

    # Hero sections without animation
    if re.search(r'(hero|Hero|banner|Banner)', content) and not re.search(r'gsap|useGSAP|framer-motion|motion', content):
        opportunities.append({
            "section": "Hero",
            "suggestion": "Add text reveal + CTA bounce animation",
            "recipe": "hero-text-reveal",
            "file": str(file_path),
        })

    # Card grids without stagger
    if re.search(r'(card|Card|grid|Grid)', content) and "stagger" not in content:
        if re.search(r'map\s*\(|\.map\(|v-for|{#each', content):
            opportunities.append({
                "section": "Card Grid",
                "suggestion": "Add staggered fade-up entrance on scroll",
                "recipe": "staggered-card-reveal",
                "file": str(file_path),
            })

    # Stats/numbers without count animation
    if re.search(r'(stat|Stat|count|metric|number|dashboard)', content, re.IGNORECASE):
        if "onUpdate" not in content and "countUp" not in content.lower():
            opportunities.append({
                "section": "Stats/Numbers",
                "suggestion": "Add count-up animation when section enters viewport",
                "recipe": "count-up-numbers",
                "file": str(file_path),
            })

    # Images without hover effect
    if re.search(r'<img|<Image|backgroundImage', content) and "mouseenter" not in content and "onMouseEnter" not in content:
        if "hover" not in content:
            opportunities.append({
                "section": "Images",
                "suggestion": "Add hover zoom + lift effect on image containers",
                "recipe": "card-hover-lift",
                "file": str(file_path),
            })

    # Navigation without scroll behavior
    if re.search(r'(nav|Nav|header|Header|navbar|Navbar)', content):
        if "scroll" not in content.lower() and "sticky" not in content:
            opportunities.append({
                "section": "Navigation",
                "suggestion": "Add shrink-on-scroll + backdrop blur effect",
                "recipe": "navbar-shrink-scroll",
                "file": str(file_path),
            })

    return opportunities


# ─── Animation Config ─────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "version": "1.0",
    "project": {
        "name": "",
        "framework": "next",
        "gsap_version": GSAP_VERSION,
    },
    "philosophy": {
        "personality": "subtle-professional",
        "density": "moderate",
        "scroll_behavior": "scroll-triggered-reveals",
    },
    "sections": {
        "hero": {
            "animation": "text-reveal",
            "enabled": True,
        },
        "cards": {
            "animation": "staggered-fade-up",
            "enabled": True,
        },
        "stats": {
            "animation": "count-up",
            "enabled": True,
        },
        "testimonials": {
            "animation": "carousel-slide",
            "enabled": True,
        },
        "cta": {
            "animation": "simple-fade-up",
            "enabled": True,
        },
    },
    "effects": {
        "smooth_scroll": False,
        "magnetic_buttons": False,
        "custom_cursor": False,
        "parallax_images": False,
        "text_split": False,
        "page_transitions": False,
        "floating_elements": False,
        "reveal_masks": False,
        "tilt_cards": False,
        "typewriter": False,
        "number_counters": True,
        "progress_indicators": False,
    },
    "performance": {
        "device_priority": "mobile-first",
        "reduced_motion": True,
        "loading_strategy": "above-fold-load-below-fold-scroll",
    },
}


# ─── Component Templates ─────────────────────────────────────────────────────

TEMPLATES = {
    "gsap-provider": '''\
"use client";
import {{ useEffect }} from "react";
import {{ gsap }} from "gsap";
import {{ ScrollTrigger }} from "gsap/ScrollTrigger";
{smooth_scroll_import}
gsap.registerPlugin(ScrollTrigger);

export function GSAPProvider({{ children }}: {{ children: React.ReactNode }}) {{
{smooth_scroll_body}
  return <>{{}}{children}</>;
}}
''',

    "use-animation": '''\
"use client";
import {{ useRef }} from "react";
import {{ gsap }} from "gsap";
import {{ useGSAP }} from "@gsap/react";
import {{ ScrollTrigger }} from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

/**
 * Hook: useScrollReveal
 * Reveals elements with fade-up animation when they enter viewport.
 */
export function useScrollReveal(selector: string, options?: {{
  y?: number;
  duration?: number;
  stagger?: number;
  start?: string;
}}) {{
  const containerRef = useRef<HTMLDivElement>(null);
  const {{ y = 40, duration = 0.6, stagger = 0.08, start = "top 85%" }} = options || {{}};

  useGSAP(() => {{
    ScrollTrigger.batch(selector, {{
      onEnter: (elements) => {{
        gsap.from(elements, {{
          opacity: 0,
          y,
          duration,
          stagger,
          ease: "power2.out",
        }});
      }},
      start,
    }});
  }}, {{ scope: containerRef }});

  return containerRef;
}}

/**
 * Hook: useCountUp
 * Animates numbers from 0 to target when element enters viewport.
 */
export function useCountUp(selector: string) {{
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {{
    const counters = gsap.utils.toArray<HTMLElement>(selector);
    counters.forEach((el) => {{
      const target = parseInt(el.dataset.target || "0", 10);
      const obj = {{ value: 0 }};
      gsap.to(obj, {{
        value: target,
        duration: 2,
        ease: "power2.out",
        snap: {{ value: 1 }},
        scrollTrigger: {{ trigger: el, start: "top 80%" }},
        onUpdate: () => {{ el.textContent = obj.value.toLocaleString(); }},
      }});
    }});
  }}, {{ scope: containerRef }});

  return containerRef;
}}

/**
 * Hook: useHoverLift
 * Adds hover lift + shadow effect to cards.
 */
export function useHoverLift(selector: string) {{
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {{
    const cards = gsap.utils.toArray<HTMLElement>(selector);
    cards.forEach((card) => {{
      card.addEventListener("mouseenter", () => {{
        gsap.to(card, {{ y: -6, boxShadow: "0 20px 40px rgba(0,0,0,0.25)", duration: 0.3, ease: "power2.out" }});
      }});
      card.addEventListener("mouseleave", () => {{
        gsap.to(card, {{ y: 0, boxShadow: "0 4px 12px rgba(0,0,0,0.08)", duration: 0.3, ease: "power2.out" }});
      }});
    }});
  }}, {{ scope: containerRef }});

  return containerRef;
}}

/**
 * Hook: useMagneticButton
 * Makes buttons follow cursor slightly on hover.
 */
export function useMagneticButton(selector: string, strength = 0.3) {{
  const containerRef = useRef<HTMLDivElement>(null);

  useGSAP(() => {{
    const buttons = gsap.utils.toArray<HTMLElement>(selector);
    buttons.forEach((btn) => {{
      const xTo = gsap.quickTo(btn, "x", {{ duration: 0.4, ease: "power3" }});
      const yTo = gsap.quickTo(btn, "y", {{ duration: 0.4, ease: "power3" }});

      btn.addEventListener("mousemove", (e) => {{
        const rect = btn.getBoundingClientRect();
        xTo((e.clientX - rect.left - rect.width / 2) * strength);
        yTo((e.clientY - rect.top - rect.height / 2) * strength);
      }});
      btn.addEventListener("mouseleave", () => {{ xTo(0); yTo(0); }});
    }});
  }}, {{ scope: containerRef }});

  return containerRef;
}}
''',

    "reduced-motion": '''\
"use client";
import {{ useEffect, useState }} from "react";

export function useReducedMotion() {{
  const [prefersReduced, setPrefersReduced] = useState(false);

  useEffect(() => {{
    const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
    setPrefersReduced(mq.matches);
    const handler = (e: MediaQueryListEvent) => setPrefersReduced(e.matches);
    mq.addEventListener("change", handler);
    return () => mq.removeEventListener("change", handler);
  }}, []);

  return prefersReduced;
}}
''',

    "scroll-reveal-css": '''\
/* GSAP Animation Initial States — Prevents FOUC */
.gsap-fade-up {{
  opacity: 0;
  transform: translateY(30px);
}}

.gsap-fade-in {{
  opacity: 0;
}}

.gsap-scale-in {{
  opacity: 0;
  transform: scale(0.9);
}}

.gsap-slide-left {{
  opacity: 0;
  transform: translateX(-40px);
}}

.gsap-slide-right {{
  opacity: 0;
  transform: translateX(40px);
}}

/* Reduced motion — show everything immediately */
@media (prefers-reduced-motion: reduce) {{
  .gsap-fade-up,
  .gsap-fade-in,
  .gsap-scale-in,
  .gsap-slide-left,
  .gsap-slide-right {{
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }}
}}
''',
}


# ─── CLI Commands ─────────────────────────────────────────────────────────────

if HAS_RICH:

    @click.group()
    @click.version_option("1.0.0", prog_name="gsap-cli")
    def cli():
        """GSAP Animated Frontend — CLI Toolkit for production-grade animations."""
        pass

    @cli.command()
    @click.option("--path", default=".", help="Project root path")
    @click.option("--framework", type=click.Choice(SUPPORTED_FRAMEWORKS), default=None)
    def init(path, framework):
        """Initialize GSAP in a project — install deps, create config, scaffold files."""
        root = find_project_root(path)
        fw = framework or detect_framework(root)

        console.print(Panel(
            f"[bold cyan]Initializing GSAP in[/] [bold white]{root.name}[/] [dim]({fw})[/]",
            border_style="cyan",
        ))

        # Step 1: Install dependencies
        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("Installing gsap + @gsap/react...", total=None)

            pkg_manager = "npm"
            if (root / "pnpm-lock.yaml").exists():
                pkg_manager = "pnpm"
            elif (root / "yarn.lock").exists():
                pkg_manager = "yarn"
            elif (root / "bun.lockb").exists():
                pkg_manager = "bun"

            install_cmd = f"{pkg_manager} {'add' if pkg_manager != 'npm' else 'install'} gsap @gsap/react"
            try:
                subprocess.run(install_cmd.split(), cwd=root, capture_output=True, timeout=120)
                progress.update(task, description="[green]✓[/] gsap + @gsap/react installed")
            except Exception as e:
                progress.update(task, description=f"[red]✗[/] Install failed: {e}")

        # Step 2: Create animation config
        config = DEFAULT_CONFIG.copy()
        config["project"]["name"] = root.name
        config["project"]["framework"] = fw

        config_path = root / ANIMATION_CONFIG_FILE
        if not config_path.exists() and HAS_YAML:
            config_path.write_text(yaml.dump(config, default_flow_style=False, sort_keys=False), encoding="utf-8")
            console.print(f"  [green]✓[/] Created {ANIMATION_CONFIG_FILE}")
        elif not HAS_YAML:
            config_path_json = root / "gsap-animations.json"
            config_path_json.write_text(json.dumps(config, indent=2), encoding="utf-8")
            console.print(f"  [green]✓[/] Created gsap-animations.json")

        # Step 3: Scaffold animation utilities
        anim_dir = root / "src" / "lib" / "animations"
        if not anim_dir.exists():
            anim_dir.mkdir(parents=True, exist_ok=True)

        files_created = []

        hooks_path = anim_dir / "use-animations.tsx"
        if not hooks_path.exists():
            hooks_path.write_text(TEMPLATES["use-animation"], encoding="utf-8")
            files_created.append(str(hooks_path.relative_to(root)))

        css_path = anim_dir / "gsap-initial-states.css"
        if not css_path.exists():
            css_path.write_text(TEMPLATES["scroll-reveal-css"], encoding="utf-8")
            files_created.append(str(css_path.relative_to(root)))

        reduced_path = anim_dir / "use-reduced-motion.tsx"
        if not reduced_path.exists():
            reduced_path.write_text(TEMPLATES["reduced-motion"], encoding="utf-8")
            files_created.append(str(reduced_path.relative_to(root)))

        if files_created:
            console.print(f"  [green]✓[/] Scaffolded animation utilities:")
            for f in files_created:
                console.print(f"    [dim]→[/] {f}")

        console.print()
        console.print(Panel(
            "[bold green]GSAP initialized![/]\n\n"
            "Next steps:\n"
            "  1. Import GSAPProvider in your layout\n"
            "  2. Import gsap-initial-states.css in globals.css\n"
            "  3. Run [bold]python gsap_cli.py scan[/] to find animation opportunities\n"
            "  4. Run [bold]python gsap_cli.py recipes[/] to browse & scaffold animations",
            border_style="green",
        ))

    @cli.command()
    @click.option("--path", default=".", help="Project root path")
    @click.option("--verbose", "-v", is_flag=True, help="Show all findings")
    def scan(path, verbose):
        """Scan project for current GSAP usage and animation opportunities."""
        root = find_project_root(path)
        fw = detect_framework(root)
        files = scan_files(root)

        console.print(Panel(
            f"[bold cyan]Scanning[/] [bold white]{root.name}[/] [dim]({fw}, {len(files)} files)[/]",
            border_style="cyan",
        ))

        all_usage = []
        all_opportunities = []

        with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), console=console) as progress:
            task = progress.add_task("Scanning files...", total=len(files))
            for f in files:
                usage = find_gsap_usage(f)
                opps = find_animation_opportunities(f)
                all_usage.extend(usage)
                all_opportunities.extend(opps)
                progress.advance(task)

        # GSAP Usage Summary
        if all_usage:
            usage_table = Table(title="GSAP Usage Found", box=box.ROUNDED, border_style="blue")
            usage_table.add_column("Type", style="cyan", min_width=20)
            usage_table.add_column("Count", style="bold white", justify="right")
            usage_table.add_column("Files", style="dim")

            usage_by_type = {}
            for u in all_usage:
                t = u["type"]
                if t not in usage_by_type:
                    usage_by_type[t] = {"count": 0, "files": set()}
                usage_by_type[t]["count"] += 1
                usage_by_type[t]["files"].add(Path(u["file"]).relative_to(root).as_posix())

            for t, data in sorted(usage_by_type.items(), key=lambda x: -x[1]["count"]):
                files_str = ", ".join(list(data["files"])[:3])
                if len(data["files"]) > 3:
                    files_str += f" +{len(data['files'])-3} more"
                usage_table.add_row(t, str(data["count"]), files_str)

            console.print(usage_table)
        else:
            console.print("[yellow]No GSAP usage found — perfect candidate for animations![/]")

        # Animation Opportunities
        if all_opportunities:
            console.print()
            opp_table = Table(title="Animation Opportunities", box=box.ROUNDED, border_style="green")
            opp_table.add_column("Section", style="bold green")
            opp_table.add_column("Suggestion", style="white")
            opp_table.add_column("Recipe", style="cyan")
            opp_table.add_column("File", style="dim")

            seen = set()
            for opp in all_opportunities:
                key = (opp["section"], opp["file"])
                if key in seen:
                    continue
                seen.add(key)
                rel = Path(opp["file"]).relative_to(root).as_posix()
                opp_table.add_row(opp["section"], opp["suggestion"], opp["recipe"], rel)

            console.print(opp_table)

        # Summary
        console.print()
        stats = {
            "Files scanned": len(files),
            "GSAP calls found": len(all_usage),
            "Unique patterns": len(set(u["type"] for u in all_usage)),
            "Animation opportunities": len(all_opportunities),
        }
        for k, v in stats.items():
            color = "green" if v > 0 else "dim"
            console.print(f"  [{color}]{k}:[/] {v}")

    @cli.command()
    @click.option("--path", default=".", help="Project root path")
    @click.option("--fix", is_flag=True, help="Show fix suggestions")
    def audit(path, fix):
        """Audit animations for performance, accessibility, and best practices."""
        root = find_project_root(path)
        files = scan_files(root)

        console.print(Panel(
            f"[bold cyan]Auditing animations in[/] [bold white]{root.name}[/]",
            border_style="cyan",
        ))

        all_issues = []
        all_usage = []

        for f in files:
            issues = find_animation_issues(f)
            usage = find_gsap_usage(f)
            all_issues.extend(issues)
            all_usage.extend(usage)

        if all_issues:
            issues_table = Table(title="Animation Issues", box=box.ROUNDED, border_style="red")
            issues_table.add_column("Sev", style="bold", min_width=6)
            issues_table.add_column("File:Line", style="cyan")
            issues_table.add_column("Issue", style="white")

            severity_colors = {"HIGH": "red", "MEDIUM": "yellow", "LOW": "dim"}

            for issue in sorted(all_issues, key=lambda x: {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[x["severity"]]):
                rel = Path(issue["file"]).relative_to(root).as_posix()
                color = severity_colors[issue["severity"]]
                issues_table.add_row(
                    f"[{color}]{issue['severity']}[/]",
                    f"{rel}:{issue['line']}",
                    issue["issue"]
                )

            console.print(issues_table)
        else:
            console.print("[bold green]✓ No animation issues found![/]")

        # Score
        total_animations = len(all_usage)
        high_issues = sum(1 for i in all_issues if i["severity"] == "HIGH")
        medium_issues = sum(1 for i in all_issues if i["severity"] == "MEDIUM")

        score = 100
        score -= high_issues * 15
        score -= medium_issues * 5
        score = max(0, score)

        color = "green" if score >= 80 else "yellow" if score >= 50 else "red"
        console.print()
        console.print(Panel(
            f"[bold {color}]Animation Health Score: {score}/100[/]\n\n"
            f"  Animations found: {total_animations}\n"
            f"  HIGH issues: [red]{high_issues}[/]\n"
            f"  MEDIUM issues: [yellow]{medium_issues}[/]\n"
            f"  LOW issues: [dim]{len(all_issues) - high_issues - medium_issues}[/]",
            border_style=color,
            title="Audit Score",
        ))

    @cli.command()
    @click.option("--path", default=".", help="Project root path")
    def report(path):
        """Generate a full animation report — coverage, score, recommendations."""
        root = find_project_root(path)
        files = scan_files(root)
        fw = detect_framework(root)

        console.print(Panel(
            f"[bold cyan]Full Animation Report[/] — [bold white]{root.name}[/]",
            border_style="cyan",
        ))

        all_usage = []
        all_issues = []
        all_opps = []
        animated_files = set()

        for f in files:
            usage = find_gsap_usage(f)
            issues = find_animation_issues(f)
            opps = find_animation_opportunities(f)
            if usage:
                animated_files.add(f)
            all_usage.extend(usage)
            all_issues.extend(issues)
            all_opps.extend(opps)

        # Coverage
        coverage = (len(animated_files) / max(len(files), 1)) * 100

        tree = Tree("[bold]Animation Coverage[/]")
        tree.add(f"Framework: [cyan]{fw}[/]")
        tree.add(f"Total files: {len(files)}")
        tree.add(f"Animated files: [green]{len(animated_files)}[/]")
        tree.add(f"Coverage: [{'green' if coverage > 30 else 'yellow'}]{coverage:.1f}%[/]")
        tree.add(f"GSAP patterns used: {len(set(u['type'] for u in all_usage))}")
        tree.add(f"Total GSAP calls: {len(all_usage)}")
        console.print(tree)

        # Features used
        console.print()
        features = set(u["type"] for u in all_usage)
        all_features = ["gsap.to", "gsap.from", "gsap.fromTo", "gsap.timeline",
                        "ScrollTrigger", "useGSAP", "gsap.matchMedia", "gsap.quickTo",
                        "Lenis", "SplitText", "Flip", "Draggable", "Observer"]

        feat_table = Table(title="Feature Checklist", box=box.ROUNDED, border_style="blue")
        feat_table.add_column("Feature", style="white")
        feat_table.add_column("Status", justify="center")
        feat_table.add_column("Usage", justify="right")

        for feat in all_features:
            used = feat in features
            count = sum(1 for u in all_usage if u["type"] == feat)
            status = "[green]✓ Used[/]" if used else "[dim]— Not used[/]"
            feat_table.add_row(feat, status, str(count) if used else "—")

        console.print(feat_table)

        # Reduced motion check
        console.print()
        has_reduced_motion = any(
            "prefers-reduced-motion" in (f.read_text(encoding="utf-8", errors="ignore"))
            for f in files[:50]
        )
        a11y_status = "[green]✓ prefers-reduced-motion detected[/]" if has_reduced_motion else "[red]✗ No prefers-reduced-motion found — CRITICAL[/]"
        console.print(f"  Accessibility: {a11y_status}")

        # Score
        high_issues = sum(1 for i in all_issues if i["severity"] == "HIGH")
        score = max(0, 100 - high_issues * 15 - sum(1 for i in all_issues if i["severity"] == "MEDIUM") * 5)
        color = "green" if score >= 80 else "yellow" if score >= 50 else "red"
        console.print(f"  Health Score: [{color}]{score}/100[/]")
        console.print(f"  Issues: [red]{high_issues} HIGH[/], [yellow]{sum(1 for i in all_issues if i['severity'] == 'MEDIUM')} MED[/], [dim]{sum(1 for i in all_issues if i['severity'] == 'LOW')} LOW[/]")
        console.print(f"  Opportunities: [green]{len(all_opps)}[/] sections could benefit from animation")

    @cli.command()
    @click.option("--path", default=".", help="Project root path")
    def config(path):
        """Generate or display animation config from interview answers."""
        root = find_project_root(path)
        config_path = root / ANIMATION_CONFIG_FILE

        if config_path.exists():
            console.print(Panel(
                f"[bold cyan]Current Animation Config[/]",
                border_style="cyan",
            ))
            content = config_path.read_text(encoding="utf-8")
            console.print(Syntax(content, "yaml", theme="monokai"))
        else:
            console.print("[yellow]No config found. Run[/] [bold]python gsap_cli.py init[/] [yellow]first.[/]")

    @cli.command()
    def recipes():
        """Browse available animation recipes and their descriptions."""
        recipe_list = [
            ("hero-text-reveal", "Hero", "Headlines slide up with stagger, subtitle fades, CTA bounces in", "Subtle"),
            ("hero-cinematic-zoom", "Hero", "Background scales 1.3→1.0, content fades over gradient overlay", "Bold"),
            ("hero-floating-shapes", "Hero", "Geometric shapes float continuously behind content", "Playful"),
            ("staggered-card-reveal", "Cards", "Cards fade-up one by one as row enters viewport", "Subtle"),
            ("card-hover-lift", "Cards", "Lift + shadow + image zoom on mouse enter", "Subtle"),
            ("card-3d-tilt", "Cards", "Cards tilt in 3D space following mouse position", "Bold"),
            ("count-up-numbers", "Stats", "Numbers animate 0→target when section visible", "Subtle"),
            ("word-by-word-reveal", "Text", "Each word fades up individually with stagger", "Elegant"),
            ("typewriter-effect", "Text", "Characters appear one by one like typing", "Playful"),
            ("pinned-scene-transitions", "Scroll", "Section pins while content transitions inside", "Cinematic"),
            ("background-color-shift", "Scroll", "Background color morphs as you scroll between sections", "Elegant"),
            ("navbar-shrink-scroll", "Nav", "Navbar shrinks + adds blur on scroll down", "Subtle"),
            ("mobile-menu-reveal", "Nav", "Menu items stagger in from right on open", "Subtle"),
            ("magnetic-button", "Effects", "Buttons subtly follow cursor on hover", "Playful"),
            ("custom-cursor", "Effects", "Replace default cursor with animated follower", "Bold"),
            ("clip-path-reveal", "Effects", "Content revealed through animated clip-path mask", "Elegant"),
            ("svg-line-draw", "Effects", "SVG strokes draw themselves on screen", "Elegant"),
            ("parallax-layers", "Scroll", "Background/mid/foreground move at different scroll speeds", "Cinematic"),
            ("horizontal-scroll", "Scroll", "Section scrolls horizontally on vertical scroll input", "Cinematic"),
            ("smooth-scroll-lenis", "Global", "Replace native scroll with buttery Lenis smooth scroll", "Subtle"),
        ]

        table = Table(title="Animation Recipe Browser", box=box.DOUBLE_EDGE, border_style="cyan")
        table.add_column("#", style="dim", justify="right", width=3)
        table.add_column("Recipe", style="bold cyan", min_width=25)
        table.add_column("Section", style="green", min_width=8)
        table.add_column("Description", style="white")
        table.add_column("Style", style="magenta", min_width=10)

        for i, (name, section, desc, style) in enumerate(recipe_list, 1):
            table.add_row(str(i), name, section, desc, style)

        console.print(table)
        console.print()
        console.print("[dim]Use these recipe names with Claude: 'Apply the hero-text-reveal recipe to my homepage'[/]")

    @cli.command()
    @click.option("--path", default=".", help="Project root path")
    def watch(path):
        """Watch project files and report animation issues in real-time."""
        try:
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
        except ImportError:
            console.print("[red]watchdog not installed. Run: pip install watchdog[/]")
            return

        root = find_project_root(path)
        console.print(Panel(
            f"[bold cyan]Watching[/] [bold white]{root.name}[/] [dim]for animation issues...[/]\n"
            f"[dim]Press Ctrl+C to stop[/]",
            border_style="cyan",
        ))

        class AnimationWatcher(FileSystemEventHandler):
            def on_modified(self, event):
                if event.is_directory:
                    return
                p = Path(event.src_path)
                if p.suffix not in (".tsx", ".ts", ".jsx", ".js"):
                    return
                if "node_modules" in p.parts:
                    return

                issues = find_animation_issues(p)
                usage = find_gsap_usage(p)

                if issues:
                    for issue in issues:
                        sev_color = {"HIGH": "red", "MEDIUM": "yellow", "LOW": "dim"}[issue["severity"]]
                        rel = Path(issue["file"]).relative_to(root).as_posix()
                        console.print(f"  [{sev_color}]{issue['severity']}[/] {rel}:{issue['line']} — {issue['issue']}")

                if usage:
                    console.print(f"  [green]✓[/] {p.relative_to(root).as_posix()} — {len(usage)} GSAP patterns detected")

        observer = Observer()
        observer.schedule(AnimationWatcher(), str(root / "src"), recursive=True)
        observer.start()

        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            console.print("\n[dim]Stopped watching.[/]")
        observer.join()


# ─── Entry Point ──────────────────────────────────────────────────────────────

def main():
    if not HAS_RICH:
        print("ERROR: 'rich' and 'click' packages required.")
        print("Install: pip install rich click pyyaml jinja2 watchdog")
        sys.exit(1)
    cli()


if __name__ == "__main__":
    main()