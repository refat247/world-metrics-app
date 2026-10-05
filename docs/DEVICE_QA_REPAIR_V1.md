# Device QA Repair Gate v1

Source evidence: physical Android-device screen recording reviewed on 2026-10-05.

## Targeted defects

1. Android Back exited the app while country details were open.
2. Globe pinch zoom was visibly laggy/jittery.
3. Country selection left the soft keyboard open temporarily.
4. The active metric could remain clipped outside the horizontal selector viewport.
5. The mobile legend occupied excessive map area.
6. Reset-view could collide with overlays when the details sheet was open.
7. Keyboard-to-details transitions produced layout jumps.
8. Portrait flat-map space utilization was weak.
9. Root-level Back had no accidental-exit protection.

Repair policy: preserve data, metric semantics, Grok source provenance, and desktop behavior; modify only native navigation, gesture rendering, and mobile presentation required by device evidence.

## Implemented repair — v1.0.1

- Native Android `OnBackPressedCallback` delegates Back to web UI state before root exit.
- Back priority is search/keyboard → country details → root double-back exit.
- First root Back shows `Press back again to exit`; a second Back within 1.8 seconds exits.
- Globe pinch uses a lightweight SVG preview transform during the gesture and performs the expensive geographic reprojection once when the gesture ends.
- Drag, mouse-wheel zoom, and auto-spin globe redraws are coalesced with `requestAnimationFrame`.
- Country search selection blurs the input before opening details, dismissing the soft keyboard.
- Active metric buttons scroll into the mobile selector viewport.
- Mobile legend is compacted; reset-view is hidden while the details sheet is open to avoid collisions.
- Mobile details sheet uses dynamic viewport units; portrait flat-map fitting is enlarged/repositioned.
- App version advanced to `1.0.1`; Android `versionCode` advanced to `2`.

## Automated validation

Deterministic repair workflow: GitHub Actions run `37265609988` — PASS.

Strengthened production audit after repair: GitHub Actions run `37265729123` — PASS.

Native Android rebuild: GitHub Actions run `37265729061` (`Android Build Gate v1`, run #5) — PASS.

The native rebuild passed dependency installation, strengthened static/provenance audit, Capacitor sync, Java/Gradle compilation, APK verification, artifact upload, and native-source synchronization check.

## Repair APK

- Artifact: `world-metrics-debug-apk`
- Artifact ID: `11326073578`
- Artifact ZIP digest: `sha256:387635741dd2ce16a1895e4298cb04ec074cce8780b404b228112a0ae930208a`
- APK size: `4,559,402` bytes
- APK SHA-256: `e03f38ca5f92305136cb6ce46c643a7f71b6af114d3950fe40324d725128b97a`
- Retention: through 2026-11-04 under the current GitHub Actions retention window.

## Gate status

**SOURCE/BUILD REPAIR: PASS**

**PHYSICAL DEVICE RE-TEST: PENDING**

A successful build verifies that the native Back callback compiles and that the repaired web/native package remains buildable. It does not establish that gesture smoothness and Android Back behavior are satisfactory on the physical device. Close Device QA Repair Gate v1 only after installing this repaired APK and re-testing the nine targeted behaviors.
