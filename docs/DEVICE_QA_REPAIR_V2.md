# Device QA Repair v2

Source evidence: physical Android-device screenshot and follow-up QA on 2026-10-05.

Targeted residual defects:

1. The right-most metric option (`Internet`) can extend beyond the portrait viewport.
2. The app has no explicit in-app Portrait ↔ Landscape switch.
3. Flat-map rendering is visually too small in portrait while the previous scaling approach can exceed horizontal bounds.

Repair policy:

- Preserve data, metric semantics, Grok source provenance, Back handling, globe gesture repairs, and existing country-detail behavior.
- On mobile, render the five metric buttons as a contained five-column grid so every option remains inside the viewport.
- Add an explicit orientation control. Android uses a native JavaScript bridge to switch between portrait and landscape without recreating the Capacitor activity; the manifest already handles orientation/screen-size configuration changes.
- Fit Flat mode against the actual country FeatureCollection with a safe inset instead of scaling a Sphere by an arbitrary multiplier. This maximizes visible land size while keeping rendered country geometry inside the viewport.

Local preflight evidence before GitHub execution:

- 390×844 portrait: 241 country paths rendered; all five metric buttons fully contained; country geometry x-bounds 6–384 within a 390 px viewport; land width ≈96.9% of map width; orientation control displays `Landscape`.
- 844×390 landscape: 241 country paths rendered; all five metric buttons contained; orientation control displays `Portrait`.

Release target: World Metrics v1.0.2 / Android versionCode 3.
