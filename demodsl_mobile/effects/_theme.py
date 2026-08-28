"""Shared theming helper for the mobile chrome effects."""

from __future__ import annotations

from typing import Any

from demodsl.effects.sanitize import sanitize_css_color

__all__ = ["themed_accent"]


def themed_accent(params: dict[str, Any], fallback: str) -> str:
    """The ``accent`` param if it is a real colour, else the effect's own.

    The engine fills ``accent`` from ``theme.accent`` for any effect that
    declares it, so a demo with a ``theme:`` block tints the chrome without
    touching the YAML. A rejected value keeps the fallback rather than
    silently becoming ``#888888``.
    """
    raw = str(params.get("accent") or "").strip()
    if not raw:
        return fallback
    safe = sanitize_css_color(raw)
    return safe if safe == raw else fallback
