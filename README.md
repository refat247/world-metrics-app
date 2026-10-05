# World Metrics App

Conversion of the original single-file `world-metrics.html` into an offline-first Progressive Web App (PWA) and a Capacitor 8 Android-ready project.

## What changed

- Preserved the original embedded D3, TopoJSON, world geometry, data, map interactions, search, flat/globe modes, and responsive country panel.
- Removed the Google Fonts network dependency; the existing CSS font fallbacks now make the UI fully functional offline.
- Removed the browser-only **Save file** control from the app shell.
- Added PWA manifest, install icons, safe-area handling, standalone/mobile metadata, and offline cache.
- Added local persistence for selected metric and flat/globe mode.
- Guarded service-worker registration so it runs in browsers/PWA mode but not inside Capacitor native WebView.
- Added pinned Capacitor 8.5.2 configuration for Android and iOS generation.

## Run as a web/PWA app

From the project directory:

```bash
python -m http.server 4173 --directory www
```

Open `http://localhost:4173`.

## Create the Android native project

**Windows / easiest:** double-click `SETUP_ANDROID_WINDOWS.bat`.

Manual requirements: Node.js 22+, Android Studio, Android SDK. Capacitor 8 targets Android SDK 36.

```bash
npm install
npx cap add android
npx cap sync android
npx cap open android
```

After any web change, run:

```bash
npx cap sync android
```

## Create the iOS native project

On macOS, double-click `SETUP_IOS_MAC.command` or follow `docs/IOS_BUILD_GUIDE.md`. Capacitor 8 requires macOS + Xcode for iOS builds.

## Build Android

See `docs/ANDROID_BUILD_GUIDE.md`. On Windows, a debug APK can be built from the generated Android project with:

```bat
cd android
gradlew.bat assembleDebug
```

Release AAB (after configuring a release signing key):

```bash
./gradlew bundleRelease
```

Never commit your `.jks`/`.keystore` or passwords.

## App identity

Current package/app ID: `app.worldmetrics.mobile`.

Change this before Play Store publication if you want your own permanent reverse-domain identifier. Changing an application ID after publishing creates a different app, so decide before the first production release.

## PWA service worker vs native Capacitor

The service worker is deliberately not registered inside Capacitor. This avoids interference with Capacitor's native bridge while retaining offline installation for the browser/PWA distribution.

## Original source

The unmodified source HTML is retained at `artifacts/original/world-metrics.html` for provenance and rollback. Its Git blob SHA is verified against the preserved Grok canonical source by `npm run audit:lineage`.

## Repository lineage

This codebase is the **production canonical** World Metrics implementation. The Grok-generated reference implementation remains preserved separately in `refat247/world-metrics` at branch `archive/grok-canonical-v1.0` (baseline commit `9bad10f022e2d07ffdf036d33ddf1b0e37fbe7ed`). See `docs/LINEAGE.md`.

Product changes should be made here rather than refactoring the Grok canonical repository into this architecture.

## Integrity checks

```bash
npm run audit
```

This runs both the application static audit and the provenance/lineage audit. GitHub Actions runs the same checks on pushes and pull requests.
