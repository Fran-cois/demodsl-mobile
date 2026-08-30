"""Unit tests for the mobile chrome effects (frame / push / home screen)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from demodsl.effects.registry import EffectRegistry
from demodsl.models import Effect
from demodsl.models.effects import register_plugin_effect_type
from demodsl_mobile import (
    MobileFrameEffect,
    MobileHomeScreenEffect,
    PushNotificationEffect,
    register,
)


@pytest.fixture(autouse=True, scope="module")
def _register_types():
    register_plugin_effect_type("mobile_frame", {"platform", "color", "time_text"})
    register_plugin_effect_type(
        "push_notification", {"app_name", "icon_letter", "title", "body", "theme", "hold"}
    )
    register_plugin_effect_type("mobile_home_screen", {"apps", "dock", "time_text", "theme"})


def _js(mock: MagicMock) -> str:
    return "".join(c.args[0] for c in mock.call_args_list)


class TestRegistration:
    def test_register_callable(self) -> None:
        reg = EffectRegistry()
        register(reg)
        assert "mobile_frame" in reg.browser_effects
        assert "push_notification" in reg.browser_effects
        assert "mobile_home_screen" in reg.browser_effects

    def test_effect_model_accepts(self) -> None:
        Effect(type="mobile_frame", duration=2.0)
        Effect(type="push_notification", duration=2.0)
        Effect(type="mobile_home_screen", duration=2.0)


class TestMobileFrame:
    def test_default_render_ios(self) -> None:
        m = MagicMock()
        MobileFrameEffect().inject(m, {})
        js = _js(m)
        assert "mobile_frame" in js
        assert "9:41" in js

    def test_android_platform(self) -> None:
        m = MagicMock()
        MobileFrameEffect().inject(m, {"platform": "android"})
        assert _js(m)  # doesn't crash

    def test_custom_time_and_color(self) -> None:
        m = MagicMock()
        MobileFrameEffect().inject(m, {"time_text": "10:30", "color": "#112233"})
        js = _js(m)
        assert "10:30" in js
        assert "#112233" in js

    def test_xss_escaped(self) -> None:
        m = MagicMock()
        MobileFrameEffect().inject(m, {"time_text": "<script>alert(1)</script>"})
        js = _js(m)
        assert "<script>alert(1)</script>" not in js

    def test_real_status_icons_not_emoji(self) -> None:
        m = MagicMock()
        MobileFrameEffect().inject(m, {})
        js = _js(m)
        assert "<svg" in js

    def test_battery_level_changes_fill_width(self) -> None:
        low = MagicMock()
        MobileFrameEffect().inject(low, {"battery": 10})
        high = MagicMock()
        MobileFrameEffect().inject(high, {"battery": 100})
        assert _js(low) != _js(high)


class TestPushNotification:
    def test_default_render(self) -> None:
        m = MagicMock()
        PushNotificationEffect().inject(m, {})
        js = _js(m)
        assert "push_notification" in js
        assert "Messages" in js

    def test_custom_content(self) -> None:
        m = MagicMock()
        PushNotificationEffect().inject(
            m,
            {
                "app_name": "Banking",
                "icon_letter": "B",
                "title": "Payment received",
                "body": "You got $42 from Alex.",
            },
        )
        js = _js(m)
        assert "Banking" in js
        assert "Payment received" in js
        assert "$42" in js

    def test_light_theme(self) -> None:
        m = MagicMock()
        PushNotificationEffect().inject(m, {"theme": "light"})
        assert _js(m)  # doesn't crash

    def test_hold_and_duration_affect_timers(self) -> None:
        m = MagicMock()
        PushNotificationEffect().inject(m, {"hold": 2.0, "duration": 3.0})
        js = _js(m)
        assert "2000" in js
        assert "3000" in js

    def test_xss_escaped(self) -> None:
        m = MagicMock()
        PushNotificationEffect().inject(m, {"title": "<script>alert(1)</script>"})
        js = _js(m)
        assert "<script>alert(1)</script>" not in js


class TestMobileHomeScreen:
    def test_default_render(self) -> None:
        m = MagicMock()
        MobileHomeScreenEffect().inject(m, {})
        js = _js(m)
        assert "mobile_home" in js
        assert "Mail" in js

    def test_custom_apps_and_dock(self) -> None:
        m = MagicMock()
        MobileHomeScreenEffect().inject(
            m,
            {
                "apps": [{"name": "Acme", "letter": "A", "color": "#ff0000"}],
                "dock": [{"name": "Chat", "letter": "C", "color": "#00ff00"}],
            },
        )
        js = _js(m)
        assert "Acme" in js
        assert "#00ff00" in js  # dock icons render colour/letter, not the name

    def test_solid_theme(self) -> None:
        m = MagicMock()
        MobileHomeScreenEffect().inject(m, {"theme": "solid"})
        assert _js(m)  # doesn't crash

    def test_xss_escaped(self) -> None:
        m = MagicMock()
        MobileHomeScreenEffect().inject(
            m, {"apps": [{"name": "<script>alert(1)</script>", "letter": "x"}]}
        )
        js = _js(m)
        assert "<script>alert(1)</script>" not in js

    def test_custom_date_text(self) -> None:
        m = MagicMock()
        MobileHomeScreenEffect().inject(m, {"date_text": "Friday, 1 January"})
        assert "Friday, 1 January" in _js(m)

    def test_real_status_icons_in_status_bar(self) -> None:
        m = MagicMock()
        MobileHomeScreenEffect().inject(m, {})
        assert "<svg" in _js(m)
