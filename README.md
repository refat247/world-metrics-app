# World Metrics App

**Role:** PRODUCT CANONICAL  
**Version:** 1.0.0

Production PWA + Capacitor Android/iOS lineage derived from the preserved Grok reference implementation.

## Repository authority

- Grok reference canonical: `refat247/world-metrics`
- Frozen Grok baseline: `archive/grok-canonical-v1.0`
- Baseline commit: `9bad10f022e2d07ffdf036d33ddf1b0e37fbe7ed`
- Canonical HTML Git blob: `79487b79286ce7c8dbae0685db33ddaefffdeaee`
- Active production canonical: this repository, `refat247/world-metrics-app`

`artifacts/original/world-metrics.html` is fetched only from that pinned commit during bootstrap and is accepted only if its Git blob SHA matches the expected canonical value.

## Audit

```bash
npm run audit
```

## Browser / PWA

```bash
python -m http.server 4173 --directory www
```

Open `http://localhost:4173`.

## Android

Android Build Gate v1 has passed in GitHub Actions. The generated `android/` project and `package-lock.json` are now version-controlled production source.

On Windows, after installing Node.js 22+ and Android Studio, double-click `SETUP_ANDROID_WINDOWS.bat`. It uses `npm ci`, synchronizes the canonical web assets into the committed Android project, and opens Android Studio. If `android/` is ever missing, the script can regenerate it as a recovery path.

The CI workflow `.github/workflows/android-debug-build.yml` builds and verifies a debug APK and publishes it as the `world-metrics-debug-apk` artifact.

## iOS

Requires macOS + Xcode. Run `SETUP_IOS_MAC.command` when the iOS gate begins.

## Design rule

Do not merge Grok/App-Builder infrastructure into this repository merely because it exists upstream. Product features belong here; the Grok repository remains the preserved comparison/reference lineage.
