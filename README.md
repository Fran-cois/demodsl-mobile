# demodsl-mobile

Mobile phone chrome browser-effect plugins for [DemoDSL](https://github.com/Fran-cois/demodsl).

Gives product demos a convincing mobile-app moment, without a real device
or a 3D render:

| Effect | What it shows |
| --- | --- |
| `mobile_frame`        | Phone bezel (iOS or Android) with a live status bar, notch/dynamic-island (or camera dot), and a home indicator / nav row |
| `push_notification`   | A push-notification banner sliding in from the top, holding, then sliding away |
| `mobile_home_screen`  | A fullscreen home-screen app grid + dock, for the "and on mobile too" beat |

## Install

```bash
pip install demodsl-mobile
```

Effects are auto-registered via the `demodsl.effects.browser` entry-point —
no YAML or Python glue required.

## Use

`mobile_frame` is a ring, not a filled panel — pair it with a portrait-ish
`viewport:` so it reads as a real phone silhouette:

```yaml
scenarios:
  - name: mobile-tour
    url: "https://example.com"
    viewport: { width: 430, height: 932 }
    steps:
      - action: navigate
        url: "https://example.com"
        wait: 6
        effects:
          - type: mobile_frame
            duration: 6.0
            platform: ios

      - action: wait
        wait: 4
        effects:
          - type: push_notification
            duration: 3.5
            hold: 2.5
            app_name: "Banking"
            icon_letter: "B"
            title: "Payment received"
            body: "You got $42 from Alex."

      - action: wait
        wait: 4
        effects:
          - type: mobile_home_screen
            duration: 4.0
```

See `examples/demo_mobile_preview.yaml` for a full runnable config.

## Design fidelity

The status bar (signal / wifi / battery), Dynamic Island, home indicator
and Android back/home/recents glyphs are all real inline SVG shapes, not
emoji — tuned to read as an actual OS chrome at a glance rather than a
generic mockup. `mobile_home_screen` mirrors a real iOS home screen
(slim status bar + a small clock/date widget + app grid + dock), not a
lock screen. `battery` (0-100) and `date_text` are also available on
both `mobile_frame` and `mobile_home_screen`.
