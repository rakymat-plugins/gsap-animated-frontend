"""Project structure and page-shape discovery helpers for GSAP workflows."""

from __future__ import annotations

import re
from pathlib import Path

SECTION_PATTERNS = {
    "Hero": ("hero", "banner", "masthead", "headline"),
    "Navigation": ("navbar", "topbar", "header", "nav"),
    "Feature Grid": ("feature", "card", "grid", "listing", "gallery"),
    "Stats": ("stats", "stat", "metric", "count"),
    "Testimonials": ("testimonial", "review", "quote", "social proof"),
    "Showcase": ("showcase", "gallery", "marquee", "slider"),
    "Timeline": ("timeline", "steps", "process", "journey"),
    "FAQ": ("faq", "accordion", "question"),
    "CTA": ("cta", "call-to-action", "footer", "contact"),
}


def detect_routes(root: Path, get_scan_roots):
    routes = []
    for scan_root in get_scan_roots(root):
        for suffix in ("page.tsx", "page.jsx", "page.ts", "page.js"):
            for candidate in scan_root.rglob(suffix):
                rel = candidate.relative_to(scan_root).as_posix()
                rel = rel.replace(f"/{suffix}", "").replace(suffix, "").strip("/")
                if rel == "app":
                    rel = ""
                elif rel.startswith("app/"):
                    rel = rel[4:]
                if rel == "pages":
                    rel = ""
                elif rel.startswith("pages/"):
                    rel = rel[6:]
                route = "/" + rel.strip("/")
                routes.append(route or "/")
    deduped = []
    for route in routes:
        if route not in deduped:
            deduped.append(route)
    return deduped[:40]


def infer_sections_from_content(content: str):
    sections = []
    lower = content.lower()
    for section_name, tokens in SECTION_PATTERNS.items():
        if any(token in lower for token in tokens):
            sections.append(section_name)
    return sections


def infer_component_patterns(content: str):
    patterns = []
    lower = content.lower()
    if ".map(" in content or "map(" in content:
        patterns.append("Repeated collection render")
    if "swiper" in lower or "carousel" in lower or "slider" in lower:
        patterns.append("Carousel or slider")
    if "dialog" in lower or "modal" in lower:
        patterns.append("Modal interactions")
    if "sticky" in lower:
        patterns.append("Sticky positioning")
    if "canvas" in lower or "webgl" in lower or "three" in lower:
        patterns.append("3D or canvas surface")
    if "video" in lower:
        patterns.append("Video surface")
    return patterns


def find_page_files(root: Path, page: str, scan_files, slugify, read_text):
    token = slugify(page)
    matches = []
    aliases = {token, token.replace("-", "")}
    if token in {"home", "homepage", "landing", "index"}:
        aliases.update({"home", "homepage", "landing", "index"})

    for source_file in scan_files(root):
        path_lower = source_file.as_posix().lower()
        content_lower = read_text(source_file).lower()
        if any(alias in path_lower or alias in content_lower for alias in aliases):
            matches.append(source_file)

    if not matches and token in {"home", "homepage", "landing", "index"}:
        for source_file in scan_files(root):
            path_lower = source_file.as_posix().lower()
            if re.search(r"(?:/|^)(page|index)\.(tsx|jsx|ts|js)$", path_lower):
                matches.append(source_file)

    unique = []
    for match in matches:
        if match not in unique:
            unique.append(match)
    return unique[:20]


def discover_page_structure(root: Path, page: str, scan_files, read_text, slugify):
    page_files = find_page_files(root, page, scan_files, slugify, read_text)
    sections = []
    repeated_components = []
    patterns = []
    candidate_selectors = []

    for source_file in page_files:
        content = read_text(source_file)
        sections.extend(infer_sections_from_content(content))
        patterns.extend(infer_component_patterns(content))
        repeated_components.extend(re.findall(r"<([A-Z][A-Za-z0-9]+)\b", content))
        candidate_selectors.extend(re.findall(r"(?:className|class)\s*=\s*[\"']([^\"']+)[\"']", content))

    deduped_sections = []
    for section in sections:
        if section not in deduped_sections:
            deduped_sections.append(section)

    deduped_patterns = []
    for pattern in patterns:
        if pattern not in deduped_patterns:
            deduped_patterns.append(pattern)

    repeated = []
    for component in repeated_components:
        if repeated_components.count(component) > 1 and component not in repeated:
            repeated.append(component)

    selector_samples = []
    for selector in candidate_selectors:
        cleaned = selector.strip()
        if cleaned and cleaned not in selector_samples:
            selector_samples.append(cleaned)

    return {
        "page_files": page_files,
        "sections": deduped_sections,
        "repeated_components": repeated[:10],
        "patterns": deduped_patterns[:10],
        "selector_samples": selector_samples[:12],
        "source_file": page_files[0].as_posix() if page_files else "",
    }
