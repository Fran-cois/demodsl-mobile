"""Shared iOS/Android-style status-bar glyphs (inline SVG), reused by
mobile_frame and mobile_home_screen so both draw the exact same chrome.
"""

from __future__ import annotations

SIGNAL_SVG = """<svg width="18" height="12" viewBox="0 0 18 12" fill="none">
  <rect x="0"  y="7" width="3" height="5" rx="0.8" fill="currentColor"/>
  <rect x="5"  y="5" width="3" height="7" rx="0.8" fill="currentColor"/>
  <rect x="10" y="3" width="3" height="9" rx="0.8" fill="currentColor"/>
  <rect x="15" y="0" width="3" height="12" rx="0.8" fill="currentColor"/>
</svg>"""

WIFI_SVG = """<svg width="16" height="12" viewBox="0 0 16 12" fill="none">
  <path d="M8 10.6a1.3 1.3 0 1 1 0-2.6 1.3 1.3 0 0 1 0 2.6Z" fill="currentColor"/>
  <path d="M4.6 6.9a4.8 4.8 0 0 1 6.8 0" stroke="currentColor" stroke-width="1.5"
    stroke-linecap="round" fill="none"/>
  <path d="M1.8 4a8.8 8.8 0 0 1 12.4 0" stroke="currentColor" stroke-width="1.5"
    stroke-linecap="round" fill="none"/>
</svg>"""

_BATTERY_SVG = """<svg width="25" height="12" viewBox="0 0 25 12" fill="none">
  <rect x="0.75" y="0.75" width="20.5" height="10.5" rx="2.8"
    stroke="currentColor" stroke-opacity="0.4" stroke-width="1"/>
  <rect x="2.2" y="2.2" width="{level}" height="7.6" rx="1.6" fill="currentColor"/>
  <rect x="22.2" y="4" width="1.6" height="4" rx="0.8" fill="currentColor" fill-opacity="0.4"/>
</svg>"""


def battery_svg(percent: float) -> str:
    """Battery glyph with a real fill level (0-100)."""
    return _BATTERY_SVG.format(level=round(20.5 * (percent / 100), 1))
