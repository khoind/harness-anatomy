#!/usr/bin/env python3
"""Fast, offline consistency checks for the atlas."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SHA = re.compile(r"^[0-9a-f]{40}$")
MARKDOWN_LINK = re.compile(r"\]\(([^)]+)\)")
REQUIRED_CARD_HEADINGS = [
    "## In one sentence",
    "## Mental model",
    "## Read these first",
    "## What to notice",
    "## Architectural lessons",
    "## Caution",
]
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".py", ".txt"}
PRIVATE_MARKER = "The" + "seus"


def main() -> int:
    manifest = json.loads((ROOT / "manifest" / "harnesses.json").read_text())
    projects = manifest["projects"]
    slugs = [project["slug"] for project in projects]
    assert len(slugs) == len(set(slugs)), "duplicate project slug"
    assert slugs == sorted(slugs), "projects must be sorted by slug"

    for project in projects:
        slug = project["slug"]
        assert SHA.fullmatch(project["reviewed_ref"]), f"bad commit for {slug}"
        assert project["url"] == f"https://github.com/{project['repository']}"
        card = ROOT / "site-docs" / "catalog" / f"{slug}.md"
        assert card.is_file(), f"missing site-docs/catalog/{slug}.md"
        card_text = card.read_text(encoding="utf-8")
        for heading in REQUIRED_CARD_HEADINGS:
            assert heading in card_text, f"{slug} lacks {heading}"
        concerns = [item["concern"] for item in project["entrypoints"]]
        assert len(concerns) == len(set(concerns)), f"duplicate concern for {slug}"
        for item in project["entrypoints"]:
            path = item["path"]
            assert path and not path.startswith("/"), f"bad path for {slug}: {path}"

    required = [
        "site-docs/index.md",
        "AGENTS.md",
        "site-docs/guide/walkthrough.md",
        "site-docs/guide/anatomy.md",
        "site-docs/guide/glossary.md",
        "site-docs/guide/comparison.md",
        "site-docs/guide/research-method.md",
        "site-docs/guide/reading-paths.md",
        "site-docs/guide/interface-lens.md",
    ]
    for path in required:
        assert (ROOT / path).is_file(), f"missing {path}"

    catalog_files = {
        path.stem for path in (ROOT / "site-docs" / "catalog").glob("*.md")
    }
    assert catalog_files == set(slugs), "catalog and manifest slugs differ"

    for document in ROOT.rglob("*.md"):
        for destination in MARKDOWN_LINK.findall(document.read_text(encoding="utf-8")):
            target = destination.split("#", 1)[0]
            if not target or target.startswith(("https://", "http://", "mailto:")):
                continue
            resolved = (document.parent / target).resolve()
            assert resolved.exists(), f"broken link in {document.relative_to(ROOT)}: {target}"

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = str(path.relative_to(ROOT))
        assert PRIVATE_MARKER.casefold() not in relative.casefold(), (
            f"private project marker in path: {relative}"
        )
        text = path.read_text(encoding="utf-8", errors="ignore")
        assert PRIVATE_MARKER.casefold() not in text.casefold(), (
            f"private project marker in {relative}"
        )

    print(
        f"OK: {len(projects)} projects, "
        f"{sum(len(p['entrypoints']) for p in projects)} source pointers, "
        f"{len(required)} required guide files"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
