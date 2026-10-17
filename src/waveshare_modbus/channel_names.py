"""Persistent storage for custom channel names (relay & digital input)."""

from __future__ import annotations

import json
from pathlib import Path

_NAMES_FILE = Path(__file__).resolve().parent / "channel_names.json"

_DEFAULT: dict[str, dict[str, str]] = {"relay": {}, "input": {}}


def _load() -> dict[str, dict[str, str]]:
    if _NAMES_FILE.exists():
        try:
            data = json.loads(_NAMES_FILE.read_text(encoding="utf-8"))
            return {
                "relay": {k: str(v) for k, v in data.get("relay", {}).items()},
                "input": {k: str(v) for k, v in data.get("input", {}).items()},
            }
        except (json.JSONDecodeError, KeyError):
            return {k: dict(v) for k, v in _DEFAULT.items()}
    return {k: dict(v) for k, v in _DEFAULT.items()}


def _save(names: dict[str, dict[str, str]]) -> None:
    _NAMES_FILE.write_text(
        json.dumps(names, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def get_all() -> dict[str, dict[str, str]]:
    return _load()


def set_name(kind: str, channel: int, name: str) -> None:
    data = _load()
    section = data.setdefault(kind, {})
    name = name.strip()
    if name:
        section[str(channel)] = name
    else:
        section.pop(str(channel), None)
    _save(data)
