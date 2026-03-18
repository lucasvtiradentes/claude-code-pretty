import json
import os
from datetime import datetime, timezone
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude" / "projects"


def _cwd_to_folder_name(cwd):
    return cwd.replace("/", "-").replace("_", "-")


def _folder_to_name(folder_name):
    stripped = folder_name.strip("-")
    return stripped if stripped else folder_name


def extract_preview(file_path):
    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if data.get("type") == "user":
                    content = data.get("message", {}).get("content", "")
                    if isinstance(content, str):
                        return content[:100]
        return ""
    except (OSError, json.JSONDecodeError):
        return ""


def _format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes}B"
    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    return f"{size_bytes / (1024 * 1024):.1f}MB"


def discover_sessions(cwd=None):
    if not PROJECTS_DIR.exists():
        return []

    if cwd is None:
        cwd = os.getcwd()

    cwd_folder = _cwd_to_folder_name(cwd)

    projects = []
    for folder in sorted(PROJECTS_DIR.iterdir()):
        if not folder.is_dir() or folder.name == "memory":
            continue

        is_current = folder.name == cwd_folder
        project_name = os.path.basename(cwd) if is_current else _folder_to_name(folder.name)

        session_files = []
        for f in folder.glob("*.jsonl"):
            stat = f.stat()
            session_files.append((f, stat))
        session_files.sort(key=lambda x: x[1].st_mtime, reverse=True)

        sessions = []
        for f, stat in session_files:
            mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
            sessions.append(
                {
                    "file": str(f),
                    "id": f.stem,
                    "date": mtime.strftime("%Y-%m-%d %H:%M"),
                    "size": _format_size(stat.st_size),
                    "size_bytes": stat.st_size,
                }
            )

        if sessions:
            projects.append(
                {
                    "path": folder.name,
                    "name": project_name,
                    "folder": folder.name,
                    "is_current": is_current,
                    "sessions": sessions,
                }
            )

    projects.sort(key=lambda p: (not p["is_current"], p["name"].lower()))
    return projects
