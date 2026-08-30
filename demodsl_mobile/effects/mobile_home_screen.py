"""Home-screen overlay — a fullscreen app-icon grid with a dock, for the
"and it's on mobile too" beat.
"""

from __future__ import annotations

from typing import Any

from demodsl.effects.js_builder import iife, inject_style
from demodsl.effects.registry import BrowserEffect
from demodsl.effects.sanitize import sanitize_css_color, sanitize_html_text, sanitize_number
from demodsl_mobile.effects._status_icons import SIGNAL_SVG, WIFI_SVG, battery_svg
from demodsl_mobile.effects._theme import themed_accent

_DEFAULT_APPS = [
    {"name": "Mail", "letter": "M", "color": "#4E8FE0"},
    {"name": "Photos", "letter": "P", "color": "#E0733D"},
    {"name": "Notes", "letter": "N", "color": "#E8C34A"},
    {"name": "Calendar", "letter": "C", "color": "#D9463C"},
    {"name": "Settings", "letter": "S", "color": "#8A8D91"},
    {"name": "Maps", "letter": "M", "color": "#5FAE5B"},
    {"name": "Music", "letter": "M", "color": "#E0507A"},
    {"name": "Camera", "letter": "C", "color": "#3C3C3E"},
]

_DEFAULT_DOCK = [
    {"name": "Phone", "letter": "P", "color": "#5FAE5B"},
    {"name": "Safari", "letter": "S", "color": "#4E8FE0"},
    {"name": "Messages", "letter": "M", "color": "#5FAE5B"},
    {"name": "App", "letter": "A", "color": "#7C6FE8"},
]


class MobileHomeScreenEffect(BrowserEffect):
    """Full-screen phone home-screen simulator (app grid + dock).

    Params
    ------
    apps : list[dict]
        ``{"name": str, "letter": str, "color": str}`` entries for the
        main grid (default 8 common apps).
    dock : list[dict]
        Same shape, rendered in the bottom dock (default 4 apps).
    time_text : str
        Status-bar clock / widget text (default ``"9:41"``).
    date_text : str
        Date widget text (default ``"Monday, 12 October"``).
    battery : int
        Battery level 0-100 shown in the status bar (default ``85``).
    theme : str
        ``"aurora"`` (default, animated gradient wallpaper) or ``"solid"``.
    duration : float
        Total seconds on screen (default ``6.0``).
    """

    effect_id = "mobile_home_screen"

    def inject(self, evaluate_js: Any, params: dict[str, Any]) -> None:
        raw_apps = params.get("apps") or _DEFAULT_APPS
        apps = self._clean_apps(raw_apps, _DEFAULT_APPS)
        raw_dock = params.get("dock") or _DEFAULT_DOCK
        dock = self._clean_apps(raw_dock, _DEFAULT_DOCK)
        time_text = sanitize_html_text(str(params.get("time_text", "9:41"))) or "9:41"
        date_text = sanitize_html_text(str(params.get("date_text", "Monday, 12 October")))
        theme = params.get("theme", "aurora")
        if theme not in ("aurora", "solid"):
            theme = "aurora"
        accent = themed_accent(params, "#7C6FE8")
        battery = sanitize_number(params.get("battery", 85), default=85, min_val=1, max_val=100)
        battery_glyph = battery_svg(battery)
        duration = sanitize_number(
            params.get("duration", 6.0), default=6.0, min_val=1.0, max_val=60.0
        )

        wallpaper = (
            f"linear-gradient(160deg, {accent} 0%, #1a1b3a 55%, #0a0a12 100%)"
            if theme == "aurora"
            else "#121214"
        )

        css = """
            @keyframes __demodsl_home_in {
              from { opacity:0; } to { opacity:1; }
            }
        """
        evaluate_js(inject_style("__demodsl_home_style", css))

        app_cells = "".join(
            f"""<div style="display:flex;flex-direction:column;align-items:center;gap:6px;">
              <div style="width:56px;height:56px;border-radius:14px;
                  background:{a["color"]};color:#fff;display:flex;
                  align-items:center;justify-content:center;font-size:22px;
                  font-weight:700;box-shadow:0 4px 10px rgba(0,0,0,0.3);">
                {a["letter"]}
              </div>
              <div style="color:#fff;font-size:12px;text-shadow:0 1px 3px rgba(0,0,0,0.6);">
                {a["name"]}
              </div>
            </div>"""
            for a in apps
        )

        dock_cells = "".join(
            f"""<div style="width:56px;height:56px;border-radius:14px;
                background:{a["color"]};color:#fff;display:flex;
                align-items:center;justify-content:center;font-size:22px;
                font-weight:700;">{a["letter"]}</div>"""
            for a in dock
        )

        js = iife(f"""
            const old = document.getElementById('__demodsl_mobile_home');
            if (old) old.remove();

            const win = document.createElement('div');
            win.id = '__demodsl_mobile_home';
            win.style.cssText = 'position:fixed;inset:0;z-index:2147483641;'
                + 'background:{wallpaper};'
                + 'display:grid;grid-template-rows:auto auto 1fr auto;'
                + 'animation:__demodsl_home_in 0.3s ease-out forwards;';

            const statusBar = document.createElement('div');
            statusBar.style.cssText = 'padding:18px 28px 0;display:flex;'
                + 'align-items:center;justify-content:space-between;color:#fff;'
                + 'font-family:-apple-system,"SF Pro Text","Segoe UI",Roboto,sans-serif;'
                + 'font-size:15px;font-weight:600;'
                + 'text-shadow:0 1px 3px rgba(0,0,0,0.5);';
            statusBar.innerHTML = `
                <span>{time_text}</span>
                <span style="display:flex;gap:6px;align-items:center;">
                  {SIGNAL_SVG}{WIFI_SVG}{battery_glyph}
                </span>`;
            win.appendChild(statusBar);

            const widget = document.createElement('div');
            widget.style.cssText = 'margin:18px 28px 4px;padding:16px 18px;'
                + 'background:rgba(255,255,255,0.14);border-radius:20px;'
                + 'backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);'
                + 'color:#fff;font-family:-apple-system,"SF Pro Display",'
                + '"Segoe UI",Roboto,sans-serif;';
            widget.innerHTML = `
                <div style="font-size:34px;font-weight:300;line-height:1;">{time_text}</div>
                <div style="font-size:13px;opacity:0.8;margin-top:4px;">{date_text}</div>`;
            win.appendChild(widget);

            const grid = document.createElement('div');
            grid.style.cssText = 'padding:14px 28px 0;display:grid;'
                + 'grid-template-columns:repeat(4, 1fr);'
                + 'row-gap:22px;align-content:start;';
            grid.innerHTML = `{app_cells}`;
            win.appendChild(grid);

            const dockWrap = document.createElement('div');
            dockWrap.style.cssText = 'margin:0 16px 22px;padding:14px 18px;'
                + 'background:rgba(255,255,255,0.14);border-radius:26px;'
                + 'display:flex;justify-content:space-around;'
                + 'backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);';
            dockWrap.innerHTML = `{dock_cells}`;
            win.appendChild(dockWrap);

            document.body.appendChild(win);

            setTimeout(() => {{
                win.style.transition = 'opacity 0.3s';
                win.style.opacity = '0';
                setTimeout(() => win.remove(), 320);
            }}, {int(duration * 1000)});
        """)
        evaluate_js(js)

    @staticmethod
    def _clean_apps(raw: list[Any], fallback: list[dict[str, str]]) -> list[dict[str, str]]:
        cleaned: list[dict[str, str]] = []
        for i, a in enumerate(raw):
            if not isinstance(a, dict):
                continue
            name = sanitize_html_text(str(a.get("name", f"App {i + 1}"))) or f"App {i + 1}"
            letter = sanitize_html_text(str(a.get("letter", name[0].upper()))) or name[0].upper()
            color = a.get("color") or fallback[i % len(fallback)]["color"]
            cleaned.append({"name": name, "letter": letter, "color": sanitize_css_color(color)})
        return cleaned or fallback
