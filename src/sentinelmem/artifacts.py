"""Versioned, deterministic experiment artifact helpers."""

from __future__ import annotations

import importlib.metadata
import json
import platform
import subprocess
from pathlib import Path
from typing import Any


ARTIFACT_SCHEMA_VERSION = "2.1"


def runtime_versions() -> dict[str, str]:
    versions = {"python": platform.python_version()}
    for distribution in ("sentinelmem", "numpy", "faiss-cpu", "sentence-transformers", "torch"):
        try:
            versions[distribution] = importlib.metadata.version(distribution)
        except importlib.metadata.PackageNotFoundError:
            versions[distribution] = "not-installed"
    return versions


def source_revision(project_root: Path) -> dict[str, Any]:
    """Capture the HEAD commit and whether the checkout has uncommitted changes."""
    command = ["git", "-c", f"safe.directory={project_root}", "-C", str(project_root)]
    try:
        commit = subprocess.run(command + ["rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
        status = subprocess.run(command + ["status", "--porcelain"], check=True, capture_output=True, text=True).stdout
        return {"commit": commit, "working_tree_dirty": bool(status.strip())}
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "working_tree_dirty": None}


def write_artifact(path: Path, artifact: dict[str, Any]) -> None:
    """Write canonical, newline-terminated JSON via atomic replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    contents = json.dumps(artifact, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(contents, encoding="utf-8", newline="\n")
    temporary.replace(path)
