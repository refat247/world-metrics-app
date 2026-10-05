# Release Audit — World Metrics App v1.0.3

## Status

**Release candidate: PASS — ready for Google Play Internal Testing.**

The remaining external boundary is Play Console ingestion/testing. Production rollout is not yet authorized by this audit.

## Provenance

- Grok baseline commit: `9bad10f022e2d07ffdf036d33ddf1b0e37fbe7ed`
- Preserved source HTML Git blob: `79487b79286ce7c8dbae0685db33ddaefffdeaee`
- The production lineage preserves that original artifact byte-for-byte while the active app is repaired independently.

## Product checks

`npm run audit` validates the original static/PWA invariants, Grok lineage, Android Back bridge, keyboard dismissal, globe gesture optimization, mobile metric containment, orientation control, safe Flat-map geometry fitting, and that the HTML app version matches `package.json`.

## Android Build Gate v1 — PASS / CLOSED

The original Android gate completed through generation, reproducibility, and repository-hygiene re-audit. The canonical Android project remains version-controlled while generated Capacitor/Gradle outputs stay ignored.

## Physical Device QA — PASS / CLOSED

### Device QA Repair v1 — v1.0.1 / versionCode 2

Physical-device recording identified Android Back exiting from country details, laggy globe pinch rendering, keyboard persistence after country selection, clipped metric navigation, oversized/colliding overlays, and mobile viewport transition defects.

Repair v1 introduced native Back delegation, root double-Back protection, lightweight pinch-preview scaling with one full reprojection at gesture end, requestAnimationFrame globe-paint coalescing, search blur, active-metric visibility, compact mobile overlays, and bottom-sheet viewport repairs. A follow-up physical recording confirmed the major Back, keyboard, metric-navigation and overlay fixes.

### Device QA Repair v2 — v1.0.2 / versionCode 3

Residual physical-device evidence showed three remaining presentation/navigation defects:

1. The right-most metric option could extend beyond the portrait viewport.
2. There was no explicit in-app Portrait ↔ Landscape control.
3. Flat mode was visually undersized while the prior arbitrary mobile scale multiplier could push country geometry beyond horizontal bounds.

Repair v2 changed the mobile metric selector to a contained five-column grid, added a native Android orientation bridge plus an in-app orientation toggle, and changed Flat-mode fitting to use the actual country FeatureCollection with a safe inset rather than an arbitrary Sphere scale multiplier.

Local browser preflight before native build:

- `390×844` portrait: 241 country paths rendered; all five metric buttons remained within the viewport; rendered country x-bounds were `6–384` inside a `390 px` viewport; visible country width was about `96.9%` of the map width; orientation control target displayed `Landscape`.
- `844×390` landscape: 241 country paths rendered; all five metric buttons remained contained; orientation control target displayed `Portrait`.

GitHub Actions Device QA Repair Gate v2 run `37268521160` completed successfully after one audit-marker repair loop.

### Final physical-device verification — 2026-10-05

Recording-based re-audit confirmed:

- all five metric options remain inside the portrait viewport;
- Portrait → Landscape and Landscape → Portrait switching works;
- Flat mode is materially larger without horizontal clipping at reset view;
- country-detail Back handling remains fixed;
- search selection dismisses the keyboard;
- the prior blocker-level zoom lag is resolved.

The user manually verified the final two checks:

- offline cold launch works with network connectivity disabled;
- at the root screen, first Back presents the exit warning and second Back exits as designed.

**Device QA v2 verdict: PASS / CLOSED.**

## Release Branding Gate — PASS / CLOSED

A release-quality audit found that the initial Capacitor Android project still contained the stock Android launcher foreground and white adaptive-icon background. That candidate was rejected before Play upload.

World Metrics release branding was then generated deterministically for **v1.0.3 / versionCode 4**:

- dark World Metrics launcher identity (`#0B1118` background);
- cyan globe + metric-bar motif;
- normal, round and adaptive launcher assets across Android densities;
- portrait and landscape splash assets across Android densities;
- 512×512 Google Play store icon at `artifacts/store/google-play-icon-512.png`.

Release Branding Gate run `37273216077` passed source/provenance audit, asset checks, Capacitor sync, branded debug APK build, release AAB build, artifact verification and canonical source promotion.

Brand source commit: `93483ff0519713e8d7788a9474cf3165bc3c4b73`.

The one-use branding workflow was removed after successful promotion. Final post-cleanup Production Integrity run `37273543377` passed on commit `3adc3e3bb6c79e4ae74970a1a03e6b41bd17746c`.

### Branded build hashes

- Branded debug APK SHA-256: `bf7ebed1a53c25f7ed52285f0d64eff0f292114df826a3a284f01093c1ec698a`
- Branded release AAB before private upload-key signing SHA-256: `1bdba883ce8169d0b5d0143c874917c315e96516c77b2cc6ecae06f6ed05ad16`

## Upload-key Signing Gate — PASS

A dedicated upload keystore was generated **outside the public repository** and used to sign the final branded v1.0.3 release bundle. `jarsigner -verify` returned `jar verified.`

Final Play upload candidate:

- File: `world-metrics-v1.0.3-signed.aab`
- Version name: `1.0.3`
- Version code: `4`
- Application ID: `app.worldmetrics.mobile`
- Signed AAB size: `3,393,492` bytes
- Signed AAB SHA-256: `161650b129340d43c064d738a083c5df10bd7a618e3815e2aa5cfb736b890c0b`
- Upload-key alias: `worldmetrics-upload`
- Upload certificate SHA-1: `0B:71:B9:86:37:62:81:B7:1A:A8:4E:4E:20:91:E7:E6:5C:B8:43:1E`
- Upload certificate SHA-256: `18:1A:BD:92:0E:79:E7:F2:0F:5A:36:EA:EE:80:3B:98:B7:8F:07:E4:4F:F8:DA:AF:82:F3:A0:88:79:04:4A:37`

**Security boundary:** the upload keystore, keystore password and key password are private release credentials and are not stored in this public repository.

## Android baseline

- Capacitor: `8.5.2`
- Java: `21` in CI
- `minSdkVersion`: `24`
- `compileSdkVersion`: `36`
- `targetSdkVersion`: `36`
- Application ID: `app.worldmetrics.mobile`
- App version: `1.0.3`
- Android versionCode: `4`
- Dependency installation: lockfile-first via `npm ci`
- Native project: `android/` is version-controlled production source
- Generated sync/build outputs: ignored and regenerated by Capacitor/Gradle

## Google Play release readiness

Google Play's current phone/tablet requirement is Android 16 / API level 36 or higher for new apps and app updates. This app targets API 36, so the target-SDK gate is satisfied.

For a new app, Play App Signing is automatically used with Google-generated app-signing keys; the developer upload key signs the release app bundle sent to Play.

Official references:

- https://support.google.com/googleplay/android-developer/answer/11926878
- https://support.google.com/googleplay/android-developer/answer/9842756
- https://support.google.com/googleplay/android-developer/answer/9845334

## Current validation boundary

Source integrity, Grok provenance, reproducible Android compilation, physical-device QA, offline launch, Android Back behavior, orientation handling, release branding, API-level compliance, upload-key signing, and final AAB verification are established.

**Next gate: Google Play Internal Testing.** Upload the signed v1.0.3 AAB, add testers, install through Google Play, and perform one Play-delivered smoke test before considering any production release.