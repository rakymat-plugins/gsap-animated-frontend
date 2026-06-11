#!/usr/bin/env python3
"""Internal workflow helper for the GSAP skill."""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

try:
    import click
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    import yaml
except ImportError:
    print("Install dependencies first: pip install -r requirements.txt")
    sys.exit(1)

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

console = Console(force_terminal=True)
SCRIPT_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = SCRIPT_DIR / "templates"
SOURCE_EXTENSIONS = (".tsx", ".ts", ".jsx", ".js", ".vue", ".svelte")
STYLE_EXTENSIONS = (".css", ".scss", ".sass", ".less")
SKIP_DIRS = {
    "node_modules",
    ".next",
    "dist",
    ".git",
    ".pnpm",
    "__pycache__",
    ".turbo",
    "build",
    "coverage",
}
ANIMATION_CONFIG_FILE = "gsap-animations.yaml"
SECTION_PATTERNS = {
    "Hero": ("hero", "banner", "masthead"),
    "Navigation": ("navbar", "topbar", "header", "nav"),
    "Cards": ("card", "grid", "listing", "gallery"),
    "Stats": ("stats", "stat", "metric", "count"),
    "Testimonials": ("testimonial", "review", "quote"),
    "CTA": ("cta", "call-to-action", "footer", "contact"),
}
MOTION_LIB_PATTERNS = {
    "GSAP": r"gsap|ScrollTrigger|useGSAP",
    "Framer Motion": r"framer-motion|motion\.",
    "Lenis": r"\bLenis\b",
    "AOS": r"\baos\b",
}
COLOR_PATTERN = re.compile(
    r"(#(?:[0-9a-fA-F]{3,8})\b|rgba?\([^)]+\)|hsla?\([^)]+\)|oklch\([^)]+\)|oklab\([^)]+\))"
)


def find_project_root(start_path=".") -> Path:
    path = Path(start_path).resolve()
    while path != path.parent:
        if (path / "package.json").exists() or (path / ".git").exists():
            return path
        path = path.parent
    return Path(start_path).resolve()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_package_json(directory: Path):
    package_file = directory / "package.json"
    if not package_file.exists():
        return None
    try:
        return json.loads(package_file.read_text(encoding="utf-8"))
    except Exception:
        return None


def find_candidate_apps(root: Path):
    candidates = [root]
    for rel in ("apps/web", "frontend", "client", "app"):
        candidate = root / rel
        if candidate.exists():
            candidates.append(candidate)
    unique = []
    for item in candidates:
        if item not in unique:
            unique.append(item)
    return unique


def detect_framework(root: Path) -> str:
    for candidate in find_candidate_apps(root):
        package_data = load_package_json(candidate)
        if not package_data:
            continue
        deps = {
            **package_data.get("dependencies", {}),
            **package_data.get("devDependencies", {}),
        }
        if "next" in deps:
            return "next"
        if "react" in deps or "react-dom" in deps:
            return "react"
        if "vue" in deps:
            return "vue"
        if "svelte" in deps:
            return "svelte"
    return "vanilla"


def detect_package_manager(root: Path) -> str:
    if (root / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (root / "yarn.lock").exists():
        return "yarn"
    if (root / "bun.lockb").exists():
        return "bun"
    return "npm"


def collect_packages(root: Path):
    package_data = load_package_json(root) or {}
    deps = {
        **package_data.get("dependencies", {}),
        **package_data.get("devDependencies", {}),
    }
    if deps:
        return deps

    for candidate in find_candidate_apps(root):
        package_data = load_package_json(candidate)
        if package_data:
            deps = {
                **package_data.get("dependencies", {}),
                **package_data.get("devDependencies", {}),
            }
            if deps:
                return deps
    return {}


def get_scan_roots(root: Path):
    preferred = [
        root / "apps" / "web" / "src",
        root / "src",
        root / "app",
        root / "pages",
        root / "components",
        root / "packages" / "ui" / "src",
    ]
    roots = [path for path in preferred if path.exists()]
    return roots or [root]


def scan_files(root: Path, include_styles=False):
    files = []
    extensions = set(SOURCE_EXTENSIONS)
    if include_styles:
        extensions.update(STYLE_EXTENSIONS)

    def walk(directory: Path):
        try:
            for entry in directory.iterdir():
                if entry.is_dir():
                    if entry.name not in SKIP_DIRS:
                        walk(entry)
                elif entry.suffix in extensions:
                    files.append(entry)
        except (PermissionError, OSError):
            return

    for scan_root in get_scan_roots(root):
        walk(scan_root)
    return sorted(set(files))


def load_template(name: str, replacements: dict[str, str] | None = None) -> str:
    content = (TEMPLATES_DIR / name).read_text(encoding="utf-8")
    for key, value in (replacements or {}).items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "page"


def ensure_workspace(root: Path, page: str, project_name: str | None = None):
    project_name = project_name or root.name
    page_slug = slugify(page)
    gsap_dir = root / ".gsap"
    pages_dir = gsap_dir / "pages"
    gsap_dir.mkdir(exist_ok=True)
    pages_dir.mkdir(exist_ok=True)

    created = []
    artifacts = {
        gsap_dir / "animation-spec.md": load_template("animation-spec.md", {"PROJECT_NAME": project_name}),
        gsap_dir / "animation-plan.md": load_template("animation-plan.md", {"PROJECT_NAME": project_name}),
        gsap_dir / "audit-report.md": load_template("audit-report.md", {"PROJECT_NAME": project_name}),
        pages_dir / f"{page_slug}.animation.md": load_template("page-animation.md", {"PAGE_NAME": page_slug}),
    }
    for path, content in artifacts.items():
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(path)

    return created


def replace_or_append_section(content: str, heading: str, lines: list[str]) -> str:
    block = f"## {heading}\n\n" + "\n".join(lines).rstrip() + "\n"
    pattern = rf"\n## {re.escape(heading)}\n.*?(?=\n## |\Z)"
    if re.search(pattern, content, flags=re.S):
        return re.sub(pattern, "\n" + block, content, flags=re.S)
    content = content.rstrip() + "\n\n" + block
    return content


def set_field(content: str, label: str, value: str) -> str:
    lines = content.splitlines()
    updated = False
    target_prefix = f"- {label}:"
    for index, line in enumerate(lines):
        if line.startswith(target_prefix):
            lines[index] = f"{target_prefix} {value}"
            updated = True
            break
    if not updated:
        lines.append(f"- {label}: {value}")
    return "\n".join(lines) + ("\n" if content.endswith("\n") or not lines[-1].endswith("\n") else "")


def detect_routes(root: Path):
    routes = []
    for scan_root in get_scan_roots(root):
        for candidate in scan_root.rglob("page.tsx"):
            rel = candidate.relative_to(scan_root).as_posix()
            route = "/" + rel.replace("/page.tsx", "").replace("page.tsx", "").strip("/")
            routes.append(route or "/")
        for candidate in scan_root.rglob("page.jsx"):
            rel = candidate.relative_to(scan_root).as_posix()
            route = "/" + rel.replace("/page.jsx", "").replace("page.jsx", "").strip("/")
            routes.append(route or "/")
    deduped = []
    for route in routes:
        if route not in deduped:
            deduped.append(route)
    return deduped[:30]


def infer_sections_from_content(content: str):
    found = []
    lower = content.lower()
    for section_name, tokens in SECTION_PATTERNS.items():
        if any(token in lower for token in tokens):
            found.append(section_name)
    return found


def find_page_files(root: Path, page: str):
    token = slugify(page)
    matches = []
    source_files = scan_files(root)
    for source_file in source_files:
        path_lower = source_file.as_posix().lower()
        content_lower = read_text(source_file).lower()
        if token in path_lower or token.replace("-", "") in content_lower:
            matches.append(source_file)
    if not matches and token in {"home", "homepage", "landing", "index"}:
        for source_file in source_files:
            path_lower = source_file.as_posix().lower()
            if path_lower.endswith("/page.tsx") or path_lower.endswith("/page.jsx") or path_lower.endswith("/index.tsx"):
                matches.append(source_file)
    return matches[:20]


def discover_page_structure(root: Path, page: str):
    page_files = find_page_files(root, page)
    sections = []
    repeated_components = []
    if not page_files:
        return {
            "page_files": [],
            "sections": [],
            "repeated_components": [],
            "source_file": "",
        }

    for source_file in page_files:
        content = read_text(source_file)
        sections.extend(infer_sections_from_content(content))
        if ".map(" in content or "map(" in content:
            repeated_components.append(source_file.name)

    deduped_sections = []
    for section in sections:
        if section not in deduped_sections:
            deduped_sections.append(section)

    return {
        "page_files": page_files,
        "sections": deduped_sections,
        "repeated_components": repeated_components[:8],
        "source_file": page_files[0].as_posix() if page_files else "",
    }


def discover_motion_stack(root: Path):
    files = scan_files(root)
    counts = Counter()
    for source_file in files:
        content = read_text(source_file)
        for name, pattern in MOTION_LIB_PATTERNS.items():
            if re.search(pattern, content, flags=re.I):
                counts[name] += 1
    return counts


def extract_design_tokens(root: Path):
    colors = Counter()
    fonts = Counter()
    css_vars = Counter()
    tone_hints = Counter()

    candidate_files = []
    for path in [
        root / "tailwind.config.ts",
        root / "tailwind.config.js",
        root / "apps" / "web" / "tailwind.config.ts",
        root / "apps" / "web" / "tailwind.config.js",
        root / "src" / "app" / "globals.css",
        root / "apps" / "web" / "src" / "app" / "globals.css",
    ]:
        if path.exists():
            candidate_files.append(path)

    candidate_files.extend(scan_files(root, include_styles=True)[:40])

    for source_file in candidate_files:
        content = read_text(source_file)
        for color in COLOR_PATTERN.findall(content):
            colors[color] += 1
        for font_match in re.findall(r"font-family\s*:\s*([^;]+);", content, flags=re.I):
            fonts[font_match.strip()] += 1
        for var_match in re.findall(r"(--[A-Za-z0-9-_]+)\s*:", content):
            css_vars[var_match] += 1
        for hint in ("luxury", "premium", "playful", "editorial", "booking", "dashboard", "minimal"):
            if hint in content.lower():
                tone_hints[hint] += 1

    return {
        "colors": [item for item, _ in colors.most_common(8)],
        "fonts": [item for item, _ in fonts.most_common(4)],
        "css_vars": [item for item, _ in css_vars.most_common(8)],
        "tone_hints": [item for item, _ in tone_hints.most_common(6)],
    }


def discover_project(root: Path, page: str):
    packages = collect_packages(root)
    page_structure = discover_page_structure(root, page)
    motion_stack = discover_motion_stack(root)
    design_tokens = extract_design_tokens(root)
    routes = detect_routes(root)

    return {
        "root": root,
        "framework": detect_framework(root),
        "package_manager": detect_package_manager(root),
        "packages": packages,
        "routes": routes,
        "page_structure": page_structure,
        "motion_stack": motion_stack,
        "design_tokens": design_tokens,
    }


def infer_questions(discovery: dict, mode: str):
    questions = []
    page_structure = discovery["page_structure"]
    motion_stack = discovery["motion_stack"]
    design_tokens = discovery["design_tokens"]
    packages = discovery["packages"]

    if not page_structure["sections"]:
        questions.append("Which sections on this page matter most for motion hierarchy?")
    if "GSAP" not in motion_stack and "gsap" not in packages:
        questions.append("Should this workflow install GSAP in the project, or is motion planning only needed for now?")
    if "Lenis" not in motion_stack and "lenis" not in packages:
        questions.append("Do you want smooth scrolling like Lenis, or should we stay with native scroll?")
    if not design_tokens["colors"]:
        questions.append("What brand colors or visual references should motion respect?")
    if "Cards" in page_structure["sections"]:
        questions.append("Should repeated cards all share one reveal pattern, or should featured cards behave differently?")
    if mode == "gsap-refactor" and "GSAP" not in motion_stack:
        questions.append("This page does not appear to use GSAP yet. Should the refactor introduce GSAP or only improve existing native/CSS motion?")
    if mode == "gsap-refactor" and not any(key in motion_stack for key in ("GSAP", "Framer Motion")):
        questions.append("What current motion feels wrong: too static, too noisy, too slow, or inconsistent?")

    deduped = []
    for item in questions:
        if item not in deduped:
            deduped.append(item)
    return deduped[:6]


def infer_recommendations(discovery: dict, mode: str):
    page_structure = discovery["page_structure"]
    recommendations = []
    if "Hero" in page_structure["sections"]:
        recommendations.append("Use a staged hero reveal for above-the-fold hierarchy.")
    if "Cards" in page_structure["sections"]:
        recommendations.append("Use batched stagger reveals for repeated cards or grids.")
    if "Stats" in page_structure["sections"]:
        recommendations.append("Use count-up motion only when the section first becomes visible.")
    if "Navigation" in page_structure["sections"]:
        recommendations.append("Consider a subtle shrink-on-scroll or backdrop polish for navigation.")
    if mode == "gsap-refactor":
        recommendations.append("Preserve good motion and remove noisy, duplicated, or mobile-heavy effects first.")
        recommendations.append("Add reduced-motion handling before adding more spectacle.")
    else:
        recommendations.append("Define mobile simplifications and reduced-motion fallbacks before implementation.")

    deduped = []
    for item in recommendations:
        if item not in deduped:
            deduped.append(item)
    return deduped[:8]


def package_summary(packages: dict):
    interesting = []
    for name in [
        "gsap",
        "@gsap/react",
        "next",
        "react",
        "tailwindcss",
        "framer-motion",
        "lenis",
        "typescript",
    ]:
        if name in packages:
            interesting.append(f"{name}@{packages[name]}")
    return interesting


def update_animation_spec(root: Path, page: str, discovery: dict, questions: list[str]):
    spec_path = root / ".gsap" / "animation-spec.md"
    content = read_text(spec_path)

    framework_line = f"- Framework: {discovery['framework']}"
    package_manager_line = f"- Package Manager: {discovery['package_manager']}"
    package_lines = package_summary(discovery["packages"]) or ["No notable frontend packages detected."]
    color_lines = discovery["design_tokens"]["colors"] or ["No color tokens detected yet."]
    font_lines = discovery["design_tokens"]["fonts"] or ["No font tokens detected yet."]

    content = replace_or_append_section(
        content,
        "Discovery Snapshot",
        [
            framework_line,
            package_manager_line,
            "- Packages:",
            *[f"  - {item}" for item in package_lines],
            f"- Routes Detected: {', '.join(discovery['routes'][:10]) if discovery['routes'] else 'None detected'}",
        ],
    )
    content = replace_or_append_section(
        content,
        "Brand And Design Signals",
        [
            "- Colors:",
            *[f"  - {item}" for item in color_lines],
            "- Fonts:",
            *[f"  - {item}" for item in font_lines],
            "- CSS Variables:",
            *[f"  - {item}" for item in (discovery['design_tokens']['css_vars'] or ['None detected'])],
        ],
    )
    content = replace_or_append_section(
        content,
        "Questions To Resolve",
        [f"- {question}" for question in questions] or ["- No blocking discovery questions right now."],
    )
    write_text(spec_path, content)


def update_page_artifact(root: Path, page: str, discovery: dict, mode: str, questions: list[str], recommendations: list[str]):
    page_slug = slugify(page)
    page_path = root / ".gsap" / "pages" / f"{page_slug}.animation.md"
    content = read_text(page_path)
    page_structure = discovery["page_structure"]

    content = set_field(content, "Page Route", page if page.startswith("/") else f"/{page_slug}")
    content = set_field(content, "Source File", page_structure["source_file"] or "Manual mapping needed")
    content = set_field(content, "Page Status", "Needs implementation plan" if mode == "gsap-new" else "Refactor in progress")
    content = replace_or_append_section(
        content,
        "Discovery Snapshot",
        [
            f"- Matched Files: {', '.join(file.name for file in page_structure['page_files'][:8]) if page_structure['page_files'] else 'No direct matches found'}",
            f"- Sections Detected: {', '.join(page_structure['sections']) if page_structure['sections'] else 'No obvious section types detected'}",
            f"- Repeated Components: {', '.join(page_structure['repeated_components']) if page_structure['repeated_components'] else 'None detected'}",
        ],
    )
    content = replace_or_append_section(
        content,
        "Resume State",
        [
            "- Next Agent Action: Read discovery sections, resolve any open questions, then implement or refactor.",
            f"- Blocking Questions: {' | '.join(questions) if questions else 'None from auto-discovery'}",
        ],
    )
    content = replace_or_append_section(
        content,
        "Recommended Motion Directions",
        [f"- {item}" for item in recommendations] or ["- Manual motion direction needed."],
    )
    write_text(page_path, content)


def update_plan_artifact(root: Path, page: str, discovery: dict, mode: str, questions: list[str], recommendations: list[str]):
    plan_path = root / ".gsap" / "animation-plan.md"
    content = read_text(plan_path)
    page_slug = slugify(page)
    page_structure = discovery["page_structure"]

    content = set_field(content, "Current Mode", mode)
    content = set_field(content, "Resume State", "Discovery complete")
    content = replace_or_append_section(
        content,
        f"Workflow Snapshot - {page_slug}",
        [
            f"- Mode: {mode}",
            f"- Framework: {discovery['framework']}",
            f"- Package Manager: {discovery['package_manager']}",
            f"- Existing Motion Stack: {', '.join(discovery['motion_stack'].keys()) if discovery['motion_stack'] else 'No motion libraries detected'}",
            f"- Suggested Next Command: {'Implement against .gsap plan and update page status fields.'}",
        ],
    )
    content = replace_or_append_section(
        content,
        f"Implementation Plan - {page_slug}",
        [
            "- Inspect matched source files before editing.",
            "- Confirm any unresolved questions from discovery.",
            "- Implement above-the-fold motion first.",
            "- Add grid/card/stat motion only after mobile and reduced-motion rules are clear.",
            "- Update .gsap page artifact after each major section is done.",
        ],
    )
    content = replace_or_append_section(
        content,
        f"Detected Project Signals - {page_slug}",
        [
            f"- Matched Files: {', '.join(file.name for file in page_structure['page_files'][:8]) if page_structure['page_files'] else 'No direct file matches'}",
            f"- Sections: {', '.join(page_structure['sections']) if page_structure['sections'] else 'Not inferred'}",
            "- Recommendations:",
            *[f"  - {item}" for item in recommendations],
            "- Open Questions:",
            *[f"  - {item}" for item in (questions or ['None from auto-discovery'])],
        ],
    )
    write_text(plan_path, content)


def update_audit_artifact(root: Path, page: str, discovery: dict, questions: list[str], recommendations: list[str]):
    audit_path = root / ".gsap" / "audit-report.md"
    content = read_text(audit_path)
    page_slug = slugify(page)
    motion_stack = discovery["motion_stack"]
    page_structure = discovery["page_structure"]
    findings = []

    if "GSAP" not in motion_stack:
        findings.append("GSAP does not appear to be implemented yet on the matched files.")
    if "Hero" in page_structure["sections"] and "Cards" in page_structure["sections"]:
        findings.append("Hero and repeated-card motion should share a clear hierarchy rather than equal visual weight.")
    if not discovery["design_tokens"]["colors"]:
        findings.append("No obvious brand color tokens were detected automatically; motion styling may need manual brand direction.")
    if not findings:
        findings.append("Existing page signals were detected; proceed with a careful refactor plan rather than a full reset.")

    content = replace_or_append_section(
        content,
        f"Refactor Snapshot - {page_slug}",
        [
            f"- Existing Motion Stack: {', '.join(motion_stack.keys()) if motion_stack else 'None detected'}",
            f"- Matched Files: {', '.join(file.name for file in page_structure['page_files'][:8]) if page_structure['page_files'] else 'No direct matches'}",
            "- Findings:",
            *[f"  - {item}" for item in findings],
            "- Recommended Improvements:",
            *[f"  - {item}" for item in recommendations],
            "- Open Questions:",
            *[f"  - {item}" for item in (questions or ['None from auto-discovery'])],
        ],
    )
    write_text(audit_path, content)


def render_summary_table(discovery: dict, page: str, questions: list[str]):
    table = Table(title=f"GSAP Discovery - {page}")
    table.add_column("Signal", style="cyan")
    table.add_column("Value", style="white")
    table.add_row("Framework", discovery["framework"])
    table.add_row("Package manager", discovery["package_manager"])
    table.add_row("Routes detected", str(len(discovery["routes"])))
    table.add_row(
        "Matched files",
        ", ".join(file.name for file in discovery["page_structure"]["page_files"][:5]) or "None",
    )
    table.add_row(
        "Sections",
        ", ".join(discovery["page_structure"]["sections"]) or "Not inferred",
    )
    table.add_row(
        "Motion stack",
        ", ".join(discovery["motion_stack"].keys()) if discovery["motion_stack"] else "None detected",
    )
    table.add_row(
        "Questions",
        str(len(questions)),
    )
    return table


@click.group()
def cli():
    """Internal GSAP workflow helper."""


@cli.command(name="gsap-new")
@click.option("--path", default=".", help="Project root path")
@click.option("--page", required=True, help="Page or section name")
@click.option("--project-name", default=None, help="Display name written into templates")
def gsap_new(path, page, project_name):
    """Bootstrap and orchestrate new-page workflow state."""
    root = find_project_root(path)
    created = ensure_workspace(root, page, project_name)
    discovery = discover_project(root, page)
    questions = infer_questions(discovery, "gsap-new")
    recommendations = infer_recommendations(discovery, "gsap-new")

    update_animation_spec(root, page, discovery, questions)
    update_page_artifact(root, page, discovery, "gsap-new", questions, recommendations)
    update_plan_artifact(root, page, discovery, "gsap-new", questions, recommendations)

    console.print(
        Panel(
            f"[bold cyan]gsap-new[/] prepared workflow state for [bold white]{page}[/]\n"
            f"[dim]framework: {discovery['framework']} | package manager: {discovery['package_manager']}[/]",
            border_style="cyan",
        )
    )
    if created:
        for created_path in created:
            console.print(f"[green]Created[/] {created_path}")
    console.print(render_summary_table(discovery, page, questions))


@cli.command(name="gsap-refactor")
@click.option("--path", default=".", help="Project root path")
@click.option("--page", required=True, help="Page or component name")
@click.option("--project-name", default=None, help="Display name written into templates")
def gsap_refactor(path, page, project_name):
    """Bootstrap and orchestrate refactor workflow state."""
    root = find_project_root(path)
    created = ensure_workspace(root, page, project_name)
    discovery = discover_project(root, page)
    questions = infer_questions(discovery, "gsap-refactor")
    recommendations = infer_recommendations(discovery, "gsap-refactor")

    update_animation_spec(root, page, discovery, questions)
    update_page_artifact(root, page, discovery, "gsap-refactor", questions, recommendations)
    update_plan_artifact(root, page, discovery, "gsap-refactor", questions, recommendations)
    update_audit_artifact(root, page, discovery, questions, recommendations)

    console.print(
        Panel(
            f"[bold cyan]gsap-refactor[/] prepared refactor state for [bold white]{page}[/]\n"
            f"[dim]framework: {discovery['framework']} | package manager: {discovery['package_manager']}[/]",
            border_style="cyan",
        )
    )
    if created:
        for created_path in created:
            console.print(f"[green]Created[/] {created_path}")
    console.print(render_summary_table(discovery, page, questions))


@cli.command(name="_status", hidden=True)
@click.option("--path", default=".", help="Project root path")
def internal_status(path):
    root = find_project_root(path)
    gsap_dir = root / ".gsap"
    table = Table(title=".gsap Status")
    table.add_column("Artifact")
    table.add_column("Present")
    for artifact in [
        "animation-spec.md",
        "animation-plan.md",
        "audit-report.md",
        "pages",
    ]:
        target = gsap_dir / artifact
        table.add_row(artifact, "yes" if target.exists() else "no")
    console.print(table)


@cli.command(name="_config", hidden=True)
@click.option("--path", default=".", help="Project root path")
def internal_config(path):
    root = find_project_root(path)
    config_path = root / ANIMATION_CONFIG_FILE
    if not config_path.exists():
        console.print("No gsap config found.")
        return
    console.print(config_path.read_text(encoding="utf-8"))


@cli.command(name="_init", hidden=True)
@click.option("--path", default=".", help="Project root path")
def internal_init(path):
    root = find_project_root(path)
    config_path = root / ANIMATION_CONFIG_FILE
    if not config_path.exists():
        config = {
            "version": "3.1",
            "project": {
                "name": root.name,
                "framework": detect_framework(root),
                "package_manager": detect_package_manager(root),
            },
            "performance": {"reduced_motion": True, "device_priority": "mobile-first"},
        }
        config_path.write_text(yaml.dump(config, default_flow_style=False, sort_keys=False), encoding="utf-8")
    console.print(f"Initialized {config_path}")


def main():
    cli()


if __name__ == "__main__":
    main()
