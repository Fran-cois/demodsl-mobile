"""DemoDSL Mobile — mobile phone chrome browser-effect plugins.

Provides realistic mobile chrome for product demos:

* ``mobile_frame``       — phone bezel + status bar + notch/home indicator
* ``push_notification``  — a push-notification banner sliding in/out
* ``mobile_home_screen`` — a fullscreen home-screen app grid + dock

Installed effects are auto-registered via the ``demodsl.effects.browser``
entry-point when this package is installed alongside demodsl.
"""

from __future__ import annotations

from demodsl_mobile.effects.mobile_frame import MobileFrameEffect
from demodsl_mobile.effects.mobile_home_screen import MobileHomeScreenEffect
from demodsl_mobile.effects.push_notification import PushNotificationEffect

__version__ = "0.1.0"

__all__ = [
    "MobileFrameEffect",
    "PushNotificationEffect",
    "MobileHomeScreenEffect",
    "register",
]

# ── Effect → valid params (keeps the "unused param" warning working) ──
# `accent` is filled from the demo's `theme:` block by the engine, for every
# effect that lists it here — see demodsl.theme._theme_effect.
_EFFECT_PARAMS = {
    "mobile_frame": {
        "platform",
        "color",
        "time_text",
        "accent",
    },
    "push_notification": {
        "app_name",
        "icon_letter",
        "title",
        "body",
        "theme",
        "accent",
        "hold",
    },
    "mobile_home_screen": {
        "apps",
        "dock",
        "time_text",
        "theme",
        "accent",
    },
}

_EFFECT_CLASSES = {
    "mobile_frame": MobileFrameEffect,
    "push_notification": PushNotificationEffect,
    "mobile_home_screen": MobileHomeScreenEffect,
}


def register(registry) -> dict[str, object]:
    """Entry-point callable: register effects and opt-in their types.

    Called by ``demodsl.engine._discover_effect_plugins`` with the engine's
    :class:`demodsl.effects.registry.EffectRegistry`.
    """
    from demodsl.models.effects import register_plugin_effect_type

    for name, cls in _EFFECT_CLASSES.items():
        registry.register_browser(name, cls())
        register_plugin_effect_type(name, _EFFECT_PARAMS[name])
    return {}
