#!/usr/bin/env python3
"""Fetch the reviewed upstream snapshots into the ignored sources/ directory."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest" / "harnesses.json"
SOURCES = ROOT / "sources"


def run(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(args, cwd=cwd, check=True)


def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    projects = {project["slug"]: project for project in data["projects"]}
    requested = sys.argv[1:] or list(projects)
    unknown = sorted(set(requested) - set(projects))
    if unknown:
        print(f"Unknown project(s): {', '.join(unknown)}", file=sys.stderr)
        print(f"Known projects: {', '.join(projects)}", file=sys.stderr)
        return 2

    SOURCES.mkdir(exist_ok=True)
    for slug in requested:
        project = projects[slug]
        target = SOURCES / slug
        url = project["url"] + ".git"
        ref = project["reviewed_ref"]
        if not target.exists():
            run("git", "clone", "--filter=blob:none", "--no-checkout", url, str(target))
        elif not (target / ".git").exists():
            raise RuntimeError(f"Refusing to reuse non-git directory: {target}")

        origin = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], cwd=target, text=True
        ).strip()
        if origin.rstrip("/").removesuffix(".git") != url.rstrip("/").removesuffix(".git"):
            raise RuntimeError(f"Unexpected origin for {target}: {origin}")

        run("git", "fetch", "--depth=1", "origin", ref, cwd=target)
        run("git", "checkout", "--detach", ref, cwd=target)
        print(f"{slug}: {ref}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

