#!/usr/bin/env python3
"""Internal workflow helper for the GSAP skill."""

from __future__ import annotations

import json
import os
import re
import sys
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
SKIP_DIRS = {"node_modules", ".next", "dist", ".git", ".pnpm", "__pycache__", ".turbo", "build", "coverage"}
ANIMATION_CONFIG_FILE = "gsap-animations.yaml"


def find_project_root(start_path=".") -> Path:
    path = Path(start_path).resolve()
    while path != path.parent:
        if (path / "package.json").exists() or (path / ".git").exists():
            return path
        path = path.parent
    return Path(start_path).resolve()


def detect_framework(root: Path) -> str:
    candidates = [root, root / "apps" / "web", root / "frontend", root / "client"]
    for candidate in candidates:
        package_file = candidate / "package.json"
        if not package_file.exists():
            continue
        try:
            data = json.loads(package_file.read_text(encoding="utf-8"))
        except Exception:
            continue
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        if "next" in deps:
            return "next"
        if "react" in deps or "react-dom" in deps:
            return "react"
        if "vue" in deps:
            return "vue"
        if "svelte" in deps:
            return "svelte"
    return "vanilla"


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


def scan_files(root: Path):
    files = []

    def walk(directory: Path):
        try:
            for entry in directory.iterdir():
                if entry.is_dir():
                    if entry.name not in SKIP_DIRS:
                        walk(entry)
                elif entry.suffix in SOURCE_EXTENSIONS:
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


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def set_field(content: str, label: str, value: str) -> str:
    pattern = rf"(^- {re.escape(label)}:\s*).*$"
    if re.search(pattern, content, flags=re.MULTILINE):
        return re.sub(pattern, rf"\1{value}", content, flags=re.MULTILINE)
    return content + f"\n- {label}: {value}\n"


def append_section(path: Path, heading: str, lines: list[str]):
    content = read_text(path).rstrip() + "\n\n"
    content += f"## {heading}\n\n"
    content += "\n".join(lines).rstrip() + "\n"
    write_text(path, content)


def summarize_usage(content: str):
    return {
        "gsap_calls": len(re.findall(r"gsap\.(to|from|fromTo|timeline|set)\s*\(", content)),
        "scroll_trigger": "ScrollTrigger" in content,
        "use_gsap": "useGSAP" in content,
        "reduced_motion": "prefers-reduced-motion" in content or "matchMedia" in content,
        "lenis": "Lenis" in content,
    }


def scan_opportunities(root: Path, page: str):
    opportunities = []
    page_token = slugify(page).replace("-", "")
    for source_file in scan_files(root):
        content = read_text(source_file)
        lower = content.lower()
        if page_token and page_token not in source_file.as_posix().lower() and page_token not in lower:
            continue
        if any(token in lower for token in ("hero", "banner")) and "gsap" not in lower:
            opportunities.append("Hero can use a staged text reveal.")
        if ("map(" in content or ".map(" in content) and any(token in lower for token in ("card", "grid", "listing")):
            opportunities.append("Repeated cards are a good fit for batched stagger reveals.")
        if any(token in lower for token in ("stat", "metric", "count")):
            opportunities.append("Stats can use count-up motion if they are visible on entry.")
        if any(token in lower for token in ("navbar", "header", "topbar")) and "scroll" not in lower:
            opportunities.append("Navigation may benefit from a subtle shrink-on-scroll state.")
    deduped = []
    for item in opportunities:
        if item not in deduped:
            deduped.append(item)
    return deduped[:8]


def find_page_files(root: Path, page: str):
    token = slugify(page)
    matches = []
    for source_file in scan_files(root):
        path_lower = source_file.as_posix().lower()
        if token in path_lower:
            matches.append(source_file)
    return matches[:12]


def write_new_workflow_state(root: Path, page: str):
    page_slug = slugify(page)
    spec_path = root / ".gsap" / "animation-spec.md"
    plan_path = root / ".gsap" / "animation-plan.md"
    page_path = root / ".gsap" / "pages" / f"{page_slug}.animation.md"

    page_content = read_text(page_path)
    page_content = set_field(page_content, "Status", "Needs interview or artifact completion")
    write_text(page_path, page_content)

    append_section(
        plan_path,
        f"Workflow Snapshot - {page_slug}",
        [
            f"- Mode: gsap-new",
            f"- Page: {page_slug}",
            "- Resume State: Bootstrap complete",
            "- Next Agent Action: Read artifacts, ask only missing questions, then implement.",
        ],
    )

    if "Brand references:" in read_text(spec_path):
        return


def write_refactor_workflow_state(root: Path, page: str):
    page_slug = slugify(page)
    plan_path = root / ".gsap" / "animation-plan.md"
    audit_path = root / ".gsap" / "audit-report.md"
    page_path = root / ".gsap" / "pages" / f"{page_slug}.animation.md"
    page_files = find_page_files(root, page)

    summaries = []
    for source_file in page_files[:6]:
        usage = summarize_usage(read_text(source_file))
        summaries.append(
            f"- {source_file.name}: gsap_calls={usage['gsap_calls']}, "
            f"scrollTrigger={usage['scroll_trigger']}, useGSAP={usage['use_gsap']}, "
            f"reducedMotion={usage['reduced_motion']}"
        )

    if not summaries:
        summaries.append("- No obvious page-specific source files were matched. Manual inspection needed.")

    append_section(
        audit_path,
        f"Refactor Snapshot - {page_slug}",
        [
            f"- Mode: gsap-refactor",
            f"- Page: {page_slug}",
            "- Current code audit:",
            *summaries,
        ],
    )

    opportunities = scan_opportunities(root, page)
    append_section(
        plan_path,
        f"Refactor Plan - {page_slug}",
        [
            "- Preserve good motion and remove noise.",
            "- Add reduced-motion handling where missing.",
            "- Simplify mobile-heavy patterns before adding more effects.",
            "- Candidate improvements:",
            *[f"  {item}" for item in (opportunities or ['Manual review required.'])],
        ],
    )

    page_content = read_text(page_path)
    page_content = set_field(page_content, "Status", "Refactor in progress")
    write_text(page_path, page_content)


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
    write_new_workflow_state(root, page)

    console.print(
        Panel(
            f"[bold cyan]gsap-new[/] prepared workflow state for [bold white]{page}[/]\n"
            f"[dim]framework: {detect_framework(root)}[/]",
            border_style="cyan",
        )
    )
    if created:
        for path in created:
            console.print(f"[green]Created[/] {path}")
    console.print(f"[green]Updated[/] {root / '.gsap' / 'animation-plan.md'}")
    console.print(f"[green]Updated[/] {root / '.gsap' / 'pages' / f'{slugify(page)}.animation.md'}")


@cli.command(name="gsap-refactor")
@click.option("--path", default=".", help="Project root path")
@click.option("--page", required=True, help="Page or component name")
@click.option("--project-name", default=None, help="Display name written into templates")
def gsap_refactor(path, page, project_name):
    """Bootstrap and orchestrate refactor workflow state."""
    root = find_project_root(path)
    created = ensure_workspace(root, page, project_name)
    write_refactor_workflow_state(root, page)

    console.print(
        Panel(
            f"[bold cyan]gsap-refactor[/] prepared refactor state for [bold white]{page}[/]\n"
            f"[dim]framework: {detect_framework(root)}[/]",
            border_style="cyan",
        )
    )
    if created:
        for path in created:
            console.print(f"[green]Created[/] {path}")
    console.print(f"[green]Updated[/] {root / '.gsap' / 'audit-report.md'}")
    console.print(f"[green]Updated[/] {root / '.gsap' / 'animation-plan.md'}")


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
            "version": "3.0",
            "project": {"name": root.name, "framework": detect_framework(root)},
            "performance": {"reduced_motion": True, "device_priority": "mobile-first"},
        }
        config_path.write_text(yaml.dump(config, default_flow_style=False, sort_keys=False), encoding="utf-8")
    console.print(f"Initialized {config_path}")


def main():
    cli()


if __name__ == "__main__":
    main()
