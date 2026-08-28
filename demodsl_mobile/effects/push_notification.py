"""Push notification banner — slides down from the top, holds, slides
back up. iOS/Android style rounded card with an app icon, title and body.
"""

from __future__ import annotations

from typing import Any

from demodsl.effects.js_builder import iife, inject_style
from demodsl.effects.registry import BrowserEffect
from demodsl.effects.sanitize import sanitize_html_text, sanitize_number
from demodsl_mobile.effects._theme import themed_accent


class PushNotificationEffect(BrowserEffect):
    """A single push-notification banner sliding in from the top.

    Params
    ------
    app_name : str
        App name shown in the small header row (default ``"Messages"``).
    icon_letter : str
        Single character/emoji for the app-icon square (default first
        letter of *app_name*).
    title : str
        Bold notification title.
    body : str
        Notification body text (one or two lines).
    theme : str
        ``"dark"`` (default) or ``"light"`` card chrome.
    hold : float
        Seconds the banner stays fully visible before sliding away
        (default ``3.0``).
    duration : float
        Total seconds on screen, including the two 0.4s slide animations
        (default ``4.0``; should be >= ``hold + 0.8``).
    """

    effect_id = "push_notification"

    _THEMES = {
        "dark": {"bg": "rgba(40,40,45,0.92)", "fg": "#F2F2F2", "fg_muted": "#A9A9AD"},
        "light": {"bg": "rgba(250,250,250,0.92)", "fg": "#1A1A1A", "fg_muted": "#6E6E73"},
    }

    def inject(self, evaluate_js: Any, params: dict[str, Any]) -> None:
        app_name = sanitize_html_text(str(params.get("app_name", "Messages"))) or "Messages"
        icon_letter = (
            sanitize_html_text(str(params.get("icon_letter", app_name[0].upper())))
            or app_name[0].upper()
        )
        title = sanitize_html_text(str(params.get("title", "New message")))
        body = sanitize_html_text(str(params.get("body", "")))
        theme = params.get("theme", "dark")
        if theme not in self._THEMES:
            theme = "dark"
        pal = dict(self._THEMES[theme])
        accent = themed_accent(params, "#3478F6")
        hold = sanitize_number(params.get("hold", 3.0), default=3.0, min_val=0.2, max_val=30.0)
        duration = sanitize_number(
            params.get("duration", 4.0), default=4.0, min_val=1.0, max_val=40.0
        )

        css = """
            @keyframes __demodsl_push_in {
              0%   { transform: translate(-50%, -140%); opacity: 0; }
              100% { transform: translate(-50%, 0); opacity: 1; }
            }
            @keyframes __demodsl_push_out {
              0%   { transform: translate(-50%, 0); opacity: 1; }
              100% { transform: translate(-50%, -140%); opacity: 0; }
            }
        """
        evaluate_js(inject_style("__demodsl_push_style", css))

        js = iife(f"""
            const old = document.getElementById('__demodsl_push_notification');
            if (old) old.remove();

            const card = document.createElement('div');
            card.id = '__demodsl_push_notification';
            card.style.cssText = 'position:fixed;top:14px;left:50%;'
                + 'transform:translate(-50%,-140%);width:min(92vw,420px);'
                + 'z-index:2147483642;background:{pal["bg"]};color:{pal["fg"]};'
                + 'border-radius:20px;padding:12px 14px;'
                + 'box-shadow:0 10px 40px rgba(0,0,0,0.35);'
                + 'backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);'
                + 'font-family:-apple-system,"SF Pro Text","Segoe UI",Roboto,sans-serif;'
                + 'animation:__demodsl_push_in 0.4s cubic-bezier(0.2,0.8,0.2,1) forwards;';

            card.innerHTML = `
                <div style="display:flex;gap:10px;align-items:flex-start;">
                  <div style="width:34px;height:34px;flex:none;border-radius:9px;
                      background:{accent};color:#fff;display:flex;
                      align-items:center;justify-content:center;
                      font-weight:700;font-size:16px;">{icon_letter}</div>
                  <div style="min-width:0;flex:1;">
                    <div style="display:flex;justify-content:space-between;
                        color:{pal["fg_muted"]};font-size:12px;
                        text-transform:uppercase;letter-spacing:0.02em;">
                      <span>{app_name}</span><span>now</span>
                    </div>
                    <div style="font-weight:700;font-size:15px;margin-top:1px;">
                      {title}
                    </div>
                    <div style="font-size:14px;color:{pal["fg_muted"]};
                        margin-top:1px;overflow:hidden;text-overflow:ellipsis;
                        display:-webkit-box;-webkit-line-clamp:2;
                        -webkit-box-orient:vertical;">{body}</div>
                  </div>
                </div>`;

            document.body.appendChild(card);

            setTimeout(() => {{
                card.style.animation =
                    '__demodsl_push_out 0.4s cubic-bezier(0.4,0,1,1) forwards';
                setTimeout(() => card.remove(), 420);
            }}, {int(hold * 1000)});

            setTimeout(() => {{ if (card.isConnected) card.remove(); }}, {int(duration * 1000)});
        """)
        evaluate_js(js)
