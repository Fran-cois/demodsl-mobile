"""Phone chrome overlay — a bezel ring, status bar, notch/dynamic-island
(or android camera dot) and a home indicator (or android nav row).

Draws a RING (border only), never a filled panel over the recorded
content — the whole point is to frame the page, not hide it.
"""

from __future__ import annotations

from typing import Any

from demodsl.effects.js_builder import iife, inject_style
from demodsl.effects.registry import BrowserEffect
from demodsl.effects.sanitize import sanitize_css_color, sanitize_html_text, sanitize_number
from demodsl_mobile.effects._status_icons import SIGNAL_SVG, WIFI_SVG, battery_svg
from demodsl_mobile.effects._theme import themed_accent


class MobileFrameEffect(BrowserEffect):
    """Wrap the viewport in a phone bezel with a live-looking status bar.

    Params
    ------
    platform : str
        ``"ios"`` (default, Dynamic Island + home indicator) or
        ``"android"`` (camera punch-hole + a 3-button nav row).
    color : str
        Bezel colour (default ``"#0A0A0A"``).
    time_text : str
        Status-bar clock text (default ``"9:41"``).
    battery : int
        Battery level 0-100 shown in the status bar (default ``85``).
    duration : float
        Total seconds on screen (default ``8.0``).
    """

    effect_id = "mobile_frame"

    def inject(self, evaluate_js: Any, params: dict[str, Any]) -> None:
        platform = params.get("platform", "ios")
        if platform not in ("ios", "android"):
            platform = "ios"
        color = sanitize_css_color(str(params.get("color", "#0A0A0A")))
        time_text = sanitize_html_text(str(params.get("time_text", "9:41"))) or "9:41"
        accent = themed_accent(params, "#FFFFFF")
        battery = sanitize_number(params.get("battery", 85), default=85, min_val=1, max_val=100)
        duration = sanitize_number(
            params.get("duration", 8.0), default=8.0, min_val=1.0, max_val=60.0
        )
        bezel = 14
        radius = 46
        battery_glyph = battery_svg(battery)

        css = """
            @keyframes __demodsl_mf_in {
              from { opacity:0; } to { opacity:1; }
            }
            #__demodsl_mobile_frame {
              font-family: -apple-system, 'SF Pro Text', 'Segoe UI', Roboto, sans-serif;
            }
            #__demodsl_mobile_frame .__demodsl_mf_icons { color: #fff; }
        """
        evaluate_js(inject_style("__demodsl_mobile_frame_style", css))

        # iOS: a true black pill (Dynamic Island), floating just under the
        # bezel edge. Android: a small punch-hole camera dot.
        notch_html = (
            f"""<div style="position:absolute; top:{bezel + 8}px; left:50%;
                transform:translateX(-50%); width:110px; height:32px;
                background:#000; border-radius:20px; z-index:2;
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);"></div>"""
            if platform == "ios"
            else f"""<div style="position:absolute; top:{bezel + 12}px; left:50%;
                transform:translateX(-50%); width:11px; height:11px;
                border-radius:50%; background:#000;
                box-shadow: inset 0 0 0 1px rgba(255,255,255,0.08);
                z-index:2;"></div>"""
        )

        # iOS: a thin home-indicator capsule. Android: back / home / recents.
        bottom_html = (
            f"""<div style="position:absolute; bottom:{bezel + 8}px; left:50%;
                transform:translateX(-50%); width:134px; height:5px;
                border-radius:3px; background:{accent}; opacity:0.92;
                z-index:2;"></div>"""
            if platform == "ios"
            else f"""<div style="position:absolute; bottom:{bezel + 14}px; left:50%;
                transform:translateX(-50%); display:flex; align-items:center;
                gap:64px; z-index:2;">
                <div style="width:0;height:0;border-top:7px solid transparent;
                    border-bottom:7px solid transparent;
                    border-right:11px solid {accent}; opacity:0.9;"></div>
                <div style="width:13px;height:13px;border-radius:50%;
                    border:2px solid {accent}; opacity:0.9;"></div>
                <div style="width:14px;height:14px;border:2px solid {accent};
                    border-radius:3px; opacity:0.9;"></div>
              </div>"""
        )

        js = iife(f"""
            const old = document.getElementById('__demodsl_mobile_frame');
            if (old) old.remove();

            const frame = document.createElement('div');
            frame.id = '__demodsl_mobile_frame';
            frame.style.cssText = 'position:fixed;inset:0;z-index:2147483641;'
                + 'pointer-events:none;box-sizing:border-box;'
                + 'border:{bezel}px solid {color};border-radius:{radius}px;'
                + 'box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.06),'
                + ' inset 0 1px 2px rgba(255,255,255,0.12);'
                + 'animation:__demodsl_mf_in 0.3s ease-out forwards;';

            const statusBar = document.createElement('div');
            statusBar.className = '__demodsl_mf_icons';
            statusBar.style.cssText = 'position:absolute;top:{bezel}px;'
                + 'left:{bezel}px;right:{bezel}px;height:38px;'
                + 'display:flex;align-items:center;justify-content:space-between;'
                + 'padding:0 24px;font-size:15px;font-weight:600;'
                + 'text-shadow:0 1px 3px rgba(0,0,0,0.6);z-index:1;';
            statusBar.innerHTML = `
                <span>{time_text}</span>
                <span style="display:flex;gap:6px;align-items:center;">
                  {SIGNAL_SVG}{WIFI_SVG}{battery_glyph}
                </span>`;
            frame.appendChild(statusBar);

            const chrome = document.createElement('div');
            chrome.innerHTML = `{notch_html}{bottom_html}`;
            while (chrome.firstChild) frame.appendChild(chrome.firstChild);

            document.body.appendChild(frame);

            setTimeout(() => {{
                frame.style.transition = 'opacity 0.3s';
                frame.style.opacity = '0';
                setTimeout(() => frame.remove(), 320);
            }}, {int(duration * 1000)});
        """)
        evaluate_js(js)
